import random

from paho.mqtt import client as mqtt_client
from tkinter import *
from PIL import Image, ImageTk

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure


broker = 'localhost'
port = 1883
temp_topic = "sensor/+/temp"
humidity_topic = "sensor/+/hum"
# generate client ID with public prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100000)}'
username = 'local'
password = 'localpw'


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
        if msg.topic == "sensor/1/temp":
            update_dashboard_temp(msg)
            update_graph(msg)
        elif msg.topic == "sensor/1/hum":
            update_dashboard_humidity(msg)
        elif msg.topic == "sensor/2/temp":
            temp_label_1.config(text=msg.payload.decode() + "%",
                             fg="black")
        elif msg.topic == "sensor/2/hum":
            hum_label_1.config(text=msg.payload.decode() + "%",
                             fg="black")
        elif msg.topic == "sensor/3/temp":
            temp_label_2.config(text=msg.payload.decode() + "%",
                             fg="black")
        elif msg.topic == "sensor/3/hum":
            hum_label_2.config(text=msg.payload.decode() + "%",
                             fg="black")
        elif msg.topic == "sensor/4/temp":
            temp_label_3.config(text=msg.payload.decode() + "%",
                             fg="black")
        elif msg.topic == "sensor/4/hum":
            hum_label_3.config(text=msg.payload.decode() + "%",
                             fg="black")
        elif msg.topic == "sensor/5/temp":
            temp_label_4.config(text=msg.payload.decode() + "%",
                             fg="black")
        elif msg.topic == "sensor/5/hum":
            hum_label_4.config(text=msg.payload.decode() + "%",
                             fg="black")
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
    # Swipe al values to the left
    x[:] = x[1:5]+x[0:1]
    y[:] = y[1:5]+y[0:1]
    # Then update the last value for the graph
    x[len(x) - 1] = float(x[len(x) - 2] + 0.1)
    y[len(y) - 1] = float(msg.payload.decode())

    # Replot the graph
    plt.cla()
    subplot.set_xlim(0.1 + x[len(x)-1] - 2, x[len(x)-1])
    subplot.set_ylim(20, 40)
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

# Temperature canvas 1
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

# Temperature canvas 2
canvas2_1 = Canvas(window, bg="white", width=100, height=100)
# To erase the border of the canvas
canvas2_1.config(highlightthickness=0)
canvas2_1.place(x=380, y=165)
img2_1 = Image.open("../images/temp.png")
resized_img = img2_1.resize((100, 100), Image.ANTIALIAS)
img2_1 = ImageTk.PhotoImage(resized_img)
canvas2_1.create_image(0, 0, anchor=NW, image=img2_1)

# Label for temperature
temp_label_1 = Label(window,
                   text=" °C",
                   bg="white",
                   fg="black",
                   font=("Helvetica", 32))

temp_label_1.place(x=510, y=190)

# Temperature canvas 3
canvas2_2 = Canvas(window, bg="white", width=100, height=100)
# To erase the border of the canvas
canvas2_2.config(highlightthickness=0)
canvas2_2.place(x=710, y=165)
img2_2 = Image.open("../images/temp.png")
resized_img = img2_2.resize((100, 100), Image.ANTIALIAS)
img2_2 = ImageTk.PhotoImage(resized_img)
canvas2_2.create_image(0, 0, anchor=NW, image=img2_2)

# Label for temperature
temp_label_2 = Label(window,
                   text=" °C",
                   bg="white",
                   fg="black",
                   font=("Helvetica", 32))

temp_label_2.place(x=840, y=190)

# Temperature canvas 4
canvas2_3 = Canvas(window, bg="white", width=100, height=100)
# To erase the border of the canvas
canvas2_3.config(highlightthickness=0)
canvas2_3.place(x=1040, y=165)
img2_3 = Image.open("../images/temp.png")
resized_img = img2_3.resize((100, 100), Image.ANTIALIAS)
img2_3 = ImageTk.PhotoImage(resized_img)
canvas2_3.create_image(0, 0, anchor=NW, image=img2_3)

