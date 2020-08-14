from django.db import models
from django.conf import settings
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    dpid = models.CharField(max_length=16, unique=True, null = True) #16 digit
    pan_no = models.CharField(max_length=10, unique=True, null = True) #10 digit
    phone_no = models.CharField(max_length=10, unique=True)
    email = models.CharField(max_length =40, unique=True)


class Share(models.Model):
    share_name = models.CharField(max_length=50)
    s_description = models.CharField(max_length=150)
    ltp = models.FloatField()
    quantity = models.IntegerField()

    def __str__(self):
        return self.share_name


class Bid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    share = models.ForeignKey(Share, on_delete=models.CASCADE)
    bid_price = models.FloatField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.share.share_name + '@' + str(self.bid_price)


class Ask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    share = models.ForeignKey(Share, on_delete=models.CASCADE)
    ask_price = models.FloatField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.share.share_name + '@' + str(self.ask_price)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        SUBMITTED = 'SUBMITTED'
        PROCESSING = 'PROCESSING'
        FAILED = 'FAILED'
        COMPLETE = 'COMPLETE'
        CANCELLED = 'CANCELLED'

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    share = models.ForeignKey(Share, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    # create orde status enums - PROCESSING, COMPLETE, FAILED ....
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    order_status = models.CharField(
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.SUBMITTED
    )

    def __str__(self):
        return self.share.share_name + '@' + str(self.price) + '-' + str(self.quantity)


class OrderQ(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING = 'PENDING'
        EXECUTED = 'EXECUTED'
        FAILED = 'FAILED'
        COMPLETE = 'COMPLETE'
        CANCELLED = 'CANCELLED'

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buyer2seller')
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller2buyer')
    price = models.FloatField()
    quantity = models.IntegerField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_status = models.CharField(
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.EXECUTED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
