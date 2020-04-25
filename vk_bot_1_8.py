import random

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll


def main():
    login, password = LOGIN, PASSWORD
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()
    response = vk.photos.get(album_id=272048436, group_id=GROUP_ID)
    photo_to_send = ''
    if response['items']:
        photo_to_send = random.choice(
            [f"photo{item['owner_id']}_{item['id']}" for item in response['items']]
        )

    vk_session = vk_api.VkApi(
        token=TOKEN)
    longpoll = VkBotLongPoll(vk_session, GROUP_ID)

    for event in longpoll.listen():
        print(event)
        vk = vk_session.get_api()

        if event.obj.message:
            name = vk.users.get(user_id=event.obj.message['from_id'])[0]['first_name']

            city = None
            try:
                city = vk.users.get(user_id=event.obj.message['from_id'], fields='city')[0]['city']['title']
            except Exception:
                pass
            # print(event.obj.message['from_id'])
            if city:
                vk.messages.send(peer_id=event.obj.message['from_id'],
                                 message=f'Привет, {name}! Как поживает {city}?\nА это котик',
                                 attachment=photo_to_send,
                                 random_id=random.randint(0, 2 ** 64))
            else:
                vk.messages.send(peer_id=event.obj.message['from_id'],
                                 message=f'Привет, {name}!',
                                 attachment=photo_to_send,
                                 random_id=random.randint(0, 2 ** 64))


if __name__ == '__main__':
    main()
