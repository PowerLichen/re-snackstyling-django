import factory
from django.contrib.auth import get_user_model

from model.clothing.models import Clothing

UserModel = get_user_model()


class ClothingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clothing
        
    user = factory.Iterator(UserModel.objects.all())
    image = factory.django.ImageField()
    
    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for tag in extracted:
                self.tags.add(tag)
