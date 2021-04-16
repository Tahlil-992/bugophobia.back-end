from rest_framework import permissions
from django.shortcuts import get_object_or_404
from users.models import BaseUser


class IsDoctor(permissions.BasePermission):
    def has_permission(self, request, view):
        user = get_object_or_404(BaseUser, id=request.user.id)
        return user.is_doctor
