import json

def get_json_obj(data_list):
    data = {}
    cook_list = []
    for row in data_list:
        areal = []
        count = 0
        for cook in cook_list:
            if row['id'] == cook['id']:
                count = + 1
                if not isinstance(cook['area'], list):
                    if row['area'] != cook['area']:
                        areal.append(row['area'])
                        areal.append(cook['area'])
                        cook['area'] = areal
                    else:
                        areal.append(cook['area'])
                        cook['area'] = areal
                else:
                    if row['area'] not in cook['area']:
                        cook['area'].append(row['area'])
                break
        if count == 0:
            row['area'] = [row['area']]
            cook_list.append(row)

    data['cook'] = cook_list
    return data


def get_area_list_json(area_list):
    area = []
    for a in area_list:
        area.extend(a)
    return area
