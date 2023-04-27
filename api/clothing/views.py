"""
Clothing views.py
옷 데이터에 대한 CRUD 뷰

@author 최민수
@create 2023-04-17
"""
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.clothing.serializers import ClothingSerializer
from api.clothing.serializers import ClothingCreateSerializer
from api.clothing.serializers import ClothingRetrieveSerializer
from api.clothing.serializers import ClothingUpdateSerializer
from api.clothing.serializers import ClothingTagUpdateSerializer
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
        if self.action in ["update", "partial_update"]:
            return ClothingUpdateSerializer
        if self.action == "multiple_tag_update":
            return ClothingTagUpdateSerializer

        return super().get_serializer_class()

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=["patch"], url_path="tag")
    def multiple_tag_update(self, request, *args, **kwargs):
        target_pk_list = [item["id"] for item in request.data]
        instance = self.get_queryset().filter(id__in=target_pk_list)
        serializer = self.get_serializer(
            instance, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
