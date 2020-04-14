import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import CookProfileImage, UserDetails
from ..serializers import CookProfileImageSerializer


class CookImageViewTest(APITestCase):
    def setUp(self) -> None:
        self.valid_payload = {
            'cook_id': 1,
            'profile_pic': 'tony.jpg'
        }
        self.invalid_payload = {
            'cook_id': 0,
            'profile_pic': ''
        }
        self.url = reverse('image')

    def test_create_valid_image(self):
        response = self.client.post(self.url,
                                    data=json.dumps(self.valid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invalid_image(self):
        response = self.client.post(self.url,
                                    data=json.dumps(self.invalid_payload),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
