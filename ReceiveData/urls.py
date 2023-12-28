from django.contrib import admin
from django.urls import path
from .views import mqtt_connect, get_humidity, send_to_topic
urlpatterns = [
    path('', mqtt_connect,name='mqtt_connect'),
    path('get_humidity/', get_humidity, name='get_humidity'),
    path('send_to_topic/', send_to_topic, name='send_to_topic')
]
