from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField()
    one_click_purchasing = models.BooleanField(default=False)
    stripe_customer_id = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.user.username} Profile"


"""def userprofile_receiver(sender, instance, created, **kwargs):
    if created:
        userprofile = UserProfile.objects.create(user=instance)


post_save.connect(userprofile_receiver, sender=User)"""
