from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav
from .serializer import UserFavSerializer
from utils.permissions import IsOwnerOrReadOnly

class UserFavViewset(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    用户收藏
    """
    # 对用户进行权限验证，需要登录并且是当前用户
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    serializer_class =UserFavSerializer
    # token 认证
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication,)

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)
