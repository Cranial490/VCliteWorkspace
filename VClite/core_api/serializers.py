from rest_framework import serializers

from .models import *
from rest_framework.authtoken.models import Token


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = VC_T_Share
        fields = '__all__'


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = VC_T_Bid
        fields = '__all__'


class AskSerializer(serializers.ModelSerializer):
    class Meta:
        model = VC_T_Ask
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = VC_T_Order
        fields = '__all__'


class OrderExecutedSerializer(serializers.ModelSerializer):
    class Meta:
        model = VC_T_Order_Executed
        fields = '__all__'


class OrderQSerializer(serializers.ModelSerializer):
    class Meta:
        model = VC_T_Order_Queue
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VC_T_User
        fields = '__all__'
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def create(self, validated_data):
        user = VC_T_User.objects.create(**validated_data)
        Token.objects.create(user=user)
        return user
