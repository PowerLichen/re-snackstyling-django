import shutil

from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lib.factory.factory_clothing import ClothingFactory
from lib.factory.factory_clothing_tag import ClothingTagFactory
from lib.factory.factory_user import UserFactory

TEST_DIR = "test_src/clothing/retrieve"


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class ClothingRetrieveTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.current_user = UserFactory()
        test_tags = ClothingTagFactory.create_batch(3)
        cls.clothing = ClothingFactory(
            user=cls.current_user,
            tags=test_tags
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
    
    def test_clothing_retrieve_success(self):
        """옷 단일 조회 성공 테스트"""
        res = self.client.get(
            self.url
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        self.assertIn("id", res.data)
        self.assertIn("user", res.data)
        self.assertIn("image", res.data)
        self.assertIn("created", res.data)
        self.assertIn("category", res.data)
        self.assertIn("tags", res.data)
        
        self.assertEqual(res.data["id"], self.clothing.id)
        self.assertEqual(res.data["user"], self.current_user.id)
        self.assertTrue(res.data["image"].endswith(self.clothing.image.name))
        self.assertEqual(len(res.data["category"]), 0)
        self.assertEqual(len(res.data["tags"]), len(self.clothing.tags.all()))
        for clothing_tag in self.clothing.tags.all():
            self.assertIn(clothing_tag.name, res.data["tags"])
            
        
    def test_clothing_retrieve_with_invalid_pk(self):
        """옷 단일 조회 테스트(유효하지 않은 pk)"""
        res = self.client.get(
            reverse("clothing-detail", kwargs={"pk": 111111})
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)