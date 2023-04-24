"""
Django model - Category
카테고리 데이터 모델

@author 최민수
@create 2023-04-24
"""
from django.db import models

from model.clothing_tag.choices import CLOTHING_TYPE_CHOICES


class ClothingTag(models.Model):    
    type = models.CharField(
        max_length=3,
        choices=CLOTHING_TYPE_CHOICES
    )
    name = models.CharField(max_length=60)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "clothing_tag"
