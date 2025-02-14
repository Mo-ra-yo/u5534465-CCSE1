from django.db import models
from django.contrib.auth.models import User
from aromatica.models import Product, Order
from django.db.models.signals import post_save

# Create your models here.

class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    bill_full_name = models.CharField(max_length=250)
    bill_email = models.CharField(max_length=250)
    bill_address1 = models.CharField(max_length=250)
    bill_address2 = models.CharField(max_length=250)
    bill_postcode = models.CharField(max_length=250)
    bill_country = models.CharField(max_length=250)

    # dont make address plural

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    
#create shipping address

def create_shipping(sender, instance, created, **kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()

post_save.connect(create_shipping, sender=User)

    
#create order model

class Order(models.Model):
    #foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250)
    email = models.EmailField(max_length=250)
    shipping_address = models.TextField(max_length=20000)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)

    def __str__(self):
        return f'order - {str(self.id)}'
    
#creates order  item model    
    
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'


