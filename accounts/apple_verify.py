# utils.py

from google.auth.transport import requests
from google.oauth2 import id_token
from django.conf import settings
import jwt
from rest_framework import serializers


def VerifyAppleToken(token):
    try:
        user_data = jwt.decode(token, options={"verify_signature": False})
        user_data["sub"]
    except Exception as e:
        raise serializers.ValidationError(
            "The token is invalid or expired. Please login again."
        )
    user_data = jwt.decode(token, options={"verify_signature": False})
    print(user_data, " apple login ")
    return user_data,True
