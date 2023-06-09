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

class ClothingCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Clothing
        fields = ["id", "user", "image"]
        
class ClothingRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.SerializerMethodField()
    tags = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Clothing
        fields = ["id", "user", "image", "category", "tags", "created"]
        
    def get_category(self, obj):
        return obj.tags.filter(type="CTG").values_list("name", flat=True)
    
class ClothingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clothing
        fields = ["image", "tags"]
    
