from rest_framework import serializers

from .models import *
from rest_framework.authtoken.models import Token


class ShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = Share
        fields = '__all__'


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = '__all__'


class AskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ask
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderQSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderQ
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {'password': {'required': True, 'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create(**validated_data)
        Token.objects.create(user=user)
        user.set_password(validated_data['password'])
        user.save()
        return user
