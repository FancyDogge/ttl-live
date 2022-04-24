from asyncio.windows_events import NULL
import requests
import geocoder

"""" Курс рубля к доллару и евро """

API_key_exchange = '597e6276254fd13fcf183cb2d44dc38b'


def get_rubusd_rate():
    try:
        response = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={API_key_exchange}&symbols=USD,RUB')

        eur_to_usd = response.json()['rates']['USD']
        eur_to_rub = response.json()['rates']['RUB']

        usd_to_rub = eur_to_rub / eur_to_usd

        return round(usd_to_rub, 1), round(eur_to_rub, 1)

    except requests.exceptions.HTTPError as eh:
        return eh
    except requests.exceptions.ConnectionError as ec:
        return ec
    except requests.exceptions.Timeout as et:
        return et
    except requests.exceptions.RequestException as er:
        return er

#print(get_rubusd_rate())



"""" Прогноз погоды """

API_key_geo = '096cb0be2424e976e4b996ba795c1c17'
myloc = geocoder.ip('me')


def weather_api_call(ip):
    try:

        # if ip == '127.0.0.1':
        #     ip = geocoder.ip('me')
        #     print(ip)

        user_location = geocoder.ipinfo(ip)


        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={user_location.latlng[0]}&lon={user_location.latlng[1]}&appid={API_key_geo}&units=metric')
        weather_icon_id = response.json()['weather'][0]['icon']

        weather_icon_url = f'https://openweathermap.org/img/wn/{weather_icon_id}@2x.png'
        temperature = response.json()['main']['temp']
        feels_like = response.json()['main']['feels_like']
        wind = response.json()['wind']['speed']
        country_and_city = response.json()['sys']['country'] + ', ' + response.json()['name']

        context = {
            'temperature': temperature,
            'feels like': feels_like,
            'wind': wind,
            'country and city': country_and_city,
            'icon_url': weather_icon_url
        }

        return context

    except requests.exceptions.HTTPError as eh:
        return eh
    except requests.exceptions.ConnectionError as ec:
        return ec
    except requests.exceptions.Timeout as et:
        return et
    except requests.exceptions.RequestException as er:
        return er
    except (KeyError, TypeError):
        return NULL

#print(weather_api_call())

""" bitcoin price """
def get_bitcoin_price():
    try:
        response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false')

        bitcoin_price = response.json()[0]['current_price']

        return bitcoin_price

    except requests.exceptions.HTTPError as eh:
        return eh
    except requests.exceptions.ConnectionError as ec:
        return ec
    except requests.exceptions.Timeout as et:
        return et
    except requests.exceptions.RequestException as er:
        return er


""" Cute Cats to make a day """
def get_cat_img():
    try:
        response = requests.get('https://api.thecatapi.com/v1/images/search')

        img_url = response.json()[0]['url']

        return img_url
    
    except requests.exceptions.HTTPError as eh:
        return eh
    except requests.exceptions.ConnectionError as ec:
        return ec
    except requests.exceptions.Timeout as et:
        return et
    except requests.exceptions.RequestException as er:
        return er