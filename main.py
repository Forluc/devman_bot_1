from environs import Env
import requests

env = Env()
env.read_env()

token = env.str('TOKEN')

headers = {
    'Authorization': f'Token {token}'
}
url_long = 'https://dvmn.org/api/long_polling/'
while True:
    try:
        response = requests.get(url_long, headers=headers, timeout=60)
        response.raise_for_status()
        for message in response:
            print(message)
    except requests.exceptions.ReadTimeout:
        continue
    except requests.exceptions.ConnectionError:
        continue
