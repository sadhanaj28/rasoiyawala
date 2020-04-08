import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from ..models import Location
from ..serializers import LocationSerializer

class CookImageViewTest(TestCase):
    pass