from django.db import connection
# import logging
# logger = logging.getLogger(__name__)

COOK_COLUMN_KEYS = ['id', 'name', 'type', 'gender', 'pan_card', 'profile_pic', 'descriptions', 
                    'contact_number_one', 'contact_number_two', 'city',
                    'area', 'north_indian_food', 'south_indian_food', 'chinees_food', 'other', 
                    'food_pic_one', 'food_pic_two']

JOB_COLUMN_KEYS = ['id', 'name', 'descriptions', 
                    'contact_number_one', 'city',
                    'area']

SMS_COLUMN_KEYS = ['contact_number_one']


def get_offset(page_number, limit):
    if int(page_number) <= 1:
        offset = 0
    else:
        offset = int(limit)*(int(page_number)) - int(limit)
    return offset


def get_cook_list(limit=None, page_number=None, user_id=None):
    with connection.cursor() as cursor:
        if user_id is not None:
            cursor.execute("SELECT pd.id, pd.name, pd.type, pd.gender, pd.pan_card, cpimg.profile_pic, \
                            pd.descriptions, pd.contact_number_one,\
                            pd.contact_number_two, ld.city, ld.area, s.north_indian_food, \
                            s.south_indian_food, s.chinees_food, s.other, s.food_pic_one, s.food_pic_two FROM user_details pd \
                            LEFT JOIN cook_location_mapping clm ON pd.id = clm.cook_id \
                            LEFT JOIN location ld ON ld.id = clm.location_id \
                            LEFT JOIN cook_specility_mapping csm ON pd.id = csm.cook_id \
                            LEFT JOIN specility s ON s.id = csm.specility_id \
                            LEFT JOIN cook_profile_image cpimg ON cpimg.cook_id = pd.id \
                            LEFT JOIN user_cook_mapping ucm ON ucm.cook_id = pd.id \
                            where ucm.user_id = %s \
                            ORDER BY pd.name ;", [user_id])
        elif page_number == None:
            cursor.execute("SELECT pd.`id`, pd.`name`, pd.`type`, pd.`gender`, pd.`pan_card`, cpimg.`profile_pic`, pd.`descriptions`, pd.`contact_number_one`,\
                            pd.`contact_number_two`, ld.`city`, ld.`area`, s.`north_indian_food`,\
                            s.`south_indian_food`, s.`chinees_food`, s.`other`, s.`food_pic_one`, s.`food_pic_two` FROM `user_details` pd \
                            LEFT JOIN `cook_location_mapping` clm ON pd.id = clm.cook_id \
                            LEFT JOIN `location` ld ON ld.id = clm.location_id\
                            LEFT JOIN `cook_specility_mapping` csm ON pd.id = csm.cook_id \
                            LEFT JOIN `specility` s ON s.id = csm.specility_id\
                            LEFT JOIN `cook_profile_image` cpimg ON cpimg.cook_id = pd.id\
                            ORDER BY pd.name LIMIT %s;", [limit])
        else:
            offset = get_offset(page_number, limit)
            cursor.execute("SELECT pd.`id`, pd.`name`, pd.`type`, pd.`gender`, pd.`pan_card`, cpimg.`profile_pic`, pd.`descriptions`, pd.`contact_number_one`,\
                                        pd.`contact_number_two`, ld.`city`, ld.`area`, s.`north_indian_food`,\
                                        s.`south_indian_food`, s.`chinees_food`, s.`other`, s.`food_pic_one`, s.`food_pic_two` FROM `user_details` pd \
                                        LEFT JOIN `cook_location_mapping` clm ON pd.id = clm.cook_id \
                                        LEFT JOIN `location` ld ON ld.id = clm.location_id\
                                        LEFT JOIN `cook_specility_mapping` csm ON pd.id = csm.cook_id \
                                        LEFT JOIN `cook_profile_image` cpimg ON cpimg.cook_id = pd.id\
                                        LEFT JOIN `specility` s ON s.id = csm.specility_id \
                                        ORDER BY pd.name LIMIT %s OFFSET %s;", (limit, offset))
        result = cursor.fetchall()
        response = [dict(zip(COOK_COLUMN_KEYS, row)) for row in result]
    return response


