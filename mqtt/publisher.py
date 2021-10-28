import random
import time
from os import path
import sys
# To make it possible to execute the publisher from the terminal, this is needed to import the sensors
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from paho.mqtt import client as mqtt_client
from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor


broker = 'broker.emqx.io'
port = 1883
topics = [
    "sensors/temperature",
    "sensors/humidity"
]
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'


def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    temperature_sensor = TemperatureSensor()
    humidity_sensor = HumiditySensor()
    msg_count = 0
    while True:
        topic_num = 0
        messages = []
        time.sleep(0.1)
        temp = temperature_sensor.read_temperature()
        messages.append(temp)
        humidity = humidity_sensor.read_humidity()
        messages.append(humidity)

        for msg in messages:
            result = client.publish(topics[topic_num], msg)
            # result: [0, 1]
            status = result[0]
            if status == 0:
                print(f"Send `{msg}` to topic `{topics[topic_num]}`")
            else:
                print(f"Failed to send message to topic {topics[topic_num]}")
            msg_count += 1
            topic_num += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
