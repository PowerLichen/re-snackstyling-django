import shutil
import random

from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from lib.factory.factory_clothing import ClothingFactory
from lib.factory.factory_clothing_tag import ClothingTagFactory
from lib.factory.factory_user import UserFactory
from model.clothing.models import Clothing

TEST_DIR = "test_src/clothing/tag_update"


@override_settings(MEDIA_ROOT=(TEST_DIR + '/media'))
class ClothingDestroyTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.current_user = UserFactory()
        cls.clothing_tag_set = ClothingTagFactory.create_batch(10)
        cls.clothing_set = ClothingFactory.create_batch(
            size=3,
            user=cls.current_user,
            tags=cls.clothing_tag_set[:3]
        )

        cls.url = reverse("clothing-multiple-tag-update")

    @classmethod
    def tearDownClass(cls) -> None:
        try:
            shutil.rmtree(TEST_DIR)
        except OSError:
            pass

    def setUp(self):
        self.client.force_authenticate(user=self.current_user)
        self.data = list()
        for clothing in self.clothing_set:
            tag_data = {
                "id": clothing.id,
                "tags": [item.id for item in random.choices(self.clothing_tag_set, k=3)]
            }
            self.data.append(tag_data)

    def do_compare_request_data_and_model_data(self):
        # compare expected data with clothing model data
        for item in self.data:
            try:
                cur_instance = Clothing.objects.get(id=item["id"])
            except Clothing.DoesNotExist:
                continue

            model_tag_id_list = [tag.id for tag in cur_instance.tags.all()]
            self.assertCountEqual(
                model_tag_id_list,
                list(set(item["tags"]))
            )

    def test_clothing_tag_update_success(self):
        """옷 태그 다중 수정 성공"""
        res = self.client.patch(
            self.url,
            self.data,
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.do_compare_request_data_and_model_data()

    def test_clothing_tag_update_with_empty_data(self):
        """옷 태그 다중 수정 성공(데이터 누락)"""
        self.data = []
        res = self.client.patch(
            self.url,
            self.data,
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_clothing_tag_update_with_invalid_clothing_id(self):
        """옷 태그 다중 수정 성공(유효하지 않은 clothing 포함)"""
        self.data[0]["id"] = 111111
        res = self.client.patch(
            self.url,
            self.data,
            format="json"
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.do_compare_request_data_and_model_data()
