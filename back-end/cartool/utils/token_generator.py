from datetime import datetime, time

from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.crypto import constant_time_compare
from django.utils.http import base36_to_int


class _OTPVerifyTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        hash_value = super()._make_hash_value(user, timestamp)
        return f'{hash_value}{user.is_active}'

    def check_token(self, user, token):
        """
        Check that a verify token is correct for a given user.
        """
        if not (user and token):
            return False
        # Parse the token
        try:
            ts_b36, _ = token.split("-")
            # RemovedInDjango40Warning.
            legacy_token = len(ts_b36) < 4
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if not constant_time_compare(self._make_token_with_timestamp(user, ts), token):
            # RemovedInDjango40Warning: when the deprecation ends, replace
            # with:
            #   return False
            if not constant_time_compare(
                    self._make_token_with_timestamp(user, ts, legacy=True),
                    token,
            ):
                return False

        # RemovedInDjango40Warning: convert days to seconds and round to
        # midnight (server time) for pre-Django 3.1 tokens.
        now = self._now()
        if legacy_token:
            ts *= 24 * 60 * 60
            ts += int((now - datetime.combine(now.date(), time.min)).total_seconds())
        # Check the timestamp is within limit.
        if (self._num_seconds(now) - ts) > settings.OPT_VERIFY_TIMEOUT:
            return False

        return True


OTPVerifyTokenGenerator = _OTPVerifyTokenGenerator()
