# from django.http import Http404
from django.shortcuts import render
# from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
import requests
from django.conf import settings
import json
# import os

PAGE_SIZE = 6
GET_COOK_LIST_API = 'http://127.0.0.1:8000/api/cook/cooks_list/'
GET_AREA_LIST = 'http://127.0.0.1:8000/api/cook/area_list/'
CREATE_COOK_API = 'http://127.0.0.1:8000/api/cook/cook_details/'
UPLOAD_COOK_IMAGE_API = 'http://127.0.0.1:8000/api/cook/cook_image/'


@method_decorator(csrf_protect, name='dispatch')
class DashboardView(View):

    def get(self, request, *args, **kwargs):
        page = max(int(request.GET['page']), 1) if "page" in request.GET else 1
        limit = PAGE_SIZE
        cook_list_json_data = []
        area_list_json = []
        area_list = requests.get(GET_AREA_LIST, params=request.GET)
        try:
            area_list_json = area_list.json()
        except Exception as e:
            print('area : ', e)
        if 'search_by' in request.GET.keys():
            search_by = request.GET["search_by"]
            cook_list = requests.get(GET_COOK_LIST_API, params=request.GET)
        else:
            cook_list = requests.get(GET_COOK_LIST_API, params=request.GET)
        try:
            cook_list_json_data = cook_list.json()['cook']
        except Exception as e:
            print('$$$$', e)
        page_details = {
            'page': page,
            'limit': limit,
            'count': len(cook_list_json_data)
        }

        if len(cook_list_json_data) == 0:
            return render(request, 'dashboard.html', context={'cook_list': cook_list_json_data,
                                                              'area_list': area_list_json,
                                                              'page_details': page_details,
                                                              'message': 'No result'})
        if cook_list.status_code == 200:
            return render(request, 'dashboard.html', context={'cook_list': cook_list_json_data,
                                                              'area_list': area_list_json,
                                                              'page_details': page_details})

    def post(self, request, *args, **kwargs):
        search_by = request.POST["search_by"]
        r = requests.get(GET_COOK_LIST_API, params={'search_by': search_by})
        if r.status_code == 200:
            return render(request, 'dashboard.html', context={'cook_list': r.json()['cook']})


@method_decorator(csrf_protect, name='dispatch')
class AddCookView(View):

    def get(self, request, *args, **kwargs):
        area_list = requests.get(GET_AREA_LIST, params=request.GET)

        return render(request, 'add_cook.html', context={'area_list': area_list.json()})

    def post(self, request, *args, **kwargs):
        agreement= request.POST.get('terms')
        print('agreement: ',agreement )
        personal_details = {'name': request.POST.get('firstname'),
                            'type': 'Cook',
                            'gender': request.POST.get('gender'),
                            'pan_card': request.POST.get('pancard'),
                            'profile_pic':'',
                            'contact_number_one': request.POST.get('primary_contact_number'),
                            'contact_number_two': request.POST.get('secondary_contact_number'),
                            'descriptions': request.POST.get('description'),
                            'is_access_granted': request.POST.get('terms'),
                            }
        area_list = request.POST.getlist('area')
        location = list()
        for area in area_list:
            area_dic = {'area': area}
            location.append(area_dic)
        specification = []
        specification_dic = {'north_indian_food': request.POST.get('north_indian_food'),
                             'south_indian_food': request.POST.get('south_indian_food'),
                             'chinees_food': request.POST.get('chinees_food')
                             }
        specification.append(specification_dic)
        data = {'personal_details': personal_details,
                'location': location,
                'specification': specification}

        headers = {"content-type": "application/json"}
        json_data = json.dumps(data)
        location_list = requests.get(GET_AREA_LIST, params=request.GET)
        try:
            response_data = requests.post(
                                        CREATE_COOK_API,
                                        data=json_data,
                                        headers=headers
                                        )
            cook_json_data = json.loads(response_data.text)

            if cook_json_data['error_message'] != '':
                return render(request, 'add_cook.html',
                              context={'error_message': cook_json_data['error_message'],
                                       'area_list': location_list.json()})

            cook_id = cook_json_data['Cook_id']
            img = request.FILES['profile_photo']
            ext = img.name.split('.')[-1]
            name = img.name.split('.')[0]
            img.name = 'C_' + str(cook_id) + '_' + name + '.' + ext
            img_response_data = requests.post(
                                            UPLOAD_COOK_IMAGE_API,
                                            data=json.dumps({'cook_id': cook_id, 'profile_pic': img.name}),
                                            headers=headers
                                            )
            user_folder = settings.MEDIA_ROOT+'/images'


            img_save_path = user_folder +'/'+ str(img)

            with open(img_save_path, 'wb') as actual_file:
                actual_file.write(img.read())

        except Exception as e:
            print('@@@@ ## ', e)
            return render(request, 'add_cook.html', context={'error_message': 'Server down, please try after sometimes ', 'area_list': location_list.json()})
        return render(request, 'add_cook.html', context={'message': 'successfully created', 'area_list': location_list.json()})
