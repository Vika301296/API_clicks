import requests

from environs import Env

long_url = 'https://espanalandia.ru'


def shorten_link(token, long_url):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {'Authorization': f'Bearer {token}'}
    payload = {
        "long_url": f"{long_url}"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    bitlink = response.json()
    return bitlink['id']


def count_clicks(token, bitlink):
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(passed_url):
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{passed_url}'
    response = requests.get(url, headers=headers)
    return response.ok


if __name__ == "__main__":
    env = Env()
    env.read_env()
    token = env.str('BITLINK_TOKEN')

    try:
        url = input('Введите ссылку: ')
        if is_bitlink(url) is True:
            total_clicks = count_clicks(token, url)
            print(f'Total Clicks: {total_clicks}')
        else:
            bitlink = shorten_link(token, url)
            print(f'Bitlink: {bitlink}')
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            print("Bad Request Error 400:", e.response.json())
        else:
            print("Other Error:", e)
