from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = "p"


from .models import Goods
from .serializer import GoodsSerialize

# class GoodsListView(APIView):
#     def get(self, request, format=None):
#         goods = Goods.objects.all()[:10]
#         serializer = GoodsSerialize(goods, many=True)
#
#         return Response(serializer.data)
class GoodsListView(generics.ListAPIView):
    '''
    商品列表页
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerialize
    pagination_class = GoodsPagination