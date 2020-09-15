# -*- coding: utf-8 -*-
from __future__ import absolute_import

# Third Party Stuff
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client as TwilioRestClient

# Local
from .base import BaseBackend
from phone_verify.models import SMSVerification


class TwilioBackend(BaseBackend):
    def __init__(self, **options):
        super(TwilioBackend, self).__init__(**options)
        # Lower case it just to be sure
        options = {key.lower(): value for key, value in options.items()}
        self._sid = options.get("sid", None)
        self._secret = options.get("secret", None)  # auth_token
        self._from = options.get("from", None)

        self.client = TwilioRestClient(self._sid, self._secret)
        self.exception_class = TwilioRestException

    def send_sms(self, number, message):
        self.client.messages.create(to=number, body=message, from_=self._from)

    def send_bulk_sms(self, numbers, message):
        for number in numbers:
            self.send_sms(number=number, message=message)


class TwilioSandboxBackend(BaseBackend):
    def __init__(self, **options):
        super(TwilioSandboxBackend, self).__init__(**options)
        # Lower case it just to be sure
        options = {key.lower(): value for key, value in options.items()}
        print("options = {}".format(options))
        self._sid = options.get("sid", None)
        self._secret = options.get("secret", None)  # auth_token
        self._from = options.get("from", None)
        self._token = options.get("sandbox_token")

        self.client = TwilioRestClient(self._sid, self._secret)
        self.exception_class = TwilioRestException

    def send_sms(self, number, message):
        self.client.messages.create(to=number, body=message, from_=self._from)

    def send_bulk_sms(self, numbers, message):
        for number in numbers:
            self.send_sms(number=number, message=message)

    def generate_security_code(self):
        """
        Returns a fixed security code
        """
        return self._token

    def validate_security_code(self, security_code, phone_number, session_token):

        stored_verification = SMSVerification.objects.filter(
            security_code=security_code, phone_number=phone_number
        ).first()
        
        # check security_code exists
        if stored_verification is None:
            return stored_verification, self.SECURITY_CODE_INVALID

        # check session code exists
        if not stored_verification.session_token == session_token:
            return stored_verification, self.SESSION_TOKEN_INVALID

        # check security_code is not expired
        if self.check_security_code_expiry(stored_verification):
            return stored_verification, self.SECURITY_CODE_EXPIRED

        # check security_code is not verified
        if stored_verification.is_verified and django_settings.PHONE_VERIFICATION.get(
            "VERIFY_SECURITY_CODE_ONLY_ONCE"
        ):
            return stored_verification, self.SECURITY_CODE_VERIFIED

        # mark security_code as verified
        stored_verification.is_verified = True
        stored_verification.save()

        return stored_verification, self.SECURITY_CODE_VALID
        '''
        if security_code == '771183':
            return SMSVerification.objects.none(), self.SECURITY_CODE_VALID
        else:
            return SMSVerification.objects.none(), self.SECURITY_CODE_INVALID
        '''
