from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
import jwt
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from authentication.models import User

class JWTAuthentication(BaseAuthentication):

    def __init__(self, **kwargs):
        self.keyword = kwargs.get('keyword', 'Bearer')

        if not settings.SECRET_KEY:
            raise ImproperlyConfigured('JWTAuthentication requires SECRET_KEY to be set.')

    def authenticate(self, request):
        auth_header = get_authorization_header(request)

        if not auth_header:
            return None

        prefix, token = auth_header.decode('utf-8').split(' ', 1)
        if prefix.lower() != self.keyword.lower():
            raise exceptions.AuthenticationFailed('Invalid authentication header. Use Bearer.')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            username = payload['username']
            user = User.objects.get(username=username)
            return (user, token)

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token is expired. Login again.')

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed('Token is invalid.')

        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No user found for this token.')

