import random
import time
from os import path
import sys
# To make it possible to execute the publisher from the terminal, this is needed to import the sensors
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from paho.mqtt import client as mqtt_client
from sensors.temperature_sensor import TemperatureSensor
from sensors.humidity_sensor import HumiditySensor


broker = 'localhost'
port = 1883
topics = []
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'local'
password = 'localpw'
status_topic = []
status_m = 0
sensor_num_set = False

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
    global sensor_num_set

    if not sensor_num_set:
        # Set temperature sensor number
        try:
            file = open("temp_sensor_num.txt", 'r')
            filedata = file.read()
            temp_sensor_num = int(filedata) + 1
            file = open("temp_sensor_num.txt", 'w')
            file.write(str(temp_sensor_num))
            file.flush()
        except IOError:
            file = open("temp_sensor_num.txt", 'w')
            file.write("1")
            file.flush()
            temp_sensor_num = 1

        # Set humidity sensor number
        try:
            file = open("hum_sensor_num.txt", 'r')
            filedata = file.read()
            hum_sensor_num = int(filedata) + 1
            file = open("hum_sensor_num.txt", 'w')
            file.write(str(hum_sensor_num))
            file.flush()
        except IOError:
            file = open("hum_sensor_num.txt", 'w')
            file.write("1")
            file.flush()
            hum_sensor_num = 1

        topics.append(f"sensor/{temp_sensor_num}/temp")
        topics.append(f"sensor/{hum_sensor_num}/hum")
        status_topic.append(f"sensor/{temp_sensor_num}/status")
        sensor_num_set = True

    if status_m == 1:
        topic_num = 0
        messages = []
        time.sleep(0.5)
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

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        if msg.topic == status_topic[0]:
            global status_m
            if msg.payload.decode() == "0":
                status_m = 0
            else:
                status_m = 1
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(status_topic[0])
    client.on_message = on_message

def run():
    client = connect_mqtt()
    client.loop_start()
    while True:
        publish(client)
        subscribe(client)


if __name__ == '__main__':
    run()
