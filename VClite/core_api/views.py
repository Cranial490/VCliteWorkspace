from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
# from rest_framework.decorators import api_view

from .serializers import *
from .models import *
from rest_framework.response import Response
from core_api.utils import validate_order
from core_api.matching import matching_engine

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import GenericAPIView, UpdateAPIView
from django.contrib.auth.models import User


class ShareViewSet(viewsets.ModelViewSet):
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    permission_classes = (AllowAny,)

    def delete(self, request, *args, **kwargs):
        response = {'message': 'Share cannot be deleted'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class AskViewSet(viewsets.ModelViewSet):
    queryset = Ask.objects.all()
    serializer_class = AskSerializer
    #permission_classes = (AllowAny,)
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        id = self.request.query_params.get('share_id')
        if(id != None):
            queryset = Ask.objects.filter(
                share__id__contains=id).order_by('ask_price')
            return queryset
        else:
            return Ask.objects.none()


class BidViewSet(viewsets.ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    #permission_classes = (AllowAny,)
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        id = self.request.query_params.get('share_id')
        if(id != None):
            queryset = Bid.objects.filter(
                share__id__contains=id).order_by('-bid_price')
            return queryset
        else:
            return Bid.objects.none()

def dataValid(data):
    if int(data['price']) > 0 and int(data['quantity']) > 0:
        return True
    else:
        return False


def stringValid(dataString):
    if dataString and dataString.strip():
        return True
    else:
        return False


def userExists(username):
    if CustomUser.objects.filter(username=username).count() > 0:
        return True
    else:
        return False


def shareExists(name):
    if Share.objects.filter(name=name).count() > 0:
        return True
    else:
        return False

def validate_data(request):
    print(request.data)
    if (stringValid(request.data['quantity']) and
        stringValid(request.data['price']) and
        stringValid(request.data['order_type']) and
        stringValid(request.data['share']) and
            dataValid(request.data)):

        if(userExists(request.user) and shareExists(request.data['share'])):
            print("returning True userExists")
            return True
        else:
            print("returning True userNotExists")
            return False
    else:
        return False

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    @action(methods=['POST'], detail=False, url_path='execute')
    def execute_order(self, request):
        print(request.user)
        if request.method == 'POST':
            if validate_data(request):
                parentOrder, order = createOrder(request)
                orderBook = getOrderBook(order)
                trades = matching_engine(orderBook, order, parentOrder)
                response = {'message': 'Order placed successfully'}
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {'message': 'Invalid data'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

    @ action(methods=['POST'], detail=False, url_path='cancel')
    def cancel_order(self, request):
        print("Order Cancelled")
        # Change parentOrder Status to Cancelled
        # Delete related Bid and Ask entries
        #


class OrderQViewSet(viewsets.ModelViewSet):
    queryset = OrderQ.objects.all()
    serializer_class = OrderQSerializer
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet, UpdateModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        username = str(self.request.user.username)
        if(username != None):
            queryset = CustomUser.objects.filter(username=username)
            return queryset
        else:
            return CustomUser.objects.none()

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class UserPartialUpdateView(UpdateAPIView, UpdateModelMixin):
    '''
    You just need to provide the field which is to be modified.
    '''
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'username'
    #if form.is_valid:
    #    form.save()

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,) #handle if directly accessed this link 
