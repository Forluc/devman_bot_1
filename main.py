import requests
from environs import Env

env = Env()
env.read_env()

dvmn_token = env.str('DVMN_TOKEN')

headers = {
    'Authorization': f'Token {dvmn_token}',
}
url_long = 'https://dvmn.org/api/long_polling/'
timestamp = 1697645287
while True:
    params = {
        'timestamp': timestamp,
    }
    try:
        response = requests.get(url_long, headers=headers, timeout=60, params=params)
        response.raise_for_status()
        for message in response:
            print(response.json())
        timestamp = response.json()['new_attempts'][0]['timestamp']
    except requests.exceptions.ReadTimeout:
        continue
    except requests.exceptions.ConnectionError:
        continue
