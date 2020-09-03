from django.db import models
from django.conf import settings
from datetime import date
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


class VC_T_User(AbstractUser):
    dpid = models.CharField(max_length=16, unique=True, null=True)  # 16 digit
    pan_no = models.CharField(
        max_length=10, unique=True, null=True)  # 10 digit
    phone_no = models.CharField(max_length=10, unique=True)
    email = models.CharField(max_length=40, unique=True)

    def send_reset_password_success_email(self, subject, tempHTML, tempText):
        """
        Send email notifying users that their password was successfully reset.
        Validation key is cleared so the reset password link only works once.
        """
        self.validation_key = None
        self.save()
        self._send_html_mail(
            subject,
            'email/{}.html'.format(tempHTML),
            'email/{}.txt'.format(tempText))

    def _send_html_mail(self, subject, template_html, template_text, **context):
        """
        Renders templates to context, and uses EmailMultiAlternatives to
        send email.
        """
        if not template_html:
            raise ValueError('No HTML template provided for email.')
        if not template_text:
            raise ValueError('No text template provided for email.')
        default_context = {
            "settings": settings,
            #"user": self
            'url': settings.SITE_URL,
            'username': self
        }
        default_context.update(context)
        from_email = settings.DEFAULT_FROM_EMAIL
        body_text = render_to_string(template_text, default_context)
        body_html = render_to_string(template_html, default_context)

        msg = EmailMultiAlternatives(
            subject=subject, body=body_text,
            from_email=from_email, to=[self.email])
        msg.attach_alternative(body_html, 'text/html')
        msg.send()


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

    def __str__(self):
        return self.parent_order.share.name + '@' + str(self.price) + '-' + str(self.filled_quantity)


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

    def __str__(self):
        return self.buyer.username + '-' + self.seller.username + '-' + str(self.price)
