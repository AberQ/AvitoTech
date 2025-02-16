from django.core.exceptions import PermissionDenied
from django.db import connections
from django.http import Http404
from rest_framework import exceptions
from rest_framework.exceptions import AuthenticationFailed, NotAuthenticated
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken


def set_rollback():
    for db in connections.all():
        if db.settings_dict['ATOMIC_REQUESTS'] and db.in_atomic_block:
            db.set_rollback(True)

def custom_exception_handler(exc, context):
    """
    Кастомный обработчик исключений.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound(*(exc.args))
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied(*(exc.args))

    # Обрабатываем ошибку неверного или просроченного токена
    if isinstance(exc, (InvalidToken, AuthenticationFailed, NotAuthenticated)):
        return Response({"description": "Неавторизован"}, status=401)

    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = {'description': exc.detail}

        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)

    return None

class IsAuthenticatedCustom(BasePermission):
    """Кастомное разрешение, которое выбрасывает AuthenticationFailed с уникальным описанием"""
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise AuthenticationFailed("Неавторизован")
        return True
