from django.urls import path
from . import views

urlpatterns = [
    path('billing_success', views.billing_success, name='billing_success'),
    path('checkout', views.checkout, name='checkout'),
    path('billing_details', views.billing_details, name='billing_details'),
    path('process_order', views.process_order, name='process_order'),
    

]