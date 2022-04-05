import vk_api
from get_user_info import *

token = '193a60928cf0f5a27e478d45275fd55b815b68019b63a993005e746104d3961aad746d9b74e3d9906e7cc'

vk = vk_api.VkApi(token=token)


def find_matches(user_link):
    if get_user_info(user_link)[0]['sex'] == 2:
        sex = 1
    else:
        sex = 2
    params = {
        'sort': 0,
        'count': 20,
        'sex': sex,
        'status': 6,
        'city': get_user_info(user_link)[0]['city']['id']
    }

    response = vk.method('users.search', params)
    return response

