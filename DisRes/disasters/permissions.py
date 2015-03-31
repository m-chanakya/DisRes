from rest_framework import permissions
from profiles.models import Organisation
from django.contrib.auth.models import User

class IsOwnerSelf(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user