def get_cook_using_area(area, limit=None, page_number=None):
    with connection.cursor() as cursor:
        if page_number == None:
            cursor.execute("SELECT pd.`id`, pd.`name`, pd.`type`, pd.`gender`, pd.`pan_card`, cpimg.`profile_pic`, pd.`descriptions`, pd.`contact_number_one`,\
                        pd.`contact_number_two`, ld.`city`, ld.`area`, s.`north_indian_food`,\
                        s.`south_indian_food`, s.`chinees_food`, s.`other`, s.`food_pic_one`, s.`food_pic_two` FROM `user_details` pd \
                        LEFT JOIN `cook_location_mapping` clm ON pd.id = clm.cook_id \
                        LEFT JOIN `location` ld ON ld.id = clm.location_id\
                        LEFT JOIN `cook_specility_mapping` csm ON pd.`id` = csm.`cook_id` \
                        LEFT JOIN `specility` s ON s.id = csm.`specility_id` \
                        LEFT JOIN `cook_profile_image` cpimg ON cpimg.cook_id = pd.id\
                        WHERE ld.`area` = %s ORDER BY pd.name LIMIT %s; ", [area, limit])
        else:
            offset = get_offset(page_number, limit)
            cursor.execute("SELECT pd.`id`, pd.`name`, pd.`type`, pd.`gender`, pd.`pan_card`, cpimg.`profile_pic`, pd.`descriptions`, pd.`contact_number_one`,\
                                    pd.`contact_number_two`, ld.`city`, ld.`area`, s.`north_indian_food`,\
                                    s.`south_indian_food`, s.`chinees_food`, s.`other`, s.`food_pic_one`, s.`food_pic_two` FROM `user_details` pd \
                                    LEFT JOIN `cook_location_mapping` clm ON pd.id = clm.cook_id \
                                    LEFT JOIN `location` ld ON ld.id = clm.location_id\
                                    LEFT JOIN `cook_specility_mapping` csm ON pd.`id` = csm.`cook_id` \
                                    LEFT JOIN `specility` s ON s.id = csm.`specility_id` \
                                    LEFT JOIN `cook_profile_image` cpimg ON cpimg.cook_id = pd.id\
                                    WHERE ld.`area` = %s ORDER BY pd.name LIMIT %s OFFSET %s; ", [area, limit, offset])

        result = cursor.fetchall()
        response = [dict(zip(COOK_COLUMN_KEYS, row)) for row in result]
    return response

def get_cook_using_user_name(name, limit=None, page_number=None):
    with connection.cursor() as cursor:
        if page_number == None:
            cursor.execute("SELECT pd.`id`, pd.`name`, pd.`type`, pd.`gender`, pd.`pan_card`, cpimg.`profile_pic`, pd.`descriptions`, pd.`contact_number_one`,\
                        pd.`contact_number_two`, ld.`city`, ld.`area`, s.`north_indian_food`,\
                        s.`south_indian_food`, s.`chinees_food`, s.`other`, s.`food_pic_one`, s.`food_pic_two` FROM `user_details` pd \
                        LEFT JOIN `cook_location_mapping` clm ON pd.id = clm.cook_id \
                        LEFT JOIN `location` ld ON ld.id = clm.location_id\
                        LEFT JOIN `cook_specility_mapping` csm ON pd.id = csm.cook_id \
                        LEFT JOIN `specility` s ON s.id = csm.specility_id \
                        LEFT JOIN `cook_profile_image` cpimg ON cpimg.cook_id = pd.id\
                        WHERE pd.`name` = %s ORDER BY pd.name LIMIT %s; ", [name, limit])
        else:
            offset = get_offset(page_number, limit)
            cursor.execute("SELECT pd.`id`, pd.`name`, pd.`type`, pd.`gender`, pd.`pan_card`, cpimg.`profile_pic`, pd.`descriptions`, pd.`contact_number_one`,\
                                    pd.`contact_number_two`, ld.`city`, ld.`area`, s.`north_indian_food`,\
                                    s.`south_indian_food`, s.`chinees_food`, s.`other`, s.`food_pic_one`, s.`food_pic_two` FROM `user_details` pd \
                                    LEFT JOIN `cook_location_mapping` clm ON pd.id = clm.cook_id \
                                    LEFT JOIN `location` ld ON ld.id = clm.location_id\
                                    LEFT JOIN `cook_specility_mapping` csm ON pd.id = csm.cook_id \
                                    LEFT JOIN `specility` s ON s.id = csm.specility_id \
                                    LEFT JOIN `cook_profile_image` cpimg ON cpimg.cook_id = pd.id\
                                    WHERE pd.`name` = %s ORDER BY pd.name LIMIT %s OFFSET %s; ", [name, limit, offset])
        result = cursor.fetchall()
        response = [dict(zip(COOK_COLUMN_KEYS, row)) for row in result]
    return response

