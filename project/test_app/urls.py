from django.urls import path
from . import views


urlpatterns = [
    path('item/<int:pk>/', views.GetItemPageView.as_view()),
    path('buy/<int:pk>/', views.CreateCheckoutSession.as_view(),
         name='buy'),
    path('cancel/', views.CancelView.as_view()),
    path('success/', views.SuccessView.as_view()),
]