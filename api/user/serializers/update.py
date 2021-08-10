import hashlib
import random

import jwt
import requests
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken

from api.logger.models import PhoneLog, EmailLog
from api.user.models import User, EmailVerifier, PhoneVerifier, Social, SocialKindChoices
from api.user.validators import validate_password
