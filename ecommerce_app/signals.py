from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from  paypal.standard.ipn.signals import valid_ipn_received
from .models import Order


@receiver(valid_ipn_received)
def payment_notification(sender, **kwargs):
    ipn=sender
    if ipn.payment_status=='complete':
        order=get_object_or_404(Order, id=ipn.invoice)
        if order.total_cost()==ipn.mc_gross:
            Order.paid=True
            Order.save()


