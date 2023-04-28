"""
Clothing views.py
옷 데이터에 대한 CRUD 뷰

@author 최민수
@create 2023-04-17
"""
from rest_framework.viewsets import ModelViewSet

from api.clothing.serializers import ClothingSerializer
from api.clothing.serializers import ClothingCreateSerializer
from api.clothing.serializers import ClothingRetrieveSerializer
from model.clothing.models import Clothing


class ClothingViewSet(ModelViewSet):
    queryset = Clothing.active_objects.all()
    serializer_class = ClothingSerializer
    
    def get_serializer_class(self):
        if self.action == "create":
            return ClothingCreateSerializer
        if self.action == "retrieve":
            return ClothingRetrieveSerializer
        if self.action == "list":
            return ClothingRetrieveSerializer
        
        return super().get_serializer_class()
