import hashlib

from django.contrib.auth.tokens import PasswordResetTokenGenerator


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        hash_string = str(user.pk) + user.email + str(timestamp)
        return hashlib.sha1(hash_string.encode('utf-8')).hexdigest()

    def make_token(self, user):
        timestamp = self._num_seconds(self._now())
        return self._make_hash_value(user, timestamp)


email_verification_token = EmailVerificationTokenGenerator()
