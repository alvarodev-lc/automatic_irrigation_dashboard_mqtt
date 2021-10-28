import random

from paho.mqtt import client as mqtt_client
from tkinter import *
from PIL import Image, ImageTk

broker = 'broker.emqx.io'
port = 1883
temp_topic = "sensors/temperature"
humidity_topic = "sensors/humidity"
# generate client ID with public prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100000)}'
username = 'emqx'
password = 'public'


def connect_mqtt() -> mqtt_client:
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


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        if msg.topic == "sensors/temperature":
            update_dashboard_temp(msg)
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(temp_topic)
    client.subscribe(humidity_topic)
    client.on_message = on_message


def update_dashboard_temp(msg):
    temp_label.config(text=msg.payload.decode() + " °C",
                      fg="black")


window = Tk()
window.title("MQTT Dashboard")
window.geometry("720x720")
window.configure(bg="white")

canvas = Canvas(window, bg="white", width=720, height=720)
# To erase the border of the canvas
canvas.config(highlightthickness=0)
canvas.place(x=0, y=0)
img = PhotoImage(file="../images/logo_test.png")
canvas.create_image(0, 0, anchor=NW, image=img)

canvas2 = Canvas(window, bg="white", width=100, height=100)
# To erase the border of the canvas
canvas2.config(highlightthickness=0)
canvas2.place(x=50, y=165)
img2 = Image.open("../images/temp.png")
resized_img = img2.resize((100, 100), Image.ANTIALIAS)
img2 = ImageTk.PhotoImage(resized_img)
canvas2.create_image(0, 0, anchor=NW, image=img2)

# Create Label
temp_label = Label(window,
                   text=" °C",
                   bg="white",
                   fg="black",
                   font=("Helvetica", 32))

temp_label.place(x=180, y=190)

client = connect_mqtt()
subscribe(client)
client.loop_start()

window.mainloop()
client.loop_stop()
