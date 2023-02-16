from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
import stripe

import test_project.settings as settings
from test_app.models import Item, Order


stripe.api_key = settings.PRIVATE_STRIPE_API_KEY
public_key = settings.PUBLIC_STRIPE_API_KEY
YOUR_DOMAIN = 'http://localhost:80'


class GetItemPageView(generic.View):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        return render(
            request,
            'test_app/index.html',
            {'item': item, 'api_key': public_key},
        )


class CreateCheckoutSession(generic.View):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': item.currency,
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success/',
            cancel_url=YOUR_DOMAIN + '/cancel/',
        )
        return JsonResponse({
            'id': session.id
        })


class SuccessView(generic.TemplateView):
    template_name = 'test_app/success.html'


class CancelView(generic.TemplateView):
    template_name = 'test_app/cancel.html'


class ConfirmOrderView(generic.View):
    def get(self, request, pk):
        order = get_object_or_404(Order.objects.prefetch_related('item'),
                                  pk=pk)
        items = order.item.filter()
        amount = int(order.get_total_price * 100)
        currency = str(order.item.filter()[0].currency)
        return render(
            request,
            template_name='test_app/cart.html',
            context={
                'order': order,
                'items': items,
                'currency': currency,
                'api_key': public_key,
            }
        )


class CreatePaymentIntentView(generic.View):
    def post(self, request, *args, **kwargs):
        try:
            order = get_object_or_404(Order.objects.prefetch_related('item'),
                                      pk=self.kwargs['pk'])
            amount = int(order.get_total_price * 100)
            currency = str(order.item.filter()[0].currency)
            intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            return JsonResponse({
                'clientSecret': intent['client_secret']
            })
        except Exception as e:
            return JsonResponse({'error': str(e)})


class CreatePaymentIntent(generic.View):
    def post(self, request, *args, **kwargs):
        order_pk = request.POST.get('pk')
        order = get_object_or_404(Order.objects.prefetch_related('item'),
                                  pk=order_pk)

        payment_intent = stripe.PaymentIntent.create(
            amount=order.total_price,
            currency=order.item.filter()[0].currency
        )
        return JsonResponse({'clientSecret': payment_intent.client_secret})