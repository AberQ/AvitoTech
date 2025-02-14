from django.core.exceptions import PermissionDenied
from django.db import connections
from django.http import Http404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission
from rest_framework import exceptions
from rest_framework.response import Response



def set_rollback():
    for db in connections.all():
        if db.settings_dict['ATOMIC_REQUESTS'] and db.in_atomic_block:
            db.set_rollback(True)

def custom_exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound(*(exc.args))
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied(*(exc.args))

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
