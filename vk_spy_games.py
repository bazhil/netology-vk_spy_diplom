from urllib.parse import urlencode
import  requests
import json
import time
from pprint import pprint

TOKEN = '5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128'
target_uid = '5030613'
api_version = '5.73'
BASE_URL = 'https://api.vk.com/method/'

def find_friends(target_uid):
    """
    функция поиска друзей пользователя
    :param target_uid: ID целевого пользователя в Вконтакте
    :return: возвращает список идентификаторов друзей пользователя
    """
    friends_id = []
    params = {
        'access_token': TOKEN,
        'target_uid': target_uid,
        'v': api_version
    }

    url = BASE_URL + 'friends.get'
    response = requests.get(url, params)
    if response.status_code == 200:
        friends_id = response.json()['response']['items']
    return friends_id

def find_groups(target_uid):
    """
    функция поиска групп пользователя
    :param target_uid: ID целевого пользователя в Вконтакте
    :return: возвращает словарь групп пользователя с ключами идентификатор группы значениями имя группы
    """
    user_groups = {}
    params = {
        'access_token': TOKEN,
        'user_id': target_uid,
        'v': api_version,
        'extended': 1
    }

    url = BASE_URL + 'groups.get'
    response = requests.get(url, params)

    if response.status_code == 200:
        try:
            items_from_groups = response.json()['response']['items']
            user_groups = {item['id']: item['name'] for item in items_from_groups}
            time.sleep(0.4)
            print('.')
        except KeyError:
            pass
    return user_groups

def group_analyse(friends_id, user_groups):
    """
    функция анализирующая группы пользователя
    :param friends_id: список друзей пользователя
    :param user_groups: список групп пользователя
    :return: возвращает список групп пользователя в которых не состоит ни один из друзей пользователя
    """
    friend_groups = []
    for friend in friends_id:
        friend_groups += list(find_groups(friend).keys())
    return set(user_groups.keys()) - set(friend_groups)

def get_members(group_id):
    """
    функция получающая количество пользователей в группах
    :param group_id: идентификатор группы
    :return: возвращает количество участников группы с ключами
    """
    users_in_group = 0
    params = {
        'access_token': TOKEN,
        'group_id': group_id,
        'v': api_version
    }

    url = BASE_URL + 'groups.getMembers'
    response = requests.get(url, params)
    if response.status_code == 200:
        try:
            users_in_group = response.json()['response']['count']
            time.sleep(0.4)
            print('.')
        except:
            pass
    return users_in_group

def end_analyse():
    """
    функция анализирующая группы и сохраняющая результат в файле groups.json
    """
    group_info = []
    user_id = input('Введите id целевого пользователя: ')
    if not user_id:
        print('Ошибка: не введен идентификатор')
    friends = find_friends(user_id)
    groups = find_groups(user_id)
    unique_groups = group_analyse(friends, groups)
    for group in unique_groups:
        count = get_members(group)
        group_info.append(dict(name=groups[group], gid=group, members_count=count))
    with open('groups.json', 'w', encoding='utf-8') as f:
        json.dump(group_info, f, ensure_ascii=False, indent=2)

end_analyse()