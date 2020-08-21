from django.db import models
from django.contrib.auth.models import User
"""from users.models import prof_receiver"""
from django_countries.fields import CountryField
from django.urls import reverse

LABEL_CATEGORY = (
    ("WC", "WINTER_WEARS"),
    ("OW", "OUTDOOR_WEARS"),

)

SIZE_CATEGORY = (
    ("XXL", "EXTRA_EXTRA_LARGE"),
    ("XL", "EXTRA_LARGE"),
    ("L", "LARGE"),
    ("M", "MEDIUM"),
    ("S", "SMALL"),

)

ADDRESS_CHOICES = (
    ("B", "billing"),
    ("S", "shipping"),
)


"""class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    one_click_purchasing = models.BooleanField(default=False)
    image = models.ImageField()
    stripe_customer_id = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} Profile"
        """

"""class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    one_click_purchasing = user = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=30)"""
    

class Item(models.Model):
    title = models.CharField(max_length=15)
    description = models.TextField(max_length=300)
    image = models.ImageField(default="army_pakistan_hd-t2.jpg")
    price = models.FloatField()
    discount_price = models.FloatField()
    label = models.CharField(max_length=2, choices = LABEL_CATEGORY)
    sizes = models.CharField(max_length=3, choices = SIZE_CATEGORY)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("market-details", kwargs={pk:self.pk})

class OrderItem(models.Model):
    quantity = models.IntegerField(default=1)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, null=True, blank=True)
    ordered = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def individual_total(self):
        return self.quantity*self.item.price

    def individual_discount_total(self):
        return self.quantity*self.item.discount_price

class Order(models.Model):
    items = models.ManyToManyField(OrderItem)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20)
    shipping_address = models.ForeignKey("Address", related_name="shipping_address", on_delete=models.CASCADE)
    billing_address = models.ForeignKey("Address", related_name="billing_address", on_delete=models.CASCADE)
    coupon = models.ForeignKey("Coupon", on_delete=models.CASCADE)
    payment = models.ForeignKey("Payment", on_delete=models.CASCADE)
    refund_granted = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    being_delievered = models.BooleanField(default=False)
    ordered = models.BooleanField(default=False)
    recieved = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()

    def __str__(self):
        return self.user.username

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    home_address = models.CharField(max_length=50)
    street_address = models.CharField(max_length=50)
    country = CountryField(multiple=False) 
    zip = models.CharField(max_length=20)
    default = models.BooleanField(default=False)
    address_type = models.CharField(max_length=2, choices=ADDRESS_CHOICES)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Addresses"

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stripe_charge_id = models.CharField(max_length=60)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Coupon(models.Model):
    code = models.CharField(max_length=20)
    amount = models.FloatField()

    def __str__(self):
        return self.code

class Refund(models.Model):
    email = models.EmailField(max_length=20)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    




