import json
import requests
import datetime
from time import sleep
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import View
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from api import views as backend_view 


class HomeView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html', context={})


@method_decorator(csrf_protect, name='dispatch')
class CookListView(View):

    def get(self, request, *args, **kwargs):
        page = max(int(request.GET['page']), 1) if "page" in request.GET else 1
        limit = settings.PAGE_SIZE

        data = {}
        if 'search_by' in request.GET.keys():
            data["search_by"] = request.GET["search_by"]
        if 'page' in request.GET.keys():
            data["page"] = request.GET["page"]
        if 'area' in request.GET.keys():
            data["area"] = request.GET["area"]
        try:
            area_list = backend_view.get_area_list() 
            cook_list = backend_view.cook_list(data)

            page_details = {
                'page': page,
                'limit': limit,
                'count': len(cook_list)
            }
            
            if len(cook_list) == 0:
                return render(request, 'cooklist.html', context={'cook_list': cook_list,
                                                                'area_list': area_list,
                                                                'page_details': page_details,
                                                                'message': 'No result'})

            return render(request, 'cooklist.html', context={'cook_list': cook_list,
                                                                'area_list': area_list,
                                                                'page_details': page_details})
        except Exception as e:
            print(e)
            return render(request, 'cooklist.html', context={'cook_list': [],
                                                                'area_list': [],
                                                                'page_details': {},
                                                                'message': 'No result'})

    def post(self, request, *args, **kwargs):
        search_by = request.POST["search_by"]
        cook_list = backend_view.cook_list() 

        return render(request, 'cooklist.html', context={'cook_list': cook_list})


@method_decorator(csrf_protect, name='dispatch')
class AddCookView(View):

    def get(self, request, *args, **kwargs):
        area_list = backend_view.get_area_list() 

        return render(request, 'registration.html', context={'area_list': area_list})

    def post(self, request, *args, **kwargs):
        user_id = None
        if request.session.get('is_login', False):
            user_id = request.session.get('user_id')
        agreement= request.POST.get('terms')
        
        personal_details = {'name': request.POST.get('name'),
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
                'specification': specification,
                'user_id': user_id}

        headers = {"content-type": "application/json"}
        json_data = json.dumps(data)
        location_list = backend_view.get_area_list() 
        try:
            response_data = backend_view.CookView.post(data)
            cook_json_data = response_data #json.loads(response_data.text)
            
            if cook_json_data['error_message'] != '':
                return render(request, 'registration.html',
                              context={'error_message': 'Invalid Card Number/Mobile Number, use unique PanCard and 10 digit mobile no',
                                       'area_list': location_list})

            cook_id = cook_json_data['Cook_id']
            img = request.FILES['profile_photo']
            ext = img.name.split('.')[-1]
            name = img.name.split('.')[0]
            img.name = 'C_' + str(cook_id) + '_' + name + '.' + ext

            img_response_data = backend_view.CookImage.post({'cook_id': cook_id, 'profile_pic': img.name})
            user_folder = settings.MEDIA_ROOT+'/images'


            img_save_path = user_folder +'/'+ str(img)

            with open(img_save_path, 'wb') as actual_file:
                actual_file.write(img.read())

        except Exception as e:
            print(e)
            return render(request, 'registration.html', context={'error_message': 'Server down, please try after sometimes ', 'area_list': location_list})
        return render(request, 'registration.html', context={'message': 'successfully created', 'area_list': location_list})


def cookDetail(request, cook_id):

    details = backend_view.getCookDetail(cook_id)
    return render(request, 'cook_details.html', {'cookdetails': details[0]})


class VacancyListView(View):

    def get(self, request, *args, **kwargs):
        page = max(int(request.GET['page']), 1) if "page" in request.GET else 1
        limit = settings.PAGE_SIZE

        data = {}

        try:
            # area_list = backend_view.get_area_list() 
            vacancy_list = backend_view.vacancy_list(data)

            page_details = {
                'page': page,
                'limit': limit,
                'count': len(vacancy_list)
            }
            
            if len(vacancy_list) == 0:
                return render(request, 'vacancy_list.html', context={'vacancy_list': vacancy_list,
                                                                'page_details': page_details,
                                                                'message': 'No result'})

            return render(request, 'vacancy_list.html', context={'vacancy_list': vacancy_list,
                                                                'page_details': page_details})
        except Exception as e:
            print(e)
            return render(request, 'vacancy_list.html', context={'vacancy_list': [],
                                                                'page_details': {},
                                                                'message': 'No result'})


