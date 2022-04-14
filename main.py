import vk_api
from datetime import datetime
from vk_bot import VkBot

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

comunity_token = '5b6a1b2b17173897d66dc603143b8a221178ddf4cd89946a8f61fb8d2da26ecece132b82abd864addbb56'

vk = vk_api.VkApi(token=comunity_token)
longpoll = VkBotLongPoll(vk, group_id=212424686, wait=25)
user_link = None


def write_message(user_id, message, attachment=None):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'attachment' : attachment, 'random_id': int(datetime.utcnow().timestamp())})

mode = None
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:

        if event.from_user:
            request = event.object

            if request['message']['text'] == "Начать":
                write_message(request['message']['from_id'], "Введите свой токен")
                mode = 'token'

            elif mode == 'token':
                user_token = request['message']['text']
                write_message(request['message']['from_id'], "Кому ищем пару?")
                mode = 'user_link'

            elif mode == 'user_link':
                if not vk_bot:
                    try:
                        user_link = request['message']['text']
                        vk_bot = VkBot(comunity_token, user_token, user_link)
                    except (Exception, vk_api.exceptions.ApiError) as error:
                        print('Ошибка ввода', error)
                        continue
                data = vk_bot.get_photos()
                if data == 'no_age':
                    mode = 'age_request'
                    continue
                if data == 'no_city':
                    mode = 'city_request'
                    continue
                photos = [x for x in data['photos']]
                write_message(request['message']['from_id'], data['link'], attachment=','.join(photos))



            elif mode == 'age_request':
                vk_bot.user_age = int(request['message']['text'])
                mode = 'user_link'

            elif mode == 'city_request':
                city_name = request['message']['text']
                vk_bot.user_city = vk_bot.get_city(city_name)
                mode = 'user_link'

