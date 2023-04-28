"""
Test clothing list
clothing list 기능 테스트 코드

@author 최민수
@create 2023-04-25
"""
import shutil
import random

from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lib.factory.factory_clothing import ClothingFactory
from lib.factory.factory_clothing_tag import ClothingTagFactory
from lib.factory.factory_user import UserFactory

TEST_DIR = "test_src/clothing/list"


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class ClothingListTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.current_user = UserFactory()
        
        cls.clothing_set = dict()
        cls.clothing_size = 10
        
        # create clothing tag using factory
        normal_tags = ClothingTagFactory.create_batch(10)
        category_tags = ClothingTagFactory.create_batch(3, type="CTG")
        
        # create clothing using factory with random tag
        for _ in range(cls.clothing_size):
            test_tag_set = [random.choice(category_tags)] + random.choices(normal_tags, k=3)
            clothing = ClothingFactory(
                user=cls.current_user,
                tags=test_tag_set
            )
            cls.clothing_set[clothing.id] = clothing
        
        cls.url = reverse("clothing-list")
        
    @classmethod
    def tearDownClass(cls) -> None:
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass
    
    def setUp(self):
        self.client.force_authenticate(user=self.current_user)
    
    def test_clothing_list_success(self):
        """옷 목록 조회 성공 테스트"""
        res = self.client.get(
            self.url
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), self.clothing_size)
        
        for data in res.data:
            self.assertIn(data["id"], self.clothing_set)
            
            current_clothing_obj = self.clothing_set[data["id"]]
            self.assertEqual(data["user"], self.current_user.id)
            self.assertTrue(data["image"].endswith(current_clothing_obj.image.name))
            self.assertEqual(
                len(data["category"]),
                len(current_clothing_obj.tags.filter(type="CTG"))
            )
            self.assertEqual(
                len(data["tags"]),
                len(current_clothing_obj.tags.all())
            )
