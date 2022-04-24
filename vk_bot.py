import random
import vk_api
from datetime import date
from db import select_db, insert_db

class VkBot:
    def __init__(self, user_token, user_link):
        self.vk_user = vk_api.VkApi(token=user_token)
        self.user_link = user_link
        self.user_age = 'no_age'
        self.user_city = 'no_city'
        self.error = False

    def get_id(self):
        user_id = self.user_link.split('/')
        return user_id[-1]

    def get_user_info(self):
        params = {
            'user_ids': self.get_id(),
            'fields': 'sex, bdate, city, relation, age'
        }
        response = self.vk_user.method('users.get', params)
        return response

    def check_age(self):
        user_data = self.get_user_info()
        if 'bdate' in user_data[0].keys():
            bdate = user_data[0]['bdate'].split('.')
            if len(bdate) == 3:
                self.user_age = date.today().year - int(bdate[-1])
                return self.user_age
            return self.user_age
        else:
            return self.user_age

    def check_city(self):
        user_data = self.get_user_info()
        if 'city' in user_data[0].keys():
            self.user_city = user_data[0]['city']['id']
            return self.user_city
        else:
            return self.user_city

    def get_city(self, city_name):
        params = {'q' : city_name, 'country_id': 1}
        response = self.vk_user.method('database.getCities', params)
        city_id = response['items'][0]['id']
        self.user_city = city_id

    def get_age(self, age):
        self.user_age = age


    def find_matches(self):
        if self.check_city() == 'no_city':
            return 'no_city'
        if self.check_age() == 'no_age':
            return 'no_age'
        user_data = self.get_user_info()
        if user_data[0]['sex'] == 2:
            sex = 1
        else:
            sex = 2
        params = {
            'sort': 0,
            'count': 1000,
            'sex': sex,
            'status': 6,
            'city': self.user_city,
            'age_from': self.user_age - 3,
            'age_to': self.user_age + 3
        }

        response = self.vk_user.method('users.search', params)
        return response

    def get_photos(self):
        result = {
            'link': None,
            'photos': []
        }
        matches = self.find_matches()
        if matches == 'no_age':
            return 'no_age'
        if matches == 'no_city':
            return 'no_city'
        count = len(matches['items']) - 1
        match = matches['items'][random.randint(0, count)]['id']
        if select_db(self.get_id(), str(match)) == "db_error":
            self.error = True
        elif select_db(self.get_id(), str(match)):
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

