from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from ..utils import can_modify_project
from .. import models



class CanModifyOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return True

        if view.kwargs.get("project_year"):
            project_year = get_object_or_404(models.ProjectYear, pk=view.kwargs.get("project_year"))
            return can_modify_project(request.user, project_year.project_id)

        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS and request.user.is_authenticated:
            return True
        if hasattr(obj, "project_id"):
            return can_modify_project(request.user, obj.project_id)
        elif hasattr(obj, "project_year"):
            return can_modify_project(request.user, obj.project_year.project_id)
        else:
            return can_modify_project(request.user, obj.id)


