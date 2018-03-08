from rest_framework import serializers

from .models import Goods,ShoppingCart


class ShoppingCarSerializer(serializers.Serializer):

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

