import argparse
import requests


def shorten_link(token, long_url):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {'Authorization': f'Bearer {token}'}
    payload = {
        "long_url": long_url
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


def is_bitlink(token, passed_url):
    headers = {'Authorization': f'Bearer {token}'}
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{passed_url}'
    response = requests.get(url, headers=headers)
    return response.ok


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'url', help='convert url into bitlink or show the amount of clicks')
    parser.add_argument(
        'token', help='type your API token'
    )
    args = parser.parse_args()

    try:
        if is_bitlink(args.token, args.url):
            total_clicks = count_clicks(args.token, args.url)
            print(f'Total Clicks: {total_clicks}')
        else:
            bitlink = shorten_link(args.token, args.url)
            print(f'Bitlink: {bitlink}')
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            print("Bad Request Error 400:", e.response.json())
        else:
            print("Other Error:", e)
