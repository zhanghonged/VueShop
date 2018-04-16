from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Goods
from .serializers import GoodsSerializer
# Create your views here.
class GoodsListView(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        goods = Goods.objects.all()[:10]
        goods_serializer = GoodsSerializer(goods, many=True)
        return Response(goods_serializer.data)