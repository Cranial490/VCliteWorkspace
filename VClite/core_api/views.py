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


class ShareViewSet(viewsets.ModelViewSet):
    queryset = VC_T_Share.objects.all()
    serializer_class = ShareSerializer
    permission_classes = (AllowAny,)

    def delete(self, request, *args, **kwargs):
        response = {'message': 'Share cannot be deleted'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class AskViewSet(viewsets.ModelViewSet):
    queryset = VC_T_Ask.objects.all()
    serializer_class = AskSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        id = self.request.query_params.get('share_id')
        if(id != None):
            queryset = VC_T_Ask.objects.filter(
                share__id__contains=id).order_by('ask_price')
            return queryset
        else:
            return VC_T_Ask.objects.none()


class BidViewSet(viewsets.ModelViewSet):
    queryset = VC_T_Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        id = self.request.query_params.get('share_id')
        if(id != None):
            queryset = VC_T_Bid.objects.filter(
                share__id__contains=id).order_by('-bid_price')
            return queryset
        else:
            return VC_T_Bid.objects.none()


class OrderExecutedViewSet(viewsets.ModelViewSet):
    queryset = VC_T_Order_Executed.objects.all()
    serializer_class = OrderExecutedSerializer
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = VC_T_User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class OrderQViewSet(viewsets.ModelViewSet):
    queryset = VC_T_Order_Queue.objects.all()
    serializer_class = OrderQSerializer
    permission_classes = (AllowAny,)


def getOrderBook(order):
    if order.parent_order.order_type == "BUY":
        orderBook = VC_T_Ask.objects.filter(
            share__name__contains=order.share.name, ask_price=order.bid_price)
        return orderBook.order_by('created_at')
    elif order.parent_order.order_type == "SELL":
        orderBook = VC_T_Bid.objects.filter(
            share__name__contains=order.share.name, bid_price=order.ask_price)
        return orderBook.order_by('created_at')


def createOrder(request):
    parentOrder = VC_T_Order(
        user=VC_T_User.objects.filter(username=request.data['user'])[0],
        share=VC_T_Share.objects.filter(name=request.data['share'])[0],
        price=float(request.data['price']),
        quantity=int(request.data['quantity']),
        order_type=request.data['order_type'],
        updated_quantity=int(request.data['quantity'])
    )
    parentOrder.save()
    if parentOrder.order_type == 'BUY':
        order = VC_T_Bid(
            user=parentOrder.user,
            share=parentOrder.share,
            parent_order=parentOrder,
            bid_price=parentOrder.price,
            quantity=parentOrder.updated_quantity
        )
    elif parentOrder.order_type == 'SELL':
        order = VC_T_Ask(
            user=parentOrder.user,
            share=parentOrder.share,
            parent_order=parentOrder,
            ask_price=parentOrder.price,
            quantity=parentOrder.updatedQuantity
        )
    # order.save()
    return parentOrder, order


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
    if VC_T_User.objects.filter(username=username).count() > 0:
        return True
    else:
        return False


def shareExists(name):
    if VC_T_Share.objects.filter(name=name).count() > 0:
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
    queryset = VC_T_Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (AllowAny,)

    @ action(methods=['POST'], detail=False, url_path='execute')
    def execute_order(self, request):
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