@method_decorator(csrf_protect, name='dispatch')
class JobView(View):

    def get(self, request, *args, **kwargs):
        area_list = backend_view.get_area_list() 

        return render(request, 'add_jobs.html', context={'area_list': area_list})

    def post(self, request, *args, **kwargs):
        agreement= request.POST.get('terms')
        user_id = None
        if request.session.get('is_login', False):
            user_id = request.session.get('user_id')
        job_details = {'name': request.POST.get('name'),
                        'contact_number_one': request.POST.get('primary_contact_number'),
                        'descriptions': request.POST.get('description')
                        }

        area_list = request.POST.getlist('area')
        location = list()
        for area in area_list:
            area_dic = {'area': area}
            location.append(area_dic)

        data = {'job_details': job_details,
                'location': location,
                'user_id':user_id}
        headers = {"content-type": "application/json"}
        location_list = backend_view.get_area_list() 
        try:
            response_data = backend_view.JobView.post(data)
            cook_json_data = response_data 
            
            if cook_json_data['error_message'] != '':
                return render(request, 'add_jobs.html',
                              context={'error_message': 'Invalid Mobile Number, use unique 10 digit mobile no',
                                       'area_list': location_list})
        except Exception as e:
            return render(request, 'add_jobs.html', context={'error_message': 'Server down, please try after sometimes ', 'area_list': location_list})
        return render(request, 'add_jobs.html', context={'message': 'successfully created', 'area_list': location_list})


# @login_required
@method_decorator(csrf_protect, name='dispatch')
class CookSettingsView(View):

    def get(self, request, *args, **kwargs):
        if request.session.get('is_login', False):
            user_id = request.session.get('user_id')
            # user, msg = backend_view.UserView.getById(user_id)
            user_details = {}
            return render(request, 'cook_settings.html', context={'user_details': user_details})
        else:
            return render(request, 'login.html')


# @login_required
@method_decorator(csrf_protect, name='dispatch')
class JobSettingsView(View):
    def get(self, request, *args, **kwargs):
        if request.session.get('is_login', False):
            user_id = request.session.get('user_id')
            # user, msg = backend_view.UserView.getById(user_id)
            user_details = {}
            return render(request, 'job_settings.html', context={'user_details': user_details})
        else:
            return render(request, 'login.html')


# @login_required
@method_decorator(csrf_protect, name='dispatch')
class UserSettingsView(View):
    def get(self, request, *args, **kwargs):
        
        if request.session.get('is_login', False):
            user_id = request.session.get('user_id')
            user, msg = backend_view.UserView.getById(user_id)
            user_details = {}
            user_details['first_name'] = user.first_name
            user_details['middle_name'] = user.middle_name
            user_details['last_name'] = user.last_name
            user_details['email'] = user.email
            user_details['phone_number'] = user.phone_number
            return render(request, 'personal_settings.html', context={'user_details': user_details})
        else:
            return render(request, 'login.html')


@method_decorator(csrf_protect, name='dispatch')
class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        data = {}
        data['phone_number'] = request.POST.get('phone_number')
        data['password'] = request.POST.get('password')
        print(data)
        user, msg = backend_view.UserView.user_varify(data)
        print(user, msg)
        if user is None:
            return render(request, 'login.html', context={'error_message': msg})
        
        request.session.set_expiry(86400) #sets the exp. value of the session
        request.session['is_login'] = True 
        request.session['user_id'] = user.id
        user_details = {}
        user_details['first_name'] = user.first_name
        user_details['middle_name'] = user.middle_name
        user_details['last_name'] = user.last_name
        user_details['email'] = user.email
        user_details['phone_number'] = user.phone_number
        return render(request, 'personal_settings.html', context={'user_details': user_details})


@method_decorator(csrf_protect, name='dispatch')
class LogoutView(View):
    def get(self, request, *args, **kwargs):
        is_login = request.session.pop('is_login',None)
        user_id = request.session.pop('user_id',None)
        return render(request, 'home.html')

@method_decorator(csrf_protect, name='dispatch')
class SignupView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'signup.html')
    
    def post(self, request, *args, **kwargs):
        user_details = {}
        user_details['first_name'] = request.POST.get('first_name')
        user_details['last_name'] = request.POST.get('last_name')
        user_details['middle_name'] = request.POST.get('middle_name')
        user_details['email'] = request.POST.get('email')
        user_details['phone_number'] = request.POST.get('phone_number')
        user_details['created_at'] = datetime.datetime.now().date()
        user_details['password'] = request.POST.get('password')
        user_id, msg = backend_view.UserView.create(user_details)
        if msg is not None:
            return render(request, 'signup.html',
                              context={'error_msg': msg})
        del user_details['password']
        user_details['user_id'] = user_id
        request.session.set_expiry(86400) #sets the exp. value of the session
        request.session['is_login'] = True 
        request.session['user_id'] = user_id
        return render(request, 'personal_settings.html',
                              context={'user_details': user_details})


class UserUpdateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'update_user.html')
    
    def post(self, request, *args, **kwargs):
        user_details = {}
        # if request.session.get('is_login', False):
        user_details['id'] = request.session.get('user_id')
        user_details['first_name'] = request.POST.get('first_name')
        user_details['last_name'] = request.POST.get('last_name')
        user_details['middle_name'] = request.POST.get('middle_name')
        user_details['email'] = request.POST.get('email')
        user_details['phone_number'] = request.POST.get('phone_number')
        succes_msg, error_msg = backend_view.UserView.update(user_details)
        if error_msg is not None:
            return render(request, 'update_user.html',
                              context={'error_message': error_msg})
        return render(request, 'personal_settings.html',
                              context={'user_details': user_details, 'message': succes_msg})

        