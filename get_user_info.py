import vk_api

token = '5b6a1b2b17173897d66dc603143b8a221178ddf4cd89946a8f61fb8d2da26ecece132b82abd864addbb56'

vk = vk_api.VkApi(token=token)


def get_id(user_link):
    user_id = user_link.split('/')
    return user_id[-1]


def get_user_info(user_link):
    params = {
        'user_ids': get_id(user_link),
        'fields': 'sex, bdate, city, relation'
    }
    response = vk.method('users.get', params)
    return response

print(get_user_info('https://vk.com/rollingonthefloorandlaughing'))