from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User


# Register your models to admin section
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

class OrderItemInLine(admin.StackedInline):
    model = OrderItem
    extra = 0

    #extend order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ["date_ordered"]
    #fields = ["user", "full_name"]
    inlines = [OrderItemInLine]
    

#unregister order mdoel
admin.site.unregister(Order)
admin.site.register(Order, OrderAdmin)

