from rest_framework import serializers
from .models import CookAddition, \
                    CookSpecilityMapping, \
                    CookLocationMapping, \
                    CookAgreement, \
                    Location, \
                    Specility, \
                    UserDetails, \
                    CookProfileImage, \
                    JobLocationMapping, \
                    JobDetails, \
                    User, \
                    UserCookMapping, \
                    UserJobMapping


# serializer the request/response
class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserDetails
        fields = ('id', 'name', 'type', 'gender', 'pan_card', 'profile_pic',
                  'contact_number_one', 'contact_number_two', 'descriptions', 'is_access_granted')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'area')


class CookLocationMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookLocationMapping
        fields = ('id', 'cook_id', 'location_id')


class SpecilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specility
        fields = ('id', 'north_indian_food', 'south_indian_food', 'chinees_food')


class CookSpecilityMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookSpecilityMapping
        fields = ('id', 'cook_id', 'specility_id')


class CookProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CookProfileImage
        fields = ('id', 'cook_id', 'profile_pic')


class CookListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=200)
    type = serializers.CharField(max_length=1)
    gender = serializers.CharField(max_length=1)
    pan_card = serializers.CharField(max_length=20)
    profile_pic = serializers.CharField(max_length=200)
    contact_number_one = serializers.CharField(max_length=10)
    contact_number_two = serializers.CharField(max_length=10)
    city = serializers.CharField(max_length=200)
    area = serializers.CharField(max_length=200)
    north_indian_food = serializers.CharField(max_length=1)
    south_indian_food = serializers.CharField(max_length=1)
    chinees_food = serializers.CharField(max_length=1)
    other = serializers.CharField(max_length=500)
    food_pic_one = serializers.CharField(max_length=200)
    food_pic_two = serializers.CharField(max_length=200)


class CookAdditionSerializer(serializers.Serializer):
    pass


class CookSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField()
    specification = serializers.SerializerMethodField()

    class Meta:
        model = UserDetails
        fields = ('id', 'name', 'type', 'gender', 'pan_card', 'profile_pic',
                  'contact_number_one', 'contact_number_two', 'descriptions', 'location', 'specification')


    def get_specification(self, obj):
        values = obj  # whatever your filter values are. obj is the Research instance
        s_m = CookSpecilityMapping.objects.filter(cook_id=values.id)
        specification_list = []
        for m in s_m:
            spe = Specility.objects.get(id=m.specility_id)
            spe = SpecilitySerializer(spe)
            specification_list.append(spe.data)
        specification = specification_list
        return specification

    def get_location(self, obj):
        values = obj  # whatever your filter values are. obj is the Research instance
        c_m = CookLocationMapping.objects.filter(cook_id=values.id)
        location_list = []
        for m in c_m:
            loca = Location.objects.get(id=m.location_id)
            loca = LocationSerializer(loca)
            location_list.append(loca.data)
        location = location_list
        return location



class JobDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetails
        fields = ('id', 'name','contact_number_one', 'descriptions')


class JobLocationMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobLocationMapping
        fields = ('id', 'job_id', 'location_id')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name','middle_name', 'last_name', 'email', 'phone_number', 'password', 'created_at')


class UserJobMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserJobMapping
        fields = ('id', 'user_id', 'job_id')



class UserCookMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserCookMapping
        fields = ('id', 'user_id', 'cook_id')


