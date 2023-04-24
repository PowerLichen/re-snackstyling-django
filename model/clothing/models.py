"""
Django model - Clothing
옷 데이터 모델

@author 최민수
@create 2023-04-17
"""
from django.conf import settings
from django.db import models
from django_extensions.db.models import TimeStampedModel

from model.managers import ActiveManager


class Clothing(TimeStampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clothing_set"
    )
    image = models.ImageField(
        "clothing image",
        upload_to="clothing/%Y/%m/%d/"
    )
    tags = models.ManyToManyField("clothing_tag.ClothingTag")
    is_active = models.BooleanField(default=True)
    
    objects = models.Manager()
    active_objects = ActiveManager()
    
    class Meta:
        db_table = "clothing"
        ordering = ["-created",]
    