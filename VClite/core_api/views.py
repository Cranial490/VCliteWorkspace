from django.shortcuts import render
from django import forms

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework import parsers, renderers, status
# from rest_framework.decorators import api_view

from rest_framework.views import APIView
from django_rest_passwordreset.signals import reset_password_token_created
from django_rest_passwordreset.models import ResetPasswordToken
from django_rest_passwordreset.views import get_password_reset_token_expiry_time

from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.dispatch import receiver
from django.shortcuts import reverse

from .serializers import *
from .models import *
from rest_framework.response import Response
from core_api.utils import validate_order
from core_api.matching import matching_engine

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import GenericAPIView, UpdateAPIView
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


class CustomPasswordResetView:
    @receiver(reset_password_token_created)
    def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
        print("request finished")
        site_full_name = 'VClite'
        site_url = settings.SITE_URL#'http://localhost:8080'
        site_shortcut_name = 'VClite'
        frontend_url = settings.SITE_URL + reverse('reset-request', kwargs={'username': reset_password_token.user.username, 'validation_key': reset_password_token.key})
        context = {
            'current_user': reset_password_token.user,
            'username': reset_password_token.user.username,
            'email': reset_password_token.user.email,
            #'reset_password_url': "{}/changePassword/{}/{}".format('http://127.0.0.1:8000/auth', reset_password_token.user.username, reset_password_token.key),
            'reset_password_url': frontend_url,
            'site_name': site_shortcut_name,
            'site_domain': site_url
        }
        email_html_message = render_to_string('email/user_reset_password.html', context)
        email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

        msg = EmailMultiAlternatives(
            # title:
            "Password Reset for {}".format(site_full_name),
            # message:
            email_plaintext_message,
            # from:
            "noreply@{}".format(site_full_name),
            # to:
            [reset_password_token.user.email]
        )
        msg.attach_alternative(email_html_message, "text/html")
        msg.send()
        #send_mail('Forgot Password', 'Go to this page to reset ur password', settings.EMAIL_HOST_USER, [reset_password_token.user.email], fail_silently=False)

'''
def isEmailValid(email):
    if(VC_T_User.objects.filter(email = email).exists()):
        return True

def isPanNoValid(email, pan_no):
    user = VC_T_User.objects.filter(email = email)
    if(user.objects.filter(pan_no = pan_no).exists()):
        return True
'''

class ResetPassword(APIView):
    """View for entering and re-entering a new password. """
    permission_classes = [AllowAny]
    authentication_classes = []

    #@ action(methods=['POST'], detail=False)
    #def save_updated_password(self, request, *args, **kwargs):
    def post(self, request, *args, **kwargs):
        user = VC_T_User.objects.get(username=kwargs.get('username'))
        password = request.data['password']
        if password is None:
            response = {'message': 'Empty Password passed'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.send_reset_password_success_email('Password successfully changed', 'user_reset_password_success', 'user_reset_password_success')
        response = {'message': 'Password Updated Successfully'}
        return Response(response, status=status.HTTP_200_OK)


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
    #permission_classes = (AllowAny,)
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        id = self.request.query_params.get('share_id')
        if(id is not None):
            queryset = VC_T_Ask.objects.filter(
                share__id__contains=id).order_by('ask_price')
            return queryset
        else:
            return VC_T_Ask.objects.none()


class BidViewSet(viewsets.ModelViewSet):
    queryset = VC_T_Bid.objects.all()
    serializer_class = BidSerializer
    #permission_classes = (AllowAny,)
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated,)

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


def isLoggedUser(request):
    if(str(request.user.id) == str(request.data['id'])):
        print("vlaidated2")
        return True
    else:
        return False


def user_data_valid(request):
    if(userExists(request.user) and isLoggedUser(request)):
        if (stringValid(request.data['username']) and
            stringValid(request.data['phone_no']) and
            stringValid(request.data['dpid']) and
                stringValid(request.data['pan_no'])):
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


class OrderQViewSet(viewsets.ModelViewSet):
    queryset = VC_T_Order_Queue.objects.all()
    serializer_class = OrderQSerializer
    permission_classes = (AllowAny,)


def order_valid(request):
    orderData = VC_T_Order.objects.filter(id__iexact=request.data['id'])
    if orderData.count() > 0:
        return orderData
    else:
        return None


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
            quantity=parentOrder.updated_quantity
        )
    # order.save()
    return parentOrder, order


class OrderViewSet(viewsets.ModelViewSet):
    queryset = VC_T_Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        userId = self.request.user.id
        print(self.request.user)
        if(userId != None):
            queryset = VC_T_Order.objects.filter(user__id__iexact=userId)
            return queryset
        else:
            return VC_T_User.objects.none()

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
        if request.method == 'POST':
            order = order_valid(request)[0]
            if order != None:
                order.order_status = "CANCELLED"
                order.save()
                print(order)
                if order.order_type == "BUY":
                    relatedBid = VC_T_Bid.objects.filter(
                        parent_order__id__iexact=order.id)[0]
                    print(relatedBid)
                    relatedBid.delete()
                elif order.order_type == "SELL":
                    relatedAsk = VC_T_Ask.objects.filter(
                        parent_order__id__iexact=order.id)[0]
                    print(relatedAsk)
                    relatedAsk.delete()
                response = {'message': 'Order Cancelled'}
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {'message': 'Order Invalid'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = VC_T_User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        username = str(self.request.user.username)
        if(username is not None):
            queryset = VC_T_User.objects.filter(username=username)
            return queryset
        else:
            return VC_T_User.objects.none()
        

    @ action(methods=['POST'], detail=False, url_path='update')
    def update_user_details(self, request):
        print(request.user)
        if request.method == 'POST':
            if(user_data_valid(request)):
                logged_user = VC_T_User.objects.filter(
                    id__iexact=request.data['id'])[0]

                logged_user.email = request.data['email']
                logged_user.phone_no = request.data['phone_no']
                logged_user.dpid = request.data['dpid']
                logged_user.pan_no = request.data['pan_no']
                logged_user.save()
                response = {'message': 'Order placed successfully'}
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = {'message': 'Invalid data'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

def getEmail(request):
    if request.method == 'GET':
        print("request = {}".format(request))
        user = VC_T_User.objects.filter(username=request.data['username'])
        if user is None:
            response = {'message': 'User not found'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        response = {'email': user.email}
        return Response(response, status=status.HTTP_200_OK)




class UserPartialUpdateView(UpdateAPIView, UpdateModelMixin):
    '''
    You just need to provide the field which is to be modified.
    '''
    queryset = VC_T_User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'username'
    # if form.is_valid:
    #    form.save()

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = VC_T_User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)  # handle if directly accessed this link

    @action (methods=['POST'], detail=False, url_path='send_email')
    def send_email(self, request, *args, **kwargs):
        print("request = {}".format(request))
        Username = request.data['username']
        if Username is None:
            response = {'message': 'Invalid data'}
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        user = VC_T_User.objects.get(username=Username)
        context = {
            'url': settings.SITE_URL,
            'username': user
        }
        email_html_message = render_to_string('email/user_registration.html', context)
        email_plaintext_message = render_to_string('email/user_registration.txt', context)
        user.send_reset_password_success_email('Registered Successfully', 'user_registration', 'user_registration')
        response = {'message': 'Registration Successful'}
        return Response(response, status=status.HTTP_200_OK)
        
