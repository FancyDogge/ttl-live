import requests
import geocoder

"""" Курс рубля к доллару и евро """

API_key_exchange = '597e6276254fd13fcf183cb2d44dc38b'


def get_rubusd_rate():
    response = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={API_key_exchange}&symbols=USD,RUB')

    eur_to_usd = response.json()['rates']['USD']
    eur_to_rub = response.json()['rates']['RUB']

    usd_to_rub = eur_to_rub / eur_to_usd

    return round(usd_to_rub, 1), round(eur_to_rub, 1)

#print(get_rubusd_rate())



"""" Прогноз погоды """

API_key_geo = 'e42bfc4b0f5b3ca7fafc98bfe00e58f7'
myloc = geocoder.ip('me')


def weather_api_call():
    response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={myloc.latlng[0]}&lon={myloc.latlng[1]}&appid={API_key_geo}&units=metric')

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

#print(weather_api_call())

''' bitcoin price '''
def get_bitcoin_price():
    response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false')

    bitcoin_price = response.json()[0]['current_price']

    return bitcoin_price