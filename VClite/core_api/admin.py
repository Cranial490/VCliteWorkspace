from django.contrib import admin
from .models import Share, Bid, Ask, Order, OrderQ
from django.contrib.auth import get_user_model
User = get_user_model()

admin.site.register(User)
admin.site.register(Share)
admin.site.register(Bid)
admin.site.register(Ask)
admin.site.register(Order)
admin.site.register(OrderQ)
# Register your models here.