def get_area_list_from_db():
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT l.`area` FROM `location` as l ORDER BY l.`area`;")
        row = cursor.fetchall()
    return row


def get_cook_using_id(id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT pd.`id`, pd.`name`, pd.`type`, pd.`gender`, pd.`pan_card`, cpimg.`profile_pic`, pd.`descriptions`, pd.`contact_number_one`,\
                    pd.`contact_number_two`, ld.`city`, ld.`area`, s.`north_indian_food`,\
                    s.`south_indian_food`, s.`chinees_food`, s.`other`, s.`food_pic_one`, s.`food_pic_two` FROM `user_details` pd \
                    LEFT JOIN `cook_location_mapping` clm ON pd.id = clm.cook_id \
                    LEFT JOIN `location` ld ON ld.id = clm.location_id\
                    LEFT JOIN `cook_specility_mapping` csm ON pd.`id` = csm.`cook_id` \
                    LEFT JOIN `specility` s ON s.id = csm.`specility_id` \
                    LEFT JOIN `cook_profile_image` cpimg ON cpimg.cook_id = pd.id\
                    WHERE pd.`id` = %s ORDER BY pd.name ; ", [id])
        result = cursor.fetchall()
        response = [dict(zip(COOK_COLUMN_KEYS, row)) for row in result]
    return response

def get_job_list(limit=None, page_number=None, user_id=None, job_id=None):
    with connection.cursor() as cursor:
        if job_id != None:
            cursor.execute("SELECT jd.id, jd.name, jd.descriptions, jd.contact_number_one, ld.city, ld.area FROM job_details jd \
                    LEFT JOIN job_location_mapping clm ON jd.id = clm.job_id \
                    LEFT JOIN location ld ON ld.id = clm.location_id \
                    LEFT JOIN user_job_mapping ujm ON ujm.job_id = jd.id \
                    where jd.id = %s \
                    ORDER BY jd.name", [job_id])
        elif user_id != None:
            cursor.execute("SELECT jd.id, jd.name, jd.descriptions, jd.contact_number_one, ld.city, ld.area FROM job_details jd \
                    LEFT JOIN job_location_mapping clm ON jd.id = clm.job_id \
                    LEFT JOIN location ld ON ld.id = clm.location_id \
                    LEFT JOIN user_job_mapping ujm ON ujm.job_id = jd.id \
                    where ujm.user_id = %s \
                    ORDER BY jd.name", [user_id])
        elif page_number == None:
            cursor.execute("SELECT jd.id, jd.name, jd.descriptions, jd.contact_number_one,\
                                ld.city, ld.area \
                                FROM job_details jd \
                                LEFT JOIN job_location_mapping clm ON jd.id = clm.job_id \
                                LEFT JOIN location ld ON ld.id = clm.location_id \
                                ORDER BY jd.name LIMIT %s;", [limit])
        else:
            offset = get_offset(page_number, limit)
            cursor.execute("SELECT jd.id, jd.name, jd.descriptions, jd.contact_number_one,\
                                ld.city, ld.area \
                                FROM job_details jd \
                                LEFT JOIN job_location_mapping clm ON jd.id = clm.job_id \
                                LEFT JOIN location ld ON ld.id = clm.location_id \
                                ORDER BY jd.name LIMIT %s OFFSET %s;", (limit, offset))
        result = cursor.fetchall()
        response = [dict(zip(JOB_COLUMN_KEYS, row)) for row in result]
    return response


def get_cook_contact_number_list():
    with connection.cursor() as cursor:
        cursor.execute("SELECT contact_number_one FROM user_details;")
        result = cursor.fetchall()
        response = [dict(zip(SMS_COLUMN_KEYS, row)) for row in result]
    return response

