import random
import vk_api
from datetime import date
from db import select_db, insert_db
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
        if select_db(self.get_id(), str(match)):
            return self.get_photos()
        params = {
            'owner_id': match,
            'album_id': 'profile',
            'extended': 1
        }
        while True:
            try:
                photos = sorted(self.vk_user.method('photos.get', params)['items'], key=lambda x: x['likes']['count'],
                                reverse=True)
                top_photos = photos[:3]
                result['link'] = 'https://vk.com/id' + str(match)
                result['photos'] += ['photo' + str(x['owner_id']) + '_' + str(x['id']) for x in top_photos]
                insert_db(self.get_id(), match)
                break
            except (Exception, vk_api.exceptions.ApiError) as error:
                print('Ошибка при работе с VK_api', error)
                return self.get_photos()

        return result
