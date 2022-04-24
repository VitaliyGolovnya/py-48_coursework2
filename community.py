import vk_api
from datetime import datetime
from vk_bot import VkBot
import time
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType


class Community:
    def __init__(self, user_token):
        with open("community_token.txt") as file:
            self.community_token = file.read()
        self.vk = vk_api.VkApi(token=self.community_token)
        self.user_token = user_token
        self.user_link = None
        self.vk_bot = None

    def write_message(self, user_id, message, attachment=None):
        self.vk.method('messages.send', {'user_id': user_id, 'message': message, 'attachment': attachment,
                                         'random_id': int(datetime.utcnow().timestamp())})
        time.sleep(1)

    def send_match(self, request):
        data = self.vk_bot.get_photos()
        if self.vk_bot.error == True:
            self.write_message(request['message']['from_id'], "База данных недопуступна. Результаты могут повторяться.")
            time.sleep(1)
        if data == 'no_age':
            self.write_message(request['message']['from_id'], "Введите возраст")
            return 'age_request'
        if data == 'no_city':
            self.write_message(request['message']['from_id'], "Введите город")
            return 'city_request'
        photos = [x for x in data['photos']]
        while True:
            try:
                self.write_message(request['message']['from_id'], data['link'], attachment=','.join(photos))
                self.write_message(request['message']['from_id'], "Искать еще пару Y/N?")
                break
            except (Exception, vk_api.exceptions.ApiError) as error:
                print('Ошибка при работе с VK_api', error)
        return 'quit'

    def longpolling(self):
        longpoll = VkBotLongPoll(self.vk, group_id=212424686, wait=25)

        mode = None
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW and event.from_user:

                request = event.object

                if str.lower(request['message']['text']) == "начать":
                    self.write_message(request['message']['from_id'], "Кому ищем пару?")
                    mode = 'user_link'


                elif mode == 'user_link':
                    if self.vk_bot is None:
                        try:
                            self.user_link = request['message']['text']
                            self.vk_bot = VkBot(self.user_token, self.user_link)
                        except (Exception, vk_api.exceptions.ApiError) as error:
                            print('Ошибка ввода', error)
                    mode = self.send_match(request)


                elif mode == 'age_request':
                    try:
                        self.vk_bot.get_age(int(request['message']['text']))
                        mode = self.send_match(request)
                    except ValueError:
                        self.write_message(request['message']['from_id'], "Ошибка ввода. Напишите число")
                        mode = self.send_match(request)


                elif mode == 'city_request':
                    try:
                        self.vk_bot.get_city(request['message']['text'])
                        mode = self.send_match(request)
                    except IndexError:
                        self.write_message(request['message']['from_id'], "Невозможно найти город")
                        mode = self.send_match(request)

                elif mode == 'quit':
                    if str.lower(request['message']['text']) == 'y':
                        mode = self.send_match(request)
                    elif str.lower(request['message']['text']) == 'n':
                        self.write_message(request['message']['from_id'], "Выход из программы")
                        time.sleep(1)
                        self.write_message(request['message']['from_id'],
                                           'Напишите "начать", чтобы запустить программу заново')
                        mode = None
                        self.vk_bot = None
