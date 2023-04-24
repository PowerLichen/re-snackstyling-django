import factory

from model.clothing_tag.choices import CLOTHING_TYPE_CHOICES
from model.clothing_tag.models import ClothingTag


class ClothingTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClothingTag
        django_get_or_create = ("name",)
    
    type = "TAG"
    name = factory.Iterator(["봄", "여름", "가을", "겨울"])
