import random
import vk_api
from datetime import date

class VkBot:
    def __init__(self, community_token, user_token, user_link):
        self.vk_community = vk_api.VkApi(token=community_token)
        self.vk_user = vk_api.VkApi(token=user_token)
        self.user_link = user_link

    def get_id(self):
        user_id = self.user_link.split('/')
        return user_id[-1]

    def get_user_info(self):
        params = {
            'user_ids': self.get_id(),
            'fields': 'sex, bdate, city, relation, age'
        }
        response = self.vk_community.method('users.get', params)
        return response

    def find_matches(self):
        user_data = self.get_user_info()
        if 'bdate' in user_data[0].keys():
            bdate = user_data[0]['bdate'].split('.')
            if len(bdate) == 3:
                user_age = date.today().year - int(bdate[-1])
        else:
            user_age = int(input('Укажите свой возраст'))
        if user_data[0]['sex'] == 2:
            sex = 1
        else:
            sex = 2
        params = {
            'sort': 0,
            'count': 1000,
            'sex': sex,
            'status': 6,
            'city': user_data[0]['city']['id'],
            'age_from': user_age - 3,
            'age_to': user_age + 3
        }

        response = self.vk_user.method('users.search', params)
        return response

    def get_photos(self):
        result = {
            'link': None,
            'photos': []
        }
        matches = self.find_matches()
        count = len(matches['items']) - 1
        match = matches['items'][random.randint(0, count)]['id']
        params = {
            'owner_id': match,
            'album_id': 'profile',
            'extended': 1
        }
        photos = sorted(self.vk_user.method('photos.get', params)['items'], key=lambda x: x['likes']['count'],
                        reverse=True)
        top_photos = photos[:3]
        result['link'] = 'https://vk.com/id' + str(match)
        result['photos'] += ['photo' + str(x['owner_id']) + '_' + str(x['id']) for x in top_photos]
        return result
vk = VkBot('5b6a1b2b17173897d66dc603143b8a221178ddf4cd89946a8f61fb8d2da26ecece132b82abd864addbb56', '193a60928cf0f5a27e478d45275fd55b815b68019b63a993005e746104d3961aad746d9b74e3d9906e7cc', 'https://vk.com/rollingonthefloorandlaughing')
print(vk.get_photos())