from django.contrib import admin
from .models import Address, OrderItem, Order, Coupon, Refund, Payment, Item

admin.site.register(Address)
admin.site.register(OrderItem)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Coupon)
admin.site.register(Refund)
admin.site.register(Payment)
