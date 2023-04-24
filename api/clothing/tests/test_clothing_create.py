"""
Test clothing create
clothing create 기능 테스트 코드

@author 최민수
@create 2023-04-24
"""
import shutil

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lib.factory.factory_user import UserFactory
from lib.factory.file_mock import file_image
from model.clothing.models import Clothing

TEST_DIR = "test_src/clothing/create"


@override_settings(MEDIA_ROOT=TEST_DIR)
class ClothingCreateTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.current_user = UserFactory()
        cls.url = reverse("clothing-list")

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass

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

        clothing = Clothing.objects.get(id=res.data["id"])
        self.assertTrue(res.data["image"].endswith(clothing.image.name))

    def test_clothing_create_with_missing_data(self):
        """옷 생성 테스트(데이터 전체 누락)"""
        res = self.client.post(
            self.url,
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_clothing_create_with_empty_image(self):
        """옷 생성 테스트(빈 이미지)"""
        self.data["image"] = SimpleUploadedFile("empty.png", b"")
        res = self.client.post(
            self.url,
            self.data
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
