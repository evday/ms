from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


from utils.permissions import IsOwnerOrReadOnly
from .serializer import ShoppingCarSerializer,ShoppingCarDetailSerializer
from .models import ShoppingCart

class ShoppingCarViewset(viewsets.ModelViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create：
        加入购物车
    delete：
        删除购物记录
    """
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)
    serializer_class = ShoppingCarSerializer
    lookup_field = "goods_id" # 传递商品id 做删除和修改操作
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCarDetailSerializer
        else:
            return ShoppingCarSerializer