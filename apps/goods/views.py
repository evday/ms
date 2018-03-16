from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import  TokenAuthentication
from rest_framework import serializers


from .filters import GoodsFilter

class GoodsPagination(PageNumberPagination):
    page_size = 12
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = "page"


from .models import Goods,GoodsCategory,Banner
from .serializer import GoodsSerialize,CategorySerializer,BannerSerializer,IndexCategorySerializer

# class GoodsListView(APIView):
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:10]
#         serializer = GoodsSerialize(goods, many=True)
#
#         return Response(serializer.data)
class GoodsListSetView(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    商品列表页,分页，搜索，过滤，排序
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerialize
    pagination_class = GoodsPagination
    # authentication_classes = (TokenAuthentication,)
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter)
    filter_class = GoodsFilter
    search_fields = ('name', 'goods_brief','goods_desc')
    ordering_fields = ('sold_num','shop_price')

    def retrieve(self, request, *args, **kwargs):
        '''重写retrieve方法，点击数加一操作'''
        instance = self.get_object()
        instance.click_num += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

#RetrieveModelMixin 获取某一条商品详情
class CategoryViewset(mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class BannerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    获取轮播图列表
    """
    queryset = Banner.objects.all().order_by("index")
    serializer_class = BannerSerializer


class IndexCategoryViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    """
    首页商品分类数据
    """
    queryset = GoodsCategory.objects.filter(is_tab=True,name__in=["生鲜食品","酒水饮料"])
    serializer_class = IndexCategorySerializer