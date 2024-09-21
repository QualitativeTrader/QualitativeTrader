from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AccAuthTokenGen(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.is_auth)
        )
    
account_activation_token = AccAuthTokenGen()