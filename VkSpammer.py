import vk_api
from vk_api.utils import get_random_id
from sys import exc_info
from random import choice
from time import sleep

token = input('Ваш токен: ')
id = int(input('Введите id. Id Чата вводить с "-" вначале: '))

#отправка и мнгновенное удаление
def chat_send(vk, chat_id, name_mass):
    vk.messages.delete(message_ids=vk.messages.send(chat_id=chat_id, random_id=get_random_id(), message=f'{choice(name_mass)}'), delete_for_all=1)


def peer_send(vk, user_id):
    vk.messages.delete(message_ids=vk.messages.send(user_id=user_id, random_id=get_random_id(), message='.'), delete_for_all=1)


#создание массива id участников бесседы, которые используются как сообщение для спама 
send = lambda: peer_send(vk, id)
if id < 0:
    vk_session = vk_api.VkApi(token=token)
    vk = vk_session.get_api()

    profile_name = vk.users.get(user_ids=vk.account.getProfileInfo()['screen_name'])[0]['id']
    data = vk.messages.getChat(chat_id=id*-1)
    name_mass = data["users"]
    name_mass.remove(data['admin_id'])
    name_mass.remove(profile_name)
    send = lambda: chat_send(vk, id*-1, name_mass) 

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

running = True
while running:
    try:
        send()
    except vk_api.exceptions.Captcha:
        print('Captcha Error.')
    #если неизвестная ошибка - он ее выводит
    except:
        print(exc_info()[0])
    sleep(0.5)