"""
Clothing serializers.py
옷 데이터에 대한 시리얼라이저

@author 최민수
@create 2023-04-17
"""
from rest_framework import serializers

from model.clothing.models import Clothing


class ClothingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothing
        fields = ["id", "user", "image", "created"]