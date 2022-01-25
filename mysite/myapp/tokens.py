############################## generate token for email verifaction ###########################
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.utils.http import base36_to_int, int_to_base36
class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return ( six.text_type(user.pk)+six.text_type(timestamp)+ six.text_type(user.is_active))
    
     
    def check_token(self, user, token):
        """
        Check that a password reset token is correct for a given user.
        """
        if not (user and token):
            return False
        # Parse the token
        try:
            # ts_b36, _ = token.split("-")
            # RemovedInDjango40Warning.
            legacy_token = len(token) < 4
            # print(ts_b36)
            # print(_)
            print(legacy_token)
        except ValueError:
            return False

        try:
            ts = base36_to_int(token)
            print(ts)
        except ValueError:
            return False
    
account_activation_token = TokenGenerator()