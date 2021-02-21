import requests 
import json
from dotenv import load_dotenv
import os

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from passlib.hash import sha256_crypt

from .custom_serializers import get_json_obj, get_area_list_json
from .utils import get_cook_using_area, get_cook_using_user_name, get_cook_list, get_area_list_from_db, get_cook_using_id, get_job_list, get_cook_contact_number_list
from .models import UserDetails, Location, Specility, CookLocationMapping, CookSpecilityMapping, User, JobLocationMapping, UserJobMapping, UserCookMapping, JobDetails
from .serializers import CookSerializer, \
    UserDetailsSerializer, \
    CookLocationMappingSerializer, \
    CookSpecilityMappingSerializer, \
    CookProfileImageSerializer,\
    JobDetailsSerializer, \
    JobLocationMappingSerializer, \
    UserSerializer, \
    UserJobMappingSerializer, \
    UserCookMappingSerializer
from . import constants


load_dotenv(verbose=True)
PAGE_LIMIT = 200


@csrf_exempt
def cook_list(data={}):
    """
    List all code snippets, or create a new snippet.
    """
    if data.keys() != []:
        page_number = data.get('page', None)
        name = data.get('search_by', None)
        area = data.get('area', None)
        user_id = data.get('user_id', None)
        if user_id is not None:
            cooks = get_cook_list(limit=PAGE_LIMIT, page_number=page_number, user_id=user_id)
        elif name is not None:
            cooks = get_cook_using_user_name(name, PAGE_LIMIT, page_number)
        elif area is not None:
            cooks = get_cook_using_area(area, PAGE_LIMIT, page_number)
        else:
            cooks = get_cook_list(PAGE_LIMIT, page_number)

        dataList = []
        # cook_dict = {}
        for cook in cooks:
            isMatch = False
            for data in dataList:
                if (data is None or data == {}):
                    isMatch = False
                    break
                if cook['id'] == data['id']:
                    isMatch = True
                    if isinstance(cook['area'], list):
                        for ca in cook['area']:
                            data['area'].append(ca)
                    else:
                        data['area'].append(cook['area'])

            if not isMatch: 
                area = []
                area.append(cook['area'])
                cook['area'] = area  
                dataList.append(cook)
                
        return dataList


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

        for location in location_list:
            area = location['area']
            if len(Location.objects.filter(area=area)):
                location_id = Location.objects.get(area=area).id
                cook_location_mapping = {'cook_id': cook_id, 'location_id': location_id}
                location_serializer = CookLocationMappingSerializer(data=cook_location_mapping)
                if location_serializer.is_valid(raise_exception=True):
                    location_serializer.save()
            else:
                return False
        return True

    @classmethod
    def create_specification(cls, specification_list, cook_id):

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
        else:
            return False
        return True

    @classmethod
    def update_cook_personal_info(cls, cook_details):
        # updating cook personal info
        
        personal_details = cook_details.get('personal_details')
        cook_id = personal_details['id']
        saved_cook = get_object_or_404(UserDetails.objects.all(), id=cook_id)

        cook_serializer = UserDetailsSerializer(instance=saved_cook, data=personal_details, partial=True)
        if cook_serializer.is_valid(raise_exception=True):
            cook_serializer.save()
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
            return cook_id, '', error_msg
        return True

    @classmethod
    def create_cook_details(cls, user_id, cook_details):
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
            CookView.mapping_cook_with_user(user_id, cook_id)

        except ValidationError as v:
            # error_msg = 'This cook is already exist in application ' if 'pan_card' in v.detail else 'please enter valid inputs'
            error_msg = str(v)
            return cook_id, success_msg, error_msg
        except Exception as e:
            return cook_id, success_msg, 'server down'
        return cook_id, success_msg, error_msg


    @classmethod
    def mapping_cook_with_user(cls, user_id, cook_id):
        user_cook_mapping = {'cook_id': cook_id, 'user_id': user_id}
        user_cook_serializer = UserCookMappingSerializer(data=user_cook_mapping)
        try:
            if user_cook_serializer.is_valid(raise_exception=True):
                user_cook_serializer.save()
        except Exception as e:
            error_msg = str(e)
        return True


    @classmethod
    def get(cls):
        users = UserDetails.objects.all()
        serializer = CookSerializer(users, many=True)
        return serializer.data

    @classmethod
    def post(cls, data):
        cook_details = data
        cook_id = None
        success_message = None
        error_message = None
        
        try:
            # if UserDetails.objects.get(pan_card=cook_details.get('personal_details')['pan_card']):
            #     return {"success": '', 'error_message': 'pancard is already exist.', "Cook_id": cook_id}
            
            if 'id' in cook_details.get('personal_details').keys():
                cook_id = cook_details.get('personal_details')['id']
                CookView.update_cook_personal_info(cook_details)
                CookView.update_cook_location_info(cook_id, cook_details)
                CookView.update_cook_specifications_info(cook_id, cook_details)
                CookView.mapping_cook_with_user(data['user_id'], cook_id)
                success_message = 'successfully updated'
            else:
                cook_id, success_message, error_message = CookView.create_cook_details(data['user_id'], cook_details)
        except Exception as e:
            return {"success": '', 'error_message':str(e), "Cook_id": cook_id}
        return {"success": success_message, 'error_message': error_message, "Cook_id": cook_id}


