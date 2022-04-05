import vk_api
from datetime import datetime

from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

token = '5b6a1b2b17173897d66dc603143b8a221178ddf4cd89946a8f61fb8d2da26ecece132b82abd864addbb56'

vk = vk_api.VkApi(token=token)
longpoll = VkBotLongPoll(vk, group_id=212424686, wait=25)


def write_message(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': int(datetime.utcnow().timestamp())})


for event in longpoll.listen():
    if event.type == VkBotEventType.MESSAGE_NEW:

        if event.from_user:
            request = event.object

            if request['message']['text'] == "привет":
                write_message(request['message']['from_id'], "Хай")
            elif request['message']['text'] == "пока":
                write_message(request['message']['from_id'], "Пока((")
            else:
                write_message(request['message']['from_id'], "Не поняла вашего ответа...")
