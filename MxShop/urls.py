"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
import xadmin
from MxShop.settings import MEDIA_ROOT
from django.views.static import serve
from goods.views import GoodsListSetView,CategoryViewset
from users.views import UserViewset
from user_operation.views import UserFavViewset
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

rooter = DefaultRouter()
#配置goods的url
rooter.register(r"goods",GoodsListSetView,base_name="goods")
#配置categorys的url
rooter.register(r"categorys",CategoryViewset,base_name="categorys")
#配置users的url
rooter.register(r"users",UserViewset,base_name="users")
#配置收藏的url
rooter.register(r"userfavs",UserFavViewset,base_name='userfavs')

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^media/(?P<path>.*)$',serve,{"document_root":MEDIA_ROOT}),#配置media 路径
    url(r'^api-auth/', include('rest_framework.urls')),

    url(r'^', include(rooter.urls)),
    url(r'^docs/', include_docs_urls(title="暮雪生鲜")),

    #drf自带的token认证模式
    url(r'^api-token-auth/', views.obtain_auth_token),

    # jwt的认证接口
    url(r'^login/', obtain_jwt_token),

]
