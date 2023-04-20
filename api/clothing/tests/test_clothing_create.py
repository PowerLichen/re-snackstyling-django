from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lib.factory.factory_user import UserFactory
from lib.factory.file_mock import file_image


class ClothingCreateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.current_user = UserFactory()
        cls.url = reverse("clothing-list")
        
        
    def setUp(self):
        self.data = {
            "image": file_image()
        }
        self.client.force_authenticate(user=self.current_user)
        
    def test_clothing_create_success(self):
        """옷 생성 성공 테스트"""
        res = self.client.post(
            self.url,
            self.data
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        