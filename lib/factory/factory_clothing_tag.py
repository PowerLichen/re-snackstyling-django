import factory

from model.clothing_tag.models import ClothingTag


class ClothingTagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ClothingTag
        django_get_or_create = ("name",)
    
    type = "TAG"
    name = factory.Faker("word")
