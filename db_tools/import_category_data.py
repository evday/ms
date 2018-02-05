# -*- coding:utf-8 -*-

#独立使用django的model
import sys
import os

path = os.path.dirname(os.path.realpath(__file__))#获取当前文件路径
sys.path.append(path+'../')#把当前项目加入到Python的根搜索路径
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MxShop.settings") #需要用到settings中的配置

import django
django.setup()# 有了这个函数之后就可以直接使用models了

from goods.models import GoodsCategory #一定要写在这个位置，放在前面Django的环境还没有初始化完成
from db_tools.data.category_data import row_data

for lev1_cat in row_data:
    lev1_instance = GoodsCategory()
    lev1_instance.code = lev1_cat["code"]
    lev1_instance.name = lev1_cat["name"]
    lev1_instance.category_type = 1
    lev1_instance.save()

    for lev2_cat in lev1_cat["sub_categorys"]:
        lev2_instance = GoodsCategory()
        lev2_instance.code = lev2_cat["code"]
        lev2_instance.name = lev2_cat["name"]
        lev2_instance.category_type = 2
        lev2_instance.parent_category = lev1_instance #自关联
        lev2_instance.save()

        for lev3_cat in lev2_cat["sub_categorys"]:
            lev3_instance = GoodsCategory()
            lev3_instance.code = lev3_cat["code"]
            lev3_instance.name = lev3_cat["name"]
            lev3_instance.category_type = 3
            lev3_instance.parent_category = lev2_instance #自关联
            lev3_instance.save()