class CookImage:
    """
    this view used for get the images and save the images.
    """

    @classmethod
    def post(cls, data):

        try:
            serializer = CookProfileImageSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                cook_saved = serializer.save()
        except Exception as e:
            return {"Error": "server down"}
        return {"success": "created successfully"}


def getCookDetail(cook_id):
    try:
        cook_details = get_cook_using_id(cook_id)
        dataList = []
        cook_dict = {}
        for cook in cook_details:
            isMatch = False
            for data in dataList:
                if (data is None or data == {}):
                    isMatch = False
                    break
                if cook['id'] == data['id']:
                    isMatch = True
                    if isinstance(cook['area'], list):
                        for ca in cook['area']:
                            data['area'].append(ca)
                    else:
                        data['area'].append(cook['area'])

            if not isMatch: 
                area = []
                area.append(cook['area'])
                cook['area'] = area  
                dataList.append(cook)
    except Exception as e:
        return {"Error": "server down"}
    return dataList


@csrf_exempt
def vacancy_list(data={}):
    jobs = None
    user_id = None
    if data.keys() != []:
        page_number = data.get('page', None)
        user_id = data.get('user_id', None)
        job_id = data.get('job_id', None)
        if job_id is not None:
            jobs = get_job_list(limit=PAGE_LIMIT, page_number=page_number, job_id=job_id)
        elif user_id is not None:
            jobs = get_job_list(limit=PAGE_LIMIT, page_number=page_number, user_id=user_id)
        else:
            jobs = get_job_list(limit=PAGE_LIMIT, page_number=page_number)

        dataList = []
        # cook_dict = {}
        for job in jobs:
            isMatch = False
            for data in dataList:
                if (data is None or data == {}):
                    isMatch = False
                    break
                if job['id'] == data['id']:
                    isMatch = True
                    if isinstance(job['area'], list):
                        for ca in job['area']:
                            data['area'].append(ca)
                    else:
                        data['area'].append(job['area'])

            if not isMatch: 
                area = []
                area.append(job['area'])
                job['area'] = area  
                dataList.append(job)
                
        return dataList


class JobView:

    @classmethod
    def deleteJobAreaMapped(cls, job_id):
        res = JobLocationMapping.objects.filter(job_id=job_id).delete()

    @classmethod
    def deleteUserJobMapped(cls, job_id):
        res = UserJobMapping.objects.filter(job_id=job_id).delete()

    @classmethod
    def deleteJob(cls, job_id):
        try:
            JobView.deleteJobAreaMapped(job_id)
            JobView.deleteUserJobMapped(job_id)
            res = JobDetails.objects.filter(id=job_id).delete()
        except Exception as e:
            return None, str(e)
        return constants.delete_msg, None

    @classmethod
    def updateJobDetails(cls, data):
        job_details = data.get('job_details')
        success_msg = None
        error_msg = None
        job_id = data.get('job_id', None)
        try:
            JobDetails.objects.filter(id=job_id).update(name=job_details['name'],
                                                    contact_number_one=job_details['phone_number'],
                                                    descriptions=job_details['descriptions'])
            JobView.deleteJobAreaMapped(job_id)
            location_list = data.get('location')

            # mapping job with location
            JobView.mapping_location_with_job(location_list, job_id)

            success_msg = constants.update_msg
        except ValidationError as v:
            error_msg = str(v)
            return success_msg, error_msg
        except Exception as e:
            return success_msg, str(e)
        return success_msg, error_msg

    @classmethod
    def getJobById(cls, user_id):
        pass

    @classmethod
    def mapping_location_with_job(cls, location_list, job_id):
        for location in location_list:
            area = location['area']
            if len(Location.objects.filter(area=area)):
                location_id = Location.objects.get(area=area).id
                job_location_mapping = {'job_id': job_id, 'location_id': location_id}
                location_serializer = JobLocationMappingSerializer(data=job_location_mapping)
                if location_serializer.is_valid(raise_exception=True):
                    location_serializer.save()
            else:
                return False
        return True


    @classmethod
    def create_job_details(cls, data):
        job_details = data.get('job_details')
        success_msg = None
        error_msg = None
        job_id = None
        user_id = data['user_id']
        try:
            serializer = JobDetailsSerializer(data=job_details)
            if serializer.is_valid(raise_exception=True):
                job_saved = serializer.save()
                job_id = job_saved.id
            location_list = data.get('location')

            # mapping job with location
            JobView.mapping_location_with_job(location_list, job_id)

            # mapping job with user
            user_job_mapping = {'job_id': job_id, 'user_id': user_id}
            user_job_serializer = UserJobMappingSerializer(data=user_job_mapping)
            if user_job_serializer.is_valid(raise_exception=True):
                user_job_serializer.save()
            success_msg = constants.create_msg
        except ValidationError as v:
            error_msg = str(v)
            return job_id, success_msg, error_msg
        except Exception as e:
            return job_id, success_msg, str(e)
        return job_id, success_msg, error_msg

    @classmethod
    def post(cls, data):
        job_details = data
        job_id = ''
        user_id = data['user_id']
        success_message = None
        error_message = None
        
        try:
            job_id, success_message, error_message = JobView.create_job_details(job_details)
            cook_contact_res = get_cook_contact_number_list()
            contact_list = ''
            for contact_dict in cook_contact_res:
                contact_list +=contact_dict['contact_number_one']+','
            msg = 'hi' # job_details['job_details']['descriptions'][:30]
            send_fast_sms(contact_list, msg)
        except Exception as e:
            error_message = str(e)
            return {"success": success_message, 'error_message': error_message, "Job_Id": job_id}
        return {"success": success_message, 'error_message': error_message, "Job_Id": job_id}


