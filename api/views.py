# from time import sleep

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404

# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework.validators import ValidationError

from .custom_serializers import get_json_obj, get_area_list_json
from .utils import get_cook_using_area, get_cook_using_user_name, get_cook_list, get_area_list_from_db
from .models import UserDetails, Location, Specility, CookLocationMapping, CookSpecilityMapping
from .serializers import CookSerializer, \
    UserDetailsSerializer, \
    CookLocationMappingSerializer, \
    CookSpecilityMappingSerializer, \
    CookProfileImageSerializer

# import logging
# logger = logging.getLogger(__name__)


PAGE_LIMIT = 6
# Create your views here.
@csrf_exempt
def cook_list(data={}):
    """
    List all code snippets, or create a new snippet.
    """
    if data.keys() != []:
        page_number = data.get('page', None)
        name = data.get('search_by', None)
        area = data.get('area', None)

        if name is not None:
            # logger.info('Information get_cook_using_user_name!')
            cooks = get_cook_using_user_name(name, PAGE_LIMIT, page_number)
        elif area is not None:
            # logger.info('Information get_cook_using_area!')
            cooks = get_cook_using_area(area, PAGE_LIMIT, page_number)
        else:
            # logger.info('Information get_cook_list!')
            cooks = get_cook_list(PAGE_LIMIT, page_number)

        # custom_serializer = get_json_obj(cooks)
        return cooks


# Create your views here.
@csrf_exempt
def get_area_list():
    """
    List all code snippets, or create a new snippet.
    """
    areas = get_area_list_from_db()
    area_list_serializer = get_area_list_json(areas)
    return area_list_serializer


class CookView:

    @classmethod
    def mapping_location_with_user(cls, location_list, cook_id):
        # logger.info('mapping location with cook')

        for location in location_list:
            area = location['area']
            if len(Location.objects.filter(area=area)):
                location_id = Location.objects.get(area=area).id
                cook_location_mapping = {'cook_id': cook_id, 'location_id': location_id}
                location_serializer = CookLocationMappingSerializer(data=cook_location_mapping)
                if location_serializer.is_valid(raise_exception=True):
                    location_serializer.save()
                    # logger.info('successfully mapped location with cook')
            else:
                # logger.error('wrong location name')
                return False
        return True

    @classmethod
    def create_specification(cls, specification_list, cook_id):
        # logger.info('creating specification for cook')

        specification_details = specification_list[0]
        north_indian_food = specification_details['north_indian_food']
        south_indian_food = specification_details['south_indian_food']
        chinees_food = specification_details['chinees_food']

        specility_id = Specility.objects.get(north_indian_food=north_indian_food, south_indian_food=south_indian_food,
                                             chinees_food=chinees_food).id

        cook_specility_mapping = {'cook_id': cook_id, 'specility_id': specility_id}

        specility_serializer = CookSpecilityMappingSerializer(data=cook_specility_mapping)

        if specility_serializer.is_valid(raise_exception=True):
            specility_serializer.save()
            # logger.info('successfully created specification for cook')
        else:
            # logger.error('error while creating specification')
            return False
        return True

    @classmethod
    def update_cook_personal_info(cls, cook_details):
        # updating cook personal info
        # logger.info('update existing cook details')
        sleep(2)
        personal_details = cook_details.get('personal_details')
        cook_id = personal_details['id']
        saved_cook = get_object_or_404(UserDetails.objects.all(), id=cook_id)

        cook_serializer = UserDetailsSerializer(instance=saved_cook, data=personal_details, partial=True)
        if cook_serializer.is_valid(raise_exception=True):
            cook_serializer.save()
            # logger.info('successfully updated existing cook personal details')
        return True

    @classmethod
    def update_cook_location_info(cls, cook_id, cook_details):
        sleep(2)
        exist_locations = CookLocationMapping.objects.filter(cook_id=cook_id)
        for loc in exist_locations:
            loc.delete()
        location_list = cook_details.get('location')
        loc_result = CookView.mapping_location_with_user(location_list, cook_id)
        if loc_result is False:
            error_msg = 'error while updating cook location'
            # logger.error(error_msg)
            return cook_id, '', error_msg
        return True

    @classmethod
    def update_cook_specifications_info(cls, cook_id, cook_details):
        exist_specifications = get_object_or_404(CookSpecilityMapping.objects.all(), cook_id=cook_id)
        exist_specifications.delete()
        specification_list = cook_details.get('specification')
        spc_result = CookView.create_specification(specification_list, cook_id)
        if spc_result is False:
            error_msg = 'error while updating cook specifications'
            # logger.error(error_msg)
            return cook_id, '', error_msg
        return True

    @classmethod
    def create_cook_details(cls, cook_details):
        personal_details = cook_details.get('personal_details')
        success_msg = ''
        error_msg = ''
        cook_id = ''
        try:
            serializer = UserDetailsSerializer(data=personal_details)
            if serializer.is_valid(raise_exception=True):
                cook_saved = serializer.save()
                cook_id = cook_saved.id

            location_list = cook_details.get('location')
            CookView.mapping_location_with_user(location_list, cook_id)

            specification_list = cook_details.get('specification')
            CookView.create_specification(specification_list, cook_id)

        except ValidationError as v:
            error_msg = 'This cook is already exist in application ' if 'pan_card' in v.detail else 'please enter valid inputs'
            # logger.error(error_msg)
            return cook_id, success_msg, error_msg
        except Exception as e:
            # logger.error("Exception while creating cook: ", e)
            return cook_id, success_msg, 'server down'
        # logger.info('successfully created cook')
        return cook_id, success_msg, error_msg

    @classmethod
    def get(cls):
        users = UserDetails.objects.all()
        serializer = CookSerializer(users, many=True)
        # logger.info('fetch cook details list')
        return serializer.data

    @classmethod
    def post(cls, data):
        cook_details = data
        cook_id = ''
        try:
            if 'id' in cook_details.get('personal_details').keys():
                # logger.info('request for updating cook {}', cook_details.get('personal_details')['id'])
                cook_id = cook_details.get('personal_details')['id']
                CookView.update_cook_personal_info(cook_details)
                CookView.update_cook_location_info(cook_id, cook_details)
                CookView.update_cook_specifications_info(cook_id, cook_details)
                success_message = 'successfully updated'
            else:
                # logger.info('request for creating cook')
                cook_id, success_message, error_message = CookView.create_cook_details(cook_details)
        except Exception as e:
            return {"success": '', 'error_message': e, "Cook_id": cook_id}
        return {"success": success_message, 'error_message': '', "Cook_id": cook_id}



class CookImage:
    """
    this view used for get the images and save the images.
    """

    @classmethod
    def post(cls, data):

        # logger.info("request for adding cook's profile image")
        try:
            serializer = CookProfileImageSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                cook_saved = serializer.save()
                # logger.info("{} created successfully", cook_saved.id)
        except Exception as e:
            # logger.error('exception while adding cook image: ', e)
            return {"Error": "server down"}
        return {"success": "created successfully"}

