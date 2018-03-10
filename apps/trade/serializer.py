import time

from rest_framework import serializers

from .models import Goods,ShoppingCart,OrderInfo,OrderGoods
from goods.serializer import GoodsSerialize


class ShoppingCarDetailSerializer(serializers.ModelSerializer):
    """购物车详情"""
    goods = GoodsSerialize(many=False,read_only=True)
    class Meta:
        model = ShoppingCart
        fields = ("goods","nums")

class ShoppingCarSerializer(serializers.Serializer):
    """购物车"""
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    nums = serializers.IntegerField(min_value=1,label="数量",required=True,
                                    error_messages={
                                        "required":"请选择购买数量",
                                        "min_value":"购买商品不能小于一"
                                    })
    # 外键字段
    goods = serializers.PrimaryKeyRelatedField(required=True,queryset=Goods.objects.all())

    def create(self,validated_data):
        # 序列化中 可以从上下文中获取request请求对象
        user = self.context["request"].user
        nums = validated_data["nums"]
        goods = validated_data["goods"]

        # 查看购物车中此商品是否存在
        existed = ShoppingCart.objects.filter(user=user,goods=goods)
        # 如果存在则将数量增加
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()

        else:
            existed = ShoppingCart.objects.create(**validated_data)

        return existed

    def update(self, instance, validated_data):
        """修改商品数量"""
        instance.nums = validated_data["nums"]
        instance.save()
        return instance

class OrderGoodsSerializer(serializers.ModelSerializer):
    goods = GoodsSerialize(many=False)
    class Meta:
        model = OrderGoods
        fields = "__all__"

class OrderDetailSerializer(serializers.ModelSerializer):
    goods = OrderGoodsSerializer(many=True)
    class Meta:
        model = OrderInfo
        fields = "__all__"



class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    def generate_order_sn(self):
        #当前时间+uid+随机数 生成订单号
        from random import Random
        random_ins = Random()
        order_sn = "{time_str}{userid}{ranstr}".format(time_str=time.strftime("%Y%m%m%H%M%S"),
                                                       userid=self.context["request"].user.id,
                                                       ranstr = random_ins.randint(10,99))
        return order_sn

    def validate(self,attrs):
        attrs["order_sn"] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = "__all__"
