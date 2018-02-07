from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Goods
from .serializer import GoodsSerialize

class GoodsListView(APIView):
    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        serializer = GoodsSerialize(goods, many=True)

        return Response(serializer.data)
