"""
Django model managers
장고 매니저 활용을 위한 기본 정의

@author 최민수
@create 2023-04-17
"""
from django.db import models


class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)
