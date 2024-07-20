from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render

from django.views.generic import TemplateView

import requests
import json

from WeatherApp import settings



class MainPageView(TemplateView):
    template_name = 'main/index.html'

    access_key = settings.WEATHERAPI
    geocode = settings.GEOAPI
    headers = {
        'X-Yandex-Weather-Key': access_key
        }
             
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        if self.request.method == "GET":

            city = self.request.GET.get('city')
            url_for_coords = f'https://geocode-maps.yandex.ru/1.x?apikey={self.geocode}&format=json&geocode={city}'
            data = requests.get(url_for_coords).json()

            try:
                coords = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()
                lon = coords[0]
                lat = coords[1]  

            except(IndexError, KeyError):
                return HttpResponse('City not found')

            url_for_weather = requests.get(f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}&lang=ru_RU', headers=self.headers)  
            weather_json = json.loads(url_for_weather.text)

            context['title'] = 'Home'
            context['city'] = city
            context['temp'] = weather_json['fact']['temp']
            context['humidity'] = weather_json['fact']['humidity']
            context['uv_index'] = weather_json['fact']['uv_index']
            context['wind_speed'] = weather_json['fact']['wind_speed']
            return context
        return context

    


# def MainPage(request):


#     if request.method == 'POST':

#         access_key = settings.WEATHERAPI
#         geocode = settings.GEOAPI
#         headers = {
#         'X-Yandex-Weather-Key': access_key
#         }

#         city = request.POST['city']
        
#         url_for_coords = f'https://geocode-maps.yandex.ru/1.x?apikey={geocode}&format=json&geocode={city}'
#         data = requests.get(url_for_coords).json()

#         try:
#             coords = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()
#             lon = coords[0]
#             lat = coords[1]  

#         except(IndexError, KeyError):
#             return HttpResponse('City not found')

#         url_for_weather = requests.get(f'https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}&lang=ru_RU', headers=headers)  
#         weather_json = json.loads(url_for_weather.text)

        
#         context = {
#         'title': 'Home',
#         'city': city,
#         'temp': weather_json['fact']['temp'],
#         'humidity': weather_json['fact']['humidity'],
#         'uv_index': weather_json['fact']['uv_index'],
#         'wind_speed': weather_json['fact']['wind_speed'],
#         } 
        
    
#         return render(request, 'main/index.html', context)
#     return render(request, 'main/index.html')
