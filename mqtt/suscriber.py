import random
from collections import deque

from paho.mqtt import client as mqtt_client
from tkinter import *
from PIL import Image, ImageTk

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


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
            update_graph(msg)
        elif msg.topic == "sensors/humidity":
            update_dashboard_humidity(msg)
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(temp_topic)
    client.subscribe(humidity_topic)
    client.on_message = on_message

#############
# Dashboard #
#############


def update_dashboard_temp(msg):
    temp_label.config(text=msg.payload.decode() + " °C",
                      fg="black")


def update_dashboard_humidity(msg):
    hum_label.config(text=msg.payload.decode() + "%",
                     fg="black")


def update_graph(msg):
    # Swipe al values to the right
    x[:] = x[1:5]+x[0:1]
    y[:] = y[1:5] + y[0:1]
    # Then update the last value for the graph
    x[len(x) - 1] = x[len(x) - 1] + 0.1
    y[len(y) - 1] = msg.payload.decode()

    # Replot the graph
    plt.cla()
    subplot.set_xlim(0.1 + x[len(x)-1] - 4, x[len(x)-1])
    subplot.set_ylim(0, 20)
    subplot.plot(x, y, c=line_color)
    graph_canvas.draw()


window = Tk()
window.title("MQTT Dashboard")
window.geometry("1024x720")
window.configure(bg="white")

# Base canvas
canvas = Canvas(window, bg="white", width=720, height=720)
# To erase the border of the canvas
canvas.config(highlightthickness=0)
canvas.place(x=0, y=0)
img = PhotoImage(file="../images/logo_test.png")
canvas.create_image(0, 0, anchor=NW, image=img)

# Temperature canvas
canvas2 = Canvas(window, bg="white", width=100, height=100)
# To erase the border of the canvas
canvas2.config(highlightthickness=0)
canvas2.place(x=50, y=165)
img2 = Image.open("../images/temp.png")
resized_img = img2.resize((100, 100), Image.ANTIALIAS)
img2 = ImageTk.PhotoImage(resized_img)
canvas2.create_image(0, 0, anchor=NW, image=img2)

# Label for temperature
temp_label = Label(window,
                   text=" °C",
                   bg="white",
                   fg="black",
                   font=("Helvetica", 32))

temp_label.place(x=180, y=190)

# Humidity canvas
canvas3 = Canvas(window, bg="white", width=100, height=100)
# To erase the border of the canvas
canvas3.config(highlightthickness=0)
canvas3.place(x=67, y=297)
img3 = Image.open("../images/humidity.png")
resized_img = img3.resize((100, 100), Image.ANTIALIAS)
img3 = ImageTk.PhotoImage(resized_img)
canvas3.create_image(0, 0, anchor=NW, image=img3)

# Label for humidity
hum_label = Label(window,
                   text=" %",
                   bg="white",
                   fg="black",
                   font=("Helvetica", 32))

hum_label.place(x=180, y=325)

# Real time graph
line_color = "r"
fig = Figure(figsize=(4, 3), dpi=100)
t = 0.1
x = [0, 0, 0, 0, 0]
y = [0, 0, 0, 0, 0]
subplot = fig.add_subplot(111)
subplot.plot(x, y, c=line_color)

graph_canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
graph_canvas.draw()
graph_canvas.get_tk_widget().pack(side=BOTTOM)

toolbar = NavigationToolbar2Tk(graph_canvas, window)
toolbar.update()

client = connect_mqtt()
subscribe(client)
client.loop_start()

window.mainloop()
client.loop_stop()
