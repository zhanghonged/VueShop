"""VueShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import include, url
import xadmin
from VueShop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from goods.views import GoodsListViewset, CategoryViewset
from users.views import SmsCodeViewset, UserViewset
from user_operation.views import UserFavViewset, LeavingMessageViewset, AddressViewset
from trade.views import ShoppingCartViewset


router = DefaultRouter()
#配置Goods的url
router.register(r'goods', GoodsListViewset, base_name='goods')
#配置category的url
router.register(r'categorys', CategoryViewset, base_name='categorys')
#配置code的url
router.register(r'codes', SmsCodeViewset, base_name="codes")
#配置用户注册的url
router.register(r'users', UserViewset, base_name="users")
#用户留言url
router.register(r'messages', LeavingMessageViewset, base_name="messages")
#收货地址
router.register(r'address', AddressViewset, base_name="address")
#收藏
router.register(r'userfavs', UserFavViewset, base_name="userfavs")
#购物车
router.register(r'shopcarts',ShoppingCartViewset, base_name = "shopcarts")

urlpatterns = [
    url(r'xadmin/', xadmin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),
    url(r'^', include(router.urls)),
    #drf自带的token认证模式
    #url(r'^api-token-auth/', views.obtain_auth_token),
    #jwt的认证接口
    url(r'^login/', obtain_jwt_token),

    # 匹配后面一定不能加"$"符号
    url(r'docs/', include_docs_urls(title="API文档"))
]