# Label for temperature
temp_label_3 = Label(window,
                   text=" °C",
                   bg="white",
                   fg="black",
                   font=("Helvetica", 32))

temp_label_3.place(x=1170, y=190)

# Temperature canvas 5
canvas2_4 = Canvas(window, bg="white", width=100, height=100)
# To erase the border of the canvas
canvas2_4.config(highlightthickness=0)
canvas2_4.place(x=1370, y=165)
img2_4 = Image.open("../images/temp.png")
resized_img = img2_4.resize((100, 100), Image.ANTIALIAS)
img2_4 = ImageTk.PhotoImage(resized_img)
canvas2_4.create_image(0, 0, anchor=NW, image=img2_4)

# Label for temperature
temp_label_4 = Label(window,
                   text=" °C",
                   bg="white",
                   fg="black",
                   font=("Helvetica", 32))

temp_label_4.place(x=1500, y=190)

# Humidity canvas 1
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

# Humidity canvas 2
canvas3_1 = Canvas(window, bg="white", width=100, height=100)
# To erase the border of the canvas
canvas3_1.config(highlightthickness=0)
canvas3_1.place(x=397, y=297)
img3_1 = Image.open("../images/humidity.png")
resized_img = img3_1.resize((100, 100), Image.ANTIALIAS)
img3_1 = ImageTk.PhotoImage(resized_img)
canvas3_1.create_image(0, 0, anchor=NW, image=img3_1)

# Label for humidity
hum_label_1 = Label(window,
                   text=" %",
                   bg="white",
                   fg="black",
                   font=("Helvetica", 32))

hum_label_1.place(x=510, y=325)

# Humidity canvas 3
canvas3_2 = Canvas(window, bg="white", width=100, height=100)
# To erase the border of the canvas
canvas3_2.config(highlightthickness=0)
canvas3_2.place(x=727, y=297)
img3_2 = Image.open("../images/humidity.png")
resized_img = img3_2.resize((100, 100), Image.ANTIALIAS)
img3_2 = ImageTk.PhotoImage(resized_img)
canvas3_2.create_image(0, 0, anchor=NW, image=img3_2)

# Label for humidity
hum_label_2 = Label(window,
                   text=" %",
                   bg="white",
                   fg="black",
                   font=("Helvetica", 32))

hum_label_2.place(x=840, y=325)

# Humidity canvas 4
canvas3_3 = Canvas(window, bg="white", width=100, height=100)
# To erase the border of the canvas
canvas3_3.config(highlightthickness=0)
canvas3_3.place(x=1057, y=297)
img3_3 = Image.open("../images/humidity.png")
resized_img = img3_3.resize((100, 100), Image.ANTIALIAS)
img3_3 = ImageTk.PhotoImage(resized_img)
canvas3_3.create_image(0, 0, anchor=NW, image=img3_3)

# Label for humidity
hum_label_3 = Label(window,
                   text=" %",
                   bg="white",
                   fg="black",
                   font=("Helvetica", 32))

hum_label_3.place(x=1170, y=325)

# Humidity canvas 5
canvas3_4 = Canvas(window, bg="white", width=100, height=100)
# To erase the border of the canvas
canvas3_4.config(highlightthickness=0)
canvas3_4.place(x=1387, y=297)
img3_4 = Image.open("../images/humidity.png")
resized_img = img3_4.resize((100, 100), Image.ANTIALIAS)
img3_4 = ImageTk.PhotoImage(resized_img)
canvas3_4.create_image(0, 0, anchor=NW, image=img3_4)

# Label for humidity
hum_label_4 = Label(window,
                   text=" %",
                   bg="white",
                   fg="black",
                   font=("Helvetica", 32))

hum_label_4.place(x=1500, y=325)

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
