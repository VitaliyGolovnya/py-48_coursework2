import vk_api
from datetime import datetime
from vk_bot import VkBot
import time
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

comunity_token = '5b6a1b2b17173897d66dc603143b8a221178ddf4cd89946a8f61fb8d2da26ecece132b82abd864addbb56'

vk = vk_api.VkApi(token=comunity_token)
longpoll = VkBotLongPoll(vk, group_id=212424686, wait=25)



def write_message(user_id, message, attachment=None):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'attachment': attachment,
                                'random_id': int(datetime.utcnow().timestamp())})
    time.sleep(1)


def send_match(request):
    data = vk_bot.get_photos()
    if data == 'no_age':
        write_message(request['message']['from_id'], "Введите возраст")
        return 'age_request'
    if data == 'no_city':
        write_message(request['message']['from_id'], "Введите город")
        return 'city_request'
    photos = [x for x in data['photos']]
    while True:
        try:
            write_message(request['message']['from_id'], data['link'], attachment=','.join(photos))
            write_message(request['message']['from_id'], "Искать еще пару Y/N?")
            break
        except (Exception, vk_api.exceptions.ApiError) as error:
            print('Ошибка при работе с VK_api', error)
    return 'quit'


mode = None
for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:

        request = event.object

        if str.lower(request['message']['text']) == "начать":
            write_message(request['message']['from_id'], "Введите свой токен")
            mode = 'token'

        elif mode == 'token':
            user_token = request['message']['text']
            write_message(request['message']['from_id'], "Кому ищем пару?")
            mode = 'user_link'
            vk_bot = None

        elif mode == 'user_link':
            if vk_bot is None:
                try:
                    user_link = request['message']['text']
                    vk_bot = VkBot(comunity_token, user_token, user_link)
                except (Exception, vk_api.exceptions.ApiError) as error:
                    print('Ошибка ввода', error)
            mode = send_match(request)


        elif mode == 'age_request':
            vk_bot.get_age(int(request['message']['text']))
            mode = send_match(request)

        elif mode == 'city_request':
            vk_bot.get_city( request['message']['text'])
            mode = send_match(request)

        elif mode == 'quit':
            if str.lower(request['message']['text']) == 'y':
                mode = send_match(request)
            elif str.lower(request['message']['text']) == 'n':
                write_message(request['message']['from_id'], "Выход из программы")
                time.sleep(1)
                write_message(request['message']['from_id'], 'Напишите "начать", чтобы запустить программу заново')
                mode = None