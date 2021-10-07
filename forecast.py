import os
import requests
import datetime
import logging

key = os.environ.get('WEATHER_KEY') # return None if not exists, returns its value if exists
url = 'http://api.openweathermap.org/data/2.5/forecast' 


def get_location():
    city, country = '',''
    while len(city) == 0:
        city = input('Type the city you want the weather for: ')

    while len(country) == 0:
        country = input('Type the 2-letter country code for the country the city is in: ')

    location = f'{city},{country}'
    return location


def get_current_weather(location, key):
    try:
        # requests can make dictionary of keys and values and pass into URL
        query = {'q': location, 'units': 'imperial', 'appid': key}
        response = requests.get(url, params=query)
        response.raise_for_status() # raise exception for 400 or 500 errors
        data = response.json() # this may raise error too if response not JSON
        return data, None
    except Exception as ex:
        print(ex)
        logging.debug(response.text)
        return None, ex # return a tuple, data is either data or None, exception either None or ex


def get_forecast_info(weather_data):
    forecast_list_data = weather_data['list']
    forecast_list = []
    for forecast in forecast_list_data:
        timestamp = forecast['dt']
        forecast_datetime = datetime.datetime.fromtimestamp(timestamp)
        forecast_date = datetime.date.fromtimestamp(timestamp)
        forecast_time = forecast_datetime.time()
        temp = forecast['main']['temp']
        wind_speed = forecast['wind']['speed']
        description = forecast['weather'][0]['description']
        forecast_dict = {'Date': forecast_date, 'Time': forecast_time, 'Temp': temp, 'Wind': wind_speed, 'Desc': description}
        forecast_list.append(forecast_dict)
    return forecast_list


def format_forecast(forecast):
    time = forecast['Time'] 
    temp = forecast['Temp'] 
    wind = forecast['Wind'] 
    description = forecast['Desc']
    # looked up formatting codes https://www.programiz.com/python-programming/datetime/strftime
    # so does datetime get the time in the user's time zone? That makes more sense for me for this program
    # since the user will be looking up times from their own computer, which is probably in their own timezone...
    # while it can be nice to see what time it will be in other countries when looking at the weather
    # most of us tend to think in terms of "our time" first
    forecast_string = f'At {time:%I:%M %p}, the temperature will be {temp}F, with a wind speed of {wind}. There will be {description}.'
    return forecast_string


def main():
    location = get_location()
    weather_data, error = get_current_weather(location, key)
    if error:
        print('Sorry, could not get weather')
    else: # if error is None
        forecasts = get_forecast_info(weather_data)
        date_printed = []
        for forecast in forecasts:
            date = forecast['Date']
            if date not in date_printed:
                print(f'\nOn {date:%d %B, %Y}:\n')
                date_printed.append(date)
            forecast_string = format_forecast(forecast)
            print(f'{forecast_string}')


if __name__ == '__main__':
    main()

