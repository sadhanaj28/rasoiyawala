from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.validators import ValidationError
from django.shortcuts import get_object_or_404
import json

from .custom_serializers import get_json_obj, get_area_list_json
from .utils import get_cook_using_area, get_cook_using_user_name, get_cook_list, get_area_list_from_db
from .models import UserDetails, Location, Specility, CookLocationMapping, CookSpecilityMapping
from .serializers import CookSerializer, \
    UserDetailsSerializer, \
    CookLocationMappingSerializer, \
    CookSpecilityMappingSerializer, \
    CookProfileImageSerializer


PAGE_LIMIT = 6
# Create your views here.
@csrf_exempt
def cook_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    page_number = None
    if request.method == 'GET':

        if 'page' in request.GET.keys():
            page_number = request.GET["page"]

        if 'search_by' in request.GET.keys():
            name = request.GET["search_by"]
            if page_number is not None:
                cooks = get_cook_using_user_name(name, PAGE_LIMIT, page_number)
            else:
                cooks = get_cook_using_user_name(name, PAGE_LIMIT)
        elif 'area' in request.GET.keys():
            area = request.GET["area"]
            if page_number is not None:
                cooks = get_cook_using_area(area, PAGE_LIMIT, page_number)
            else:
                cooks = get_cook_using_area(area, PAGE_LIMIT)
        else:
            if page_number is not None:
                cooks = get_cook_list(PAGE_LIMIT, page_number)
            else:
                cooks = get_cook_list(PAGE_LIMIT)

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
        try:
            area_list_serializer = get_area_list_json(areas)
        except Exception as e:
            print('area api @@@@@', e)
        return JsonResponse(area_list_serializer, safe=False)


class CookView(APIView):

    def create_location(self, location_list, cook_id):
        for location in location_list:
            area = location['area']
            if len(Location.objects.filter(area=area)):
                location_id = Location.objects.get(area=area).id
                cook_location_mapping = {'cook_id': cook_id, 'location_id': location_id}
                location_serializer = CookLocationMappingSerializer(data=cook_location_mapping)
                if location_serializer.is_valid(raise_exception=True):
                    cook_location_mapping_saved = location_serializer.save()
                    # cook_location_mapping_id = cook_location_mapping_saved.id
            else:
                print('wrong location name')
                return False
        return True

    def create_specification(self, specification_list, cook_id):
        specification_details = specification_list[0]
        north_indian_food = specification_details['north_indian_food']
        south_indian_food = specification_details['south_indian_food']
        chinees_food = specification_details['chinees_food']
        specility_id = Specility.objects.get(north_indian_food=north_indian_food, south_indian_food=south_indian_food,
                                             chinees_food=chinees_food).id
        cook_specility_mapping = {'cook_id': cook_id, 'specility_id': specility_id}
        specility_serializer = CookSpecilityMappingSerializer(data=cook_specility_mapping)
        if specility_serializer.is_valid(raise_exception=True):
            cook_specility_mapping_saved = specility_serializer.save()
            cook_specility_mapping_id = cook_specility_mapping_saved.id
        return True

    def get(self, request):
        users = UserDetails.objects.all()
        print('user: ', users[0])
        serializer = CookSerializer(users, many=True)
        print('serializer: ', serializer)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        personal_details = data.get('personal_details')
        if 'id' in personal_details.keys():
            cook_id = personal_details['id']
            saved_cook = get_object_or_404(UserDetails.objects.all(), id=cook_id)
            cook_serializer = UserDetailsSerializer(instance=saved_cook, data=personal_details, partial=True)
            if cook_serializer.is_valid(raise_exception=True):
                cook_saved = cook_serializer.save()

            # delete mapped location
            exist_locations = CookLocationMapping.objects.filter(cook_id=cook_id)
            for loc in exist_locations:
                loc.delete()
            location_list = data.get('location')
            loc_result = self.create_location(location_list, cook_id)

            # delete mapped specifications
            exist_specifications = get_object_or_404(CookSpecilityMapping.objects.all(), cook_id=cook_id)
            exist_specifications.delete()
            specification_list = data.get('specification')
            spc_result = self.create_specification(specification_list, cook_id)
        else:
            try:
                print('*******')
                serializer = UserDetailsSerializer(data=personal_details)

                if serializer.is_valid(raise_exception=True):
                    cook_saved = serializer.save()
                    cook_id = cook_saved.id

                location_list = data.get('location')
                loc_result = self.create_location(location_list, cook_id)

                specification_list = data.get('specification')
                spc_result = self.create_specification(specification_list, cook_id)
            except ValidationError as v:
                print('***** ', v.detail, '  type> ', type(v.detail))
                error_msg = 'This cook is already exist in application 'if 'pan_card' in v.detail else 'please enter valid inputs'
                return Response({'error_message': error_msg})
            except Exception as e:
                return Response({'error_message': 'server down'})
        return Response({"success": "created successfully", 'error_message': '', "Cook_id": cook_id})


class CookImageView(APIView):
    def post(self, request):
        data = request.data
        serializer = CookProfileImageSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            cook_saved = serializer.save()
            cook_id = cook_saved.id
        return Response({"success": "created successfully"})

