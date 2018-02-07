from django.views.generic.base import View
from .models import Goods
from django.shortcuts import HttpResponse
import json

class GoodsListView(View):
    def get(self,request):
        # 原始方法
        # goods_list = []
        # goods = Goods.objects.all()[:10]
        # for good in goods:
        #     goods_detail = {}
        #     goods_detail["name"] = good.name
        #     goods_detail["category"] = good.category.name
        #     goods_detail["shop_price"] = good.shop_price
        #     goods_list.append(goods_detail)
        # return HttpResponse(json.dumps(goods_list),content_type="application/json")

        # 利用Django的serializers进行序列化
        goods = Goods.objects.all()[:10]
        from django.core import serializers
        json_data = serializers.serialize("json",goods)
        json_data = json.loads(json_data)
        from django.http import JsonResponse
        return JsonResponse(json_data,safe=False)


