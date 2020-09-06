from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.validators import ValidationError
from django.shortcuts import get_object_or_404

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
def cook_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        page_number = request.GET.get('page', None)
        name = request.GET.get('search_by', None)
        area = request.GET.get('area', None)

        if name is not None:
            # logger.info('Information get_cook_using_user_name!')
            cooks = get_cook_using_user_name(name, PAGE_LIMIT, page_number)
        elif area is not None:
            # logger.info('Information get_cook_using_area!')
            cooks = get_cook_using_area(area, PAGE_LIMIT, page_number)
        else:
            # logger.info('Information get_cook_list!')
            cooks = get_cook_list(PAGE_LIMIT, page_number)

        custom_serializer = get_json_obj(cooks)
        return JsonResponse(custom_serializer, safe=False)


# Create your views here.
@csrf_exempt
def get_area_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        areas = get_area_list_from_db()
        area_list_serializer = get_area_list_json(areas)
        return JsonResponse(area_list_serializer, safe=False)


class CookView(APIView):

    def mapping_location_with_user(self, location_list, cook_id):
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

    def create_specification(self, specification_list, cook_id):
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

    def update_cook_personal_info(self, cook_details):
        # updating cook personal info
        # logger.info('update existing cook details')
        personal_details = cook_details.get('personal_details')
        cook_id = personal_details['id']
        saved_cook = get_object_or_404(UserDetails.objects.all(), id=cook_id)

        cook_serializer = UserDetailsSerializer(instance=saved_cook, data=personal_details, partial=True)
        if cook_serializer.is_valid(raise_exception=True):
            cook_serializer.save()
            # logger.info('successfully updated existing cook personal details')
        return True

    def update_cook_location_info(self, cook_id, cook_details):
        exist_locations = CookLocationMapping.objects.filter(cook_id=cook_id)
        for loc in exist_locations:
            loc.delete()
        location_list = cook_details.get('location')
        loc_result = self.mapping_location_with_user(location_list, cook_id)
        if loc_result is False:
            error_msg = 'error while updating cook location'
            # logger.error(error_msg)
            return cook_id, '', error_msg
        return True

    def update_cook_specifications_info(self, cook_id, cook_details):
        exist_specifications = get_object_or_404(CookSpecilityMapping.objects.all(), cook_id=cook_id)
        exist_specifications.delete()
        specification_list = cook_details.get('specification')
        spc_result = self.create_specification(specification_list, cook_id)
        if spc_result is False:
            error_msg = 'error while updating cook specifications'
            # logger.error(error_msg)
            return cook_id, '', error_msg
        return True

    def create_cook_details(self, cook_details):
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
            self.mapping_location_with_user(location_list, cook_id)

            specification_list = cook_details.get('specification')
            self.create_specification(specification_list, cook_id)

        except ValidationError as v:
            error_msg = 'This cook is already exist in application ' if 'pan_card' in v.detail else 'please enter valid inputs'
            # logger.error(error_msg)
            return cook_id, success_msg, error_msg
        except Exception as e:
            # logger.error("Exception while creating cook: ", e)
            return cook_id, success_msg, 'server down'
        # logger.info('successfully created cook')
        return cook_id, success_msg, error_msg

    def get(self, request):
        users = UserDetails.objects.all()
        serializer = CookSerializer(users, many=True)
        # logger.info('fetch cook details list')
        return Response(serializer.data)

    def post(self, request):
        cook_details = request.data
        cook_id = ''
        try:
            if 'id' in cook_details.get('personal_details').keys():
                # logger.info('request for updating cook {}', cook_details.get('personal_details')['id'])
                cook_id = cook_details.get('personal_details')['id']
                self.update_cook_personal_info(cook_details)
                self.update_cook_location_info(cook_id, cook_details)
                self.update_cook_specifications_info(cook_id, cook_details)
                success_message = 'successfully updated'
            else:
                # logger.info('request for creating cook')
                cook_id, success_message, error_message = self.create_cook_details(cook_details)
        except Exception as e:
            return Response({"success": '', 'error_message': e, "Cook_id": cook_id})
        return Response({"success": success_message, 'error_message': '', "Cook_id": cook_id})



class CookImageView(APIView):
    """
    this view used for get the images and save the images.
    """
    def post(self, request):
        # logger.info("request for adding cook's profile image")
        try:
            data = request.data
            serializer = CookProfileImageSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                cook_saved = serializer.save()
                # logger.info("{} created successfully", cook_saved.id)
        except Exception as e:
            # logger.error('exception while adding cook image: ', e)
            return Response({"Error": "server down"})
        return Response({"success": "created successfully"})

