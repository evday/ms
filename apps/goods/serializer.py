from rest_framework import serializers
from .models import Goods,GoodsCategory,GoodsImage,Banner


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


class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsImage
        fields = ("image", )

class GoodsSerialize(serializers.ModelSerializer):
    category = CategorySerializer()
    # 这个images是model表中的related_name
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = Goods
        fields = "__all__"

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = "__all__"
