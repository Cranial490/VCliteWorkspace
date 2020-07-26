from django.contrib import admin
from .models import VC_T_Share, VC_T_Bid, VC_T_Ask, VC_T_Order, VC_T_Order_Queue
from django.contrib.auth import get_user_model
User = get_user_model()

admin.site.register(User)
admin.site.register(VC_T_Share)
admin.site.register(VC_T_Bid)
admin.site.register(VC_T_Ask)
admin.site.register(VC_T_Order)
admin.site.register(VC_T_Order_Queue)
# Register your models here.
