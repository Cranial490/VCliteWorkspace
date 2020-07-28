from django.db import models
from django.conf import settings
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class VC_T_User(AbstractUser):
    dpid = models.CharField(max_length=16)
    phone_no = models.CharField(max_length=10)
    pan_no = models.CharField(max_length=10)


class VC_T_Share(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    ltp = models.FloatField()
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class VC_T_Order(models.Model):
    class OrderStatus(models.TextChoices):
        SUBMITTED = 'SUBMITTED'
        PROCESSING = 'PROCESSING'
        FAILED = 'FAILED'
        COMPLETE = 'COMPLETE'
        CANCELLED = 'CANCELLED'

    class OrderType(models.TextChoices):
        BUY = 'BUY'
        SELL = 'SELL'

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    share = models.ForeignKey(VC_T_Share, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField()
    updated_quantity = models.IntegerField()
    order_status = models.CharField(
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.SUBMITTED
    )
    order_type = models.CharField(
        max_length=4,
        choices=OrderType.choices,
        default=OrderType.BUY
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.share.name + '@' + str(self.price) + '-' + str(self.quantity)


class VC_T_Bid(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    share = models.ForeignKey(VC_T_Share, on_delete=models.CASCADE)
    bid_price = models.FloatField()
    quantity = models.IntegerField()
    parent_order = models.ForeignKey(VC_T_Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.share.name + '@' + str(self.bid_price)


class VC_T_Ask(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    share = models.ForeignKey(VC_T_Share, on_delete=models.CASCADE)
    ask_price = models.FloatField()
    quantity = models.IntegerField()
    parent_order = models.ForeignKey(VC_T_Order, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.share.name + '@' + str(self.ask_price)


class VC_T_Order_Executed(models.Model):
    class OrderStatus(models.TextChoices):
        EXECUTED = 'EXECUTED'
        FAILED = 'FAILED'
        COMPLETE = 'COMPLETE'

    parent_order = models.ForeignKey(VC_T_Order, on_delete=models.CASCADE)
    price = models.FloatField()
    filled_quantity = models.IntegerField()
    order_status = models.CharField(
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.EXECUTED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class VC_T_Order_Queue(models.Model):
    class OrderStatus(models.TextChoices):
        SUBMITTED = 'SUBMITTED'
        EXECUTED = 'EXECUTED'
        FAILED = 'FAILED'
        COMPLETE = 'COMPLETE'
        CANCELLED = 'CANCELLED'

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='buyer2seller')
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller2buyer')
    buyer_order_child = models.ForeignKey(
        VC_T_Order_Executed, on_delete=models.CASCADE, related_name='buyerOrder')
    seller_order_child = models.ForeignKey(
        VC_T_Order_Executed, on_delete=models.CASCADE, related_name='sellerOrder')
    price = models.FloatField()
    quantity = models.IntegerField()

    order_status = models.CharField(
        max_length=10,
        choices=OrderStatus.choices,
        default=OrderStatus.SUBMITTED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
