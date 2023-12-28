from django.http import HttpResponse
from django.shortcuts import render
import paho.mqtt.client as mqtt
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
global_humidity = None
def on_connect(client, userdata, flags, rc, properties=None):
    print("CONNACK received with code %s." % rc)

def on_publish(client, userdata, mid):
    print("mid: " + str(mid))

def on_subscribe(client, userdata, mid, granted_qos, properties=None):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))
    humidity_value = json.loads(msg.payload)['humidity']
    update_humidity_in_view(humidity_value)


def update_humidity_in_view(value):
    global global_humidity
    global_humidity = value

def get_humidity(request):
    humidity_value = global_humidity if global_humidity is not None else 0
    return JsonResponse({'humidity': humidity_value})

@csrf_exempt
def send_to_topic(request):
    client = mqtt.Client(client_id="", protocol=mqtt.MQTTv5)
    if request.method == 'POST':
        mode = request.POST.get('Mode', '')
        if mode in ('0', '1'):
            client.on_connect = on_connect
            client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
            client.username_pw_set("GreenSmart", "Minhtu19062002")
            client.connect("59f312a8eac34af9982aa5d07e1f9a86.s2.eu.hivemq.cloud", 8883)
            
            client.on_publish = on_publish
            client.publish("ModeValue", payload=mode, qos=1)
            client.loop_start()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def mqtt_connect(request):
    client = mqtt.Client(client_id="", protocol=mqtt.MQTTv5)
    client.on_connect = on_connect
    client.tls_set(tls_version=mqtt.ssl.PROTOCOL_TLS)
    client.username_pw_set("GreenSmart", "Minhtu19062002")
    client.connect("59f312a8eac34af9982aa5d07e1f9a86.s2.eu.hivemq.cloud", 8883)
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    client.on_publish = on_publish
    client.subscribe("esp8266/soil-moisture/#", qos=1)
    client.publish("ModeValue", payload="cooll", qos=1)
    client.loop_start()

    return render (request, "index/data_display.html")