def send_fast_sms(contact_list, msg):
    # mention url 
    url = "https://www.fast2sms.com/dev/bulkV2"
    
    job_msg = 'Job www.cookdukan.com/cook_job'
    # create a dictionary 
    my_data = { 
        # Your default Sender ID 
        'sender_id': 'SMSINI',  
        
        # Put your message here! 
        # 'message': 'This is a test message', 
        "message" : "7",
        "variables_values" : job_msg,  
        
        'language': 'english', 
        'route': 's', 
        
        # You can send sms to multiple numbers 
        # separated by comma. 
        'numbers': contact_list    
    } 

    # create a dictionary 
    headers = { 
        'authorization': os.getenv("FAST_SMS_KEY"),
        'Content-Type': "application/x-www-form-urlencoded", 
        'Cache-Control': "no-cache"
    }

    response = requests.request("POST", 
                            url, 
                            data = my_data, 
                            headers = headers) 
    
    #load json data from source 
    returned_msg = json.loads(response.text) 


class UserView:

    @classmethod
    def getById(cls, user_id):
        error_msg = ''
        user = User.objects.get(id=user_id)
        if user is None:
            # invalid
            error_msg = 'invalid Id'
        return user, error_msg

    @classmethod
    def getByPwdPhone(cls, data):
        error_msg = ''
        user = User.objects.filter(phone_number=data[constants.phone_number], password=data[constants.password])
        if user is None:
            # invalid
            error_msg = constants.invalid_credential
        return user, error_msg
    
    @classmethod
    def create(cls, user_details):
        # user_details = user_details.get(constants.data)
        success_msg = None
        error_msg = None
        user_details[constants.password] = sha256_crypt.encrypt(user_details[constants.password])
        user_id = None
        try:
            serializer = UserSerializer(data=user_details)
            if serializer.is_valid(raise_exception=True):
                user_saved = serializer.save()  
                user_id =  user_saved.id
        except ValidationError as v:
            error_msg = str(v)
            return success_msg, error_msg
        except Exception as e:
            error_msg = str(e)
            return success_msg, error_msg
        return user_id, error_msg
    
    @classmethod
    def update(cls, data):
        try:
            User.objects.filter(id=data[constants.user_id]).update(first_name=data[constants.first_name],
                                                    middle_name=data[constants.middle_name],
                                                    last_name=data[constants.last_name], 
                                                    email=data[constants.email], 
                                                    phone_number=data[constants.phone_number])
        except Exception as e:
            return None, str(e)
        return constants.update_msg, None
    
    @classmethod
    def user_varify(cls, data):
        try:
            user = User.objects.get(phone_number=data[constants.phone_number])
            is_valid = sha256_crypt.verify(data[constants.password], user.password)
            if not is_valid:
                return None, constants.invalid_credential
        except Exception as e:
            return None, str(e)
        return user, None
    
    @classmethod
    def reset_password(cls, data):
        pass

    @classmethod
    def varify_otp(cls, data):
        pass
        
