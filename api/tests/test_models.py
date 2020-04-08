from django.test import TestCase

from ..models import Location, CookProfileImage, UserDetails


class CookAgreementTest(TestCase):
    def setUp(self):
        Location.objects.create(city='test_city_1', area='btm_test')
        Location.objects.create(city='test_city_2', area='jp_test')

    def test_cook_agreement(self):
        cook_agr1 = Location.objects.get(id=1)
        cook_agr2 = Location.objects.get(id=2)
        self.assertEqual(cook_agr1.city, "test_city_1")
        self.assertEqual(cook_agr2.city, "test_city_2")


class CookProfileImageTest(TestCase):
    def setUp(self):
        UserDetails.objects.create(name="test_cook", type='Cook', gender='Female', pan_card="GFFDRE45", profile_pic="",
                                   contact_number_one=9876543212, contact_number_two=9876545678,
                                   descriptions="hello test address",
                                   is_access_granted="Yes")
        cook = UserDetails.objects.get(pan_card="GFFDRE45")
        CookProfileImage.objects.create(cook_id=cook.id, profile_pic='helll.jpg')

    def test_cook_profile_image(self):
        img = CookProfileImage.objects.get(id=1)
        self.assertEqual(img.profile_pic, "helll.jpg")
