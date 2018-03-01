from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # 如果用户请求在安全操作列表中就不做任何操作
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
