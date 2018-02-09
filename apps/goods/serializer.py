from rest_framework import serializers
from .models import Goods,GoodsCategory,GoodsImage


# class GoodsSerialize(serializers.Serializer):
#     name = serializers.CharField(required=True,max_length=100)
#     shop_price = serializers.IntegerField()
#     goods_font_image = serializers.ImageField()

# ModelSerializer 的嵌套使用
class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True) #sub_cat 是我们自关联的related_name
    class Meta:
        model = GoodsCategory
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    sub_cat = CategorySerializer2(many=True)
    class Meta:
        model = GoodsCategory
        fields = "__all__"




class GoodsSerialize(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Goods
        fields = "__all__"
        # depth = 2

