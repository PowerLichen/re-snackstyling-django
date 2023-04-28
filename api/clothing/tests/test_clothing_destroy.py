"""
Test clothing destroy
clothing destroy 기능 테스트 코드

@author 최민수
@create 2023-04-26
"""
import shutil

from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lib.factory.factory_clothing import ClothingFactory
from lib.factory.factory_clothing_tag import ClothingTagFactory
from lib.factory.factory_user import UserFactory
from model.clothing.models import Clothing

TEST_DIR = "test_src/clothing/destroy"


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class ClothingDestroyTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.current_user = UserFactory()
        cls.clothing_tag_set = ClothingTagFactory.create_batch(3)
        cls.clothing = ClothingFactory(
            user=cls.current_user,
            tags=cls.clothing_tag_set
        )

        cls.url = reverse(
            "clothing-detail",
            kwargs={"pk": cls.clothing.id}
        )

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass

    def setUp(self):
        self.client.force_authenticate(user=self.current_user)

    def test_clothing_destroy_success(self):
        """옷 삭제 성공 테스트"""
        res = self.client.delete(
            self.url
        )
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.clothing.refresh_from_db()
        self.assertFalse(self.clothing.is_active)
        
    def test_clothing_destroy_wxith_invalid_pk(self):
        """옷 삭제 테스트(유효하지 않은 pk)"""
        res = self.client.get(
            reverse("clothing-detail", kwargs={"pk": 111111})
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        
