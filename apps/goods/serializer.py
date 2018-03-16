from django.db.models import Q
from rest_framework import serializers
from .models import Goods,GoodsCategory,GoodsImage,Banner,GoodsCategoryBrand,IndexAd


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

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategoryBrand
        fields = "__all__"

class IndexCategorySerializer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    goods = serializers.SerializerMethodField()
    sub_cat = CategorySerializer2(many=True) #二级分类
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self,obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            good_ins = ad_goods[0].goods
            goods_json = GoodsSerialize(good_ins,many=False,context={"request":self.context["request"]}).data
        return goods_json

    def get_goods(self,obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id = obj.id)|Q(category__parent_category__parent_category_id = obj.id))
        goods_serializer = GoodsSerialize(all_goods,many=True,context={"request":self.context["request"]})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"