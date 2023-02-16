from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
import stripe

import test_project.settings as settings
from test_app.models import Item


stripe.api_key = settings.PRIVATE_STRIPE_API_KEY
public_key = settings.PUBLIC_STRIPE_API_KEY
YOUR_DOMAIN = settings.YOUR_DOMAIN


class GetItemPageView(generic.View):
    def get(self, request, pk):
        item = get_object_or_404(Item, pk=pk)
        return render(
            request,
            'test_app/index.html',
            {'item': item, 'api_key': public_key,
             'price': item.price / 100})


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
