from rest_framework import serializers
from django.db.models import Q
from .models import Goods, GoodsCategory, GoodsImage, Banner, GoodsCategoryBrand, IndexAd

class CategorySerializer3(serializers.ModelSerializer):
    class Meta:
        model = GoodsCategory
        fields = "__all__"

class CategorySerializer2(serializers.ModelSerializer):
    sub_cat = CategorySerializer3(many=True)
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
        fields = ("image",)



class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    image = GoodsImageSerializer(many=True)
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
    sub_cat = CategorySerializer2(many=True)
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id, )
        if ad_goods:
            good_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        # ad_goods 只给前端返回id及第一个image，不需要全部返回
        goods_return = {}
        goods_return["id"] = goods_json["id"]
        goods_return["image"] = goods_json["image"][0]
        return goods_return



    def get_goods(self, obj):
        all_goods = Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|Q(category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = "__all__"

