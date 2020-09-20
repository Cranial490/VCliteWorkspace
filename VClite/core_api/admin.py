from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
#User = get_user_model()

admin.site.register(VC_T_Share)
admin.site.register(VC_T_Bid)
admin.site.register(VC_T_Ask)
admin.site.register(VC_T_Order)
admin.site.register(VC_T_Order_Queue)
admin.site.register(VC_T_Order_Executed)
admin.site.register(VC_T_User)
# Register your models here.
