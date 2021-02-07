from django.db import models


USER_TYPE = (
        ('Cook', 'Cook'),
        ('Hire', 'Hire'),
    )

GENDER = (
        ('Female', 'Female'),
        ('Male', 'Male'),
    )

YES_NO = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )


# Create your models here.
class CookAgreement(models.Model):
    id = models.AutoField(primary_key=True)
    cook_id = models.IntegerField()
    is_access_granted = models.CharField(max_length=10, choices=YES_NO)

    class Meta:
        db_table = 'cook_agreements'


class UserDetails(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=10, choices=USER_TYPE)
    gender = models.CharField(max_length=10, choices=GENDER)
    pan_card = models.CharField(max_length=20, unique=True)
    profile_pic = models.CharField(max_length=200, blank=True, null=True)
    contact_number_one = models.CharField(max_length=10)
    contact_number_two = models.CharField(max_length=10, blank=True, null=True)
    descriptions = models.TextField(default=None)
    is_access_granted = models.CharField(max_length=10, choices=YES_NO, default='Yes')

    class Meta:
        db_table = 'user_details'


class CookProfileImage(models.Model):
    id = models.AutoField(primary_key=True)
    cook_id = models.IntegerField()
    profile_pic = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'cook_profile_image'


class Specility(models.Model):
    id = models.AutoField(primary_key=True)
    north_indian_food = models.CharField(max_length=10, choices=YES_NO)
    south_indian_food = models.CharField(max_length=10, choices=YES_NO)
    chinees_food = models.CharField(max_length=10, choices=YES_NO)
    other = models.CharField(max_length=500, blank=True, null=True)
    food_pic_one = models.CharField(max_length=200, blank=True, null=True)
    food_pic_two = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'specility'


class Location(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    area = models.CharField(max_length=200)

    class Meta:
        db_table = 'location'


class CookLocationMapping(models.Model):
    id = models.AutoField(primary_key=True)
    cook_id = models.IntegerField()
    location_id = models.IntegerField()

    class Meta:
        db_table = 'cook_location_mapping'


class CookSpecilityMapping(models.Model):
    id = models.AutoField(primary_key=True)
    cook_id = models.IntegerField()
    specility_id = models.IntegerField()

    class Meta:
        db_table = 'cook_specility_mapping'


class CookAddition(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    is_agree = models.BooleanField()
    is_new = models.BooleanField(default=True)
    class Meta:
        db_table = 'cook_addition'


class JobDetails(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    contact_number_one = models.CharField(max_length=10, default='0000000000')
    descriptions = models.TextField(default=None)

    class Meta:
        db_table = 'job_details'

class JobLocationMapping(models.Model):
    id = models.AutoField(primary_key=True)
    job_id = models.IntegerField()
    location_id = models.IntegerField()

    class Meta:
        db_table = 'job_location_mapping'
