import sys
import os

path = os.path.dirname(os.path.realpath(__file__))#获取当前文件路径
sys.path.append(path+'../')#把当前项目加入到Python的根搜索路径
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MxShop.settings") #需要用到settings中的配置

import django
django.setup()# 有了这个函数之后就可以直接使用models了

from goods.models import Goods,GoodsImage,GoodsCategory #一定要写在这个位置，放在前面Django的环境还没有初始化完成
from db_tools.data.product_data import row_data

for goods_detail in row_data:
    goods = Goods()
    goods.name = goods_detail["name"]
    goods.market_price = float(int(goods_detail["market_price"].replace("￥","").replace("元","")))
    goods.shop_price = float(int(goods_detail["sale_price"].replace("￥","").replace("元","")))
    goods.goods_brief = goods_detail["desc"] if goods_detail["desc"] is not None else ""
    goods.goods_desc = goods_detail["goods_desc"] if goods_detail["goods_desc"] is not None else ""
    goods.goods_font_image = goods_detail["images"][0] if goods_detail["images"] else "" #轮播图取第一张

    category_name = goods_detail["categorys"][-1] # 这里只取最后一个(最细的分类)
    category = GoodsCategory.objects.filter(name = category_name)
    if category:
        goods.category = category[0]
    goods.save()

    for goods_image in goods_detail["images"]:
        goods_image_instance = GoodsImage()
        goods_image_instance.image = goods_image
        goods_image_instance.goods = goods
        goods_image_instance.save()