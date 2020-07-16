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
    queryset = Share.objects.all()
    serializer_class = ShareSerializer
    permission_classes = (AllowAny,)

    def delete(self, request, *args, **kwargs):
        response = {'message': 'Share cannot be deleted'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class AskViewSet(viewsets.ModelViewSet):
    queryset = Ask.objects.all()
    serializer_class = AskSerializer
    permission_classes = (AllowAny,)

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
    permission_classes = (AllowAny,)

    def get_queryset(self):
        id = self.request.query_params.get('share_id')
        if(id != None):
            queryset = Bid.objects.filter(
                share__id__contains=id).order_by('-bid_price')
            return queryset
        else:
            return Bid.objects.none()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (TokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    @action(methods=['POST'], detail=True)
    def execute_order(self, request):
        if request.method == 'POST':
            if form.is_valid():
                if "buyorder" in request.data:
                    order = Bid(
                        user=request.user, share=request.data['share'], bid_price=request.data['bid_price'], quantity=request.data['quantity'])
                    if validate_order(order):
                        asks = Ask.objects.filter(
                            share__share_name__contains=share, ask_price=order.bid_price)
                        asks.order_by('created_at')
                        trades = matching_engine(asks, 'buy', order)
                        response = {'message': 'Order placed successfully'}
                        return Response(response, status=status.HTTP_200_OK)
                    else:
                        response = {'message': 'Order quantity not valid'}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)

                elif "sellorder" in request.data:
                    order = Ask(
                        user=request.user, share=request.data['share'], ask_price=request.data['ask_price'], quantity=request.data['quantity'])
                    if validate_order(order):
                        bids = Bid.objects.filter(
                            share__share_name__contains=share, bid_price=order.ask_price)
                        trades = matching_engine(bids, 'sell', order)
                        response = {'message': 'Order placed successfully'}
                        return Response(response, status=status.HTTP_200_OK)
                    else:
                        response = {'message': 'Order quantity not valid'}
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class OrderQViewSet(viewsets.ModelViewSet):
    queryset = OrderQ.objects.all()
    serializer_class = OrderQSerializer
    permission_classes = (AllowAny,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
