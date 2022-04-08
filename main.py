import vk_api
from datetime import datetime
from vk_bot import VkBot

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

comunity_token = '5b6a1b2b17173897d66dc603143b8a221178ddf4cd89946a8f61fb8d2da26ecece132b82abd864addbb56'

vk = vk_api.VkApi(token=comunity_token)
longpoll = VkBotLongPoll(vk, group_id=212424686, wait=25)


def write_message(user_id, message, attachment=None):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'attachment' : attachment, 'random_id': int(datetime.utcnow().timestamp())})


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:

        if event.from_user:
            request = event.object

            if request['message']['text'] == "начать":
                write_message(request['message']['from_id'], "Введите свой токен")

            if len(request['message']['text']) == 85:
                user_token = request['message']['text']
                write_message(request['message']['from_id'], "Кому ищем пару?")

            if 'vk.com' in request['message']['text']:
                user_link = request['message']['text']
                vk_bot = VkBot(comunity_token, user_token, user_link)
                data = vk_bot.get_photos()
                photos = [x for x in data['photos']]
                write_message(request['message']['from_id'], data['link'], attachment=','.join(photos))
