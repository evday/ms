from rest_framework import serializers
from .models import Goods,GoodsCategory


# class GoodsSerialize(serializers.Serializer):
#     name = serializers.CharField(required=True,max_length=100)
#     shop_price = serializers.IntegerField()
#     goods_font_image = serializers.ImageField()

# ModelSerializer 的嵌套使用
class GoodsCategorySerialize(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class GoodsSerialize(serializers.ModelSerializer):
    # category = GoodsCategorySerialize()
    class Meta:
        model = Goods
        fields = "__all__"
        depth = 2
        