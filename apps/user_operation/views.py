from django.shortcuts import render
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication

from .models import UserFav
from .serializer import UserFavSerializer,UserFavDetailSerializer
from utils.permissions import IsOwnerOrReadOnly

class UserFavViewset(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet):
    """
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    """
    # 对用户进行权限验证，需要登录并且是当前用户
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    # token 认证
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication,)
    lookup_field = "goods_id"

    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return UserFavDetailSerializer
        if self.action == "create":
            return UserFavSerializer
        return UserFavSerializer



