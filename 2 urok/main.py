import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(access_token, url):
    vk_url = 'https://api.vk.com/method/utils.getShortLink'
    params = {
        'access_token': access_token,
        'url': url,
        'v':  5.236
    }

    response = requests.get(vk_url, params=params)
    response.raise_for_status()
    return response.json()['response']['short_url']


def count_clicks(access_token, short_url):
    key = urlparse(short_url).path.lstrip('/')
    vk_url = 'https://api.vk.com/method/utils.getLinkStats'

    params = {
        'access_token': access_token,
        'key': key,
        'interval': 'forever',
        'v':  5.236
    }

    response = requests.get(vk_url, params=params)
    response.raise_for_status()
    stats = response.json()['response']['stats']
    if stats:
        return stats[0]['views']
    else:
        return 0


def is_short_link(url):
    return urlparse(url).netloc == 'vk.cc'


def main():
    load_dotenv()
    access_token = os.environ['VK_TOKEN']
    try:
        user_url = input('Введите ссылку для сокращения или статистики кликов: ')
        if is_short_link(user_url):
            clicks = count_clicks(access_token, user_url)
            print(f'Количество кликов по ссылке: {clicks}')
        else:
            short_url = shorten_link(access_token, user_url)
            print(f'Сокращенная ссылка: {short_url}')
    except requests.exceptions.HTTPError as error:
        print(f'Ошибка: Неверная ссылка - {error}')
        print(f'Ответ: {error.response.json()}')
    except requests.exceptions.RequestException as error:
        print(f'Ошибка: Ошибка запроса - {error}')
    except KeyError:
        print('Ошибка: Нет ответа от сервера')


if __name__ == "__main__":
    main()
