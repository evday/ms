from datetime import datetime

from django.conf import settings
from django.shortcuts import redirect

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import mixins
from  rest_framework.views import APIView
from rest_framework.response import Response

from utils.alipay import AliPay
from utils.permissions import IsOwnerOrReadOnly
from .serializer import ShoppingCarSerializer,ShoppingCarDetailSerializer,OrderSerializer,OrderDetailSerializer
from .models import ShoppingCart,OrderInfo,OrderGoods


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

    def perform_create(self, serializer):
        '''加入到购物车，库存数减一'''
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    def perform_destroy(self, instance):
        '''从购物车删除后，库存数加一'''
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def perform_update(self, serializer):
        """更新购物车中商品数量，库存数做相应改变"""
        existed_record = ShoppingCart.objects.get(id=serializer.id) # 获取现在的购物车对象
        existed_nums = existed_record.nums  # 获取现在的购物车商品数
        save_record = serializer.save() # 保存时的商品数
        nums = save_record.nums - existed_nums  # 这里肯能会是负数
        goods = save_record.goods
        goods.goods_num -= nums # 所以这里要用减号，如果nums是负数那么负负得正
        goods.save()
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ShoppingCarDetailSerializer
        else:
            return ShoppingCarSerializer


class OrderViewset(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create：
        新增订单
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return OrderDetailSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order

class AlipayView(APIView):

    def get(self, request):
        """
        处理支付宝返回的return_url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.GET.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign",None)

        alipay = AliPay(
            appid = "",
            app_notify_url = "http://127.0.0.1:8000/alipay/return/",
            app_private_key_path= settings.PRIVATE_KEY_PATH,
            alipay_public_key_path= settings.ALI_PUB_KEY_PATH,
            debug = True,
            return_url = "http://127.0.0.1:8000/alipay/return/",
        )

        verify_re = alipay.verify(processed_dict,sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no',None) # out_trade_no 支付宝的api
            trade_no = processed_dict.get('trade_no',None)
            trade_status = processed_dict.get('trade_status',None)

            existed_orders = OrderInfo.objects.filter(order_sn = order_sn)
            for existed_order in existed_orders:
                existed_order.pay_status = trade_status
                existed_order.trade_no = trade_no
                existed_order.pay_time = datetime.now()
                existed_order.save()

            response = redirect("index")
            response.set_cookie("nextPath","pay",max_age = 3)
            return response

        else:
            response = redirect("index")
            return response

    def post(self,request):
        """
        处理支付宝的notify_url
        :param request:
        :return:
        """
        processed_dict = {}
        for key, value in request.POST.items():
            processed_dict[key] = value

        sign = processed_dict.pop("sign", None)

        alipay = AliPay(
            appid = "",
            app_notify_url = "http://127.0.0.1:8000/alipay/return/",
            app_private_key_path= settings.PRIVATE_KEY_PATH,
            alipay_public_key_path= settings.ALI_PUB_KEY_PATH,
            debug = True,
            return_url = "http://127.0.0.1:8000/alipay/return/",
        )

        verify_re = alipay.verify(processed_dict,sign)

        if verify_re is True:
            order_sn = processed_dict.get('out_trade_no', None)  # out_trade_no 支付宝的api
            trade_no = processed_dict.get('trade_no', None)
            trade_status = processed_dict.get('trade_status', None)

            existed_orders = OrderInfo.objects.filter(order_sn=order_sn)
            for existed_order in existed_orders:
                order_goods = existed_order.goods.all() # 根据related_name goods 取到商品订单Queryset
                for order_good in order_goods: #销量加一
                    goods = order_good.goods
                    goods.sold_num += order_good.goods_num
                    goods.save()

                    existed_order.pay_status = trade_status
                    existed_order.trade_no = trade_no
                    existed_order.pay_time = datetime.now()
                    existed_order.save()
            return Response("success") # 返回状态，如果不返回支付宝会一直发起请求





