"""
Test clothing update
clothing update 기능 테스트 코드

@author 최민수
@create 2023-04-24
"""
import shutil

from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lib.factory.factory_clothing import ClothingFactory
from lib.factory.factory_clothing_tag import ClothingTagFactory
from lib.factory.factory_user import UserFactory
from lib.factory.file_mock import file_image

TEST_DIR = "test_src/clothing/update"


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class ClothingUpdateTestCase(APITestCase):
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
        self.data = {
            "tags": [self.clothing_tag_set[0].id]
        }
        self.client.force_authenticate(user=self.current_user)

    def test_clothing_update_success(self):
        """옷 수정 성공 테스트"""
        after_image_name = "test_patch_success.png"
        self.data["image"] = file_image(filename=after_image_name)

        res = self.client.patch(
            self.url,
            self.data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data["image"].endswith(after_image_name))
        self.assertEqual(len(res.data["tags"]), len(self.data["tags"]))
        self.assertCountEqual(res.data["tags"], self.data["tags"])

    def test_clothing_update_missing_data(self):
        """옷 수정 성공 테스트(데이터 누락)"""
        res = self.client.patch(
            self.url,
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data["image"].endswith(self.clothing.image.name))
        self.assertCountEqual(
            res.data["tags"],
            [item.id for item in self.clothing_tag_set]
        )

    def test_clothing_update_only_with_image(self):
        """옷 수정 성공 테스트(image 필드만 수정)"""
        after_image_name = "test_only_image.png"
        request_data = {
            "image": file_image(filename=after_image_name)
        }

        res = self.client.patch(
            self.url,
            request_data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data["image"].endswith(after_image_name))
        self.assertCountEqual(
            res.data["tags"],
            [item.id for item in self.clothing_tag_set]
        )

    def test_clothing_update_only_with_tags(self):
        """옷 수정 성공 테스트(tags 필드만 수정)"""
        res = self.client.patch(
            self.url,
            self.data
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data["image"].endswith(self.clothing.image.name))
        self.assertCountEqual(
            res.data["tags"],
            self.data["tags"]
        )

    def test_clothing_update_with_invalid_pk(self):
        """옷 수정 테스트(유효하지 않은 pk)"""
        res = self.client.get(
            reverse("clothing-detail", kwargs={"pk": 111111}),
            self.data
        )
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
