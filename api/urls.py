from django.urls import include
from django.urls import path
from rest_framework import routers

from api.clothing import views

router = routers.DefaultRouter()
router.register(r"clothing", views.ClothingViewSet, basename="clothing")

urlpatterns = router.urls