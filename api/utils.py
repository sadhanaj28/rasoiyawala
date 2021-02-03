from django.db import connection
# import logging
# logger = logging.getLogger(__name__)

COOK_COLUMN_KEYS = ['id', 'name', 'type', 'gender', 'pan_card', 'profile_pic', 'descriptions', 'contact_number_one', 'contact_number_two', 'city',
                    'area', 'north_indian_food', 'south_indian_food', 'chinees_food', 'other', 'food_pic_one', 'food_pic_two']


def get_offset(page_number, limit):
    if int(page_number) <= 1:
        offset = 0
    else:
        offset = int(limit)*(int(page_number)) - int(limit)
    return offset


def get_cook_list(limit=None, page_number=None):
    with connection.cursor() as cursor:
        if page_number == None:
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

