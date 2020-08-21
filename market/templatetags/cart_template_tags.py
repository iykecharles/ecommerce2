from market.models import Order
from django import template

register = template.Library()

@register.filter
def cart_counter(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0