import random

from paho.mqtt import client as mqtt_client
from tkinter import *
from PIL import Image, ImageTk

from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
from matplotlib.figure import Figure

broker = 'localhost'
port = 1883
temp_topic = "sensor/+/temp"
humidity_topic = "sensor/+/hum"
water_topic = "sensor/+/water"
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
        parsed_msg = ""
        if "water" not in msg.topic:
            split_msg = msg.payload.decode().split("\\")[0]

            char_num = 0
            parsed_msg = ""
            for char in split_msg:
                if char_num < 5:
                    if char.isdigit():
                        parsed_msg += char
                    elif char == ".":
                        parsed_msg += char
                    char_num += 1
        elif "water" in msg.topic:
            i = 0
            for char in msg.payload.decode():
                if i == 0 and char.isdigit():
                    parsed_msg += char
                else:
                    break
        if msg.topic == "sensor/1/temp":
            temp_label.config(text=parsed_msg + "%",
                                fg="black")
            update_graph(msg)
        elif msg.topic == "sensor/1/hum":
            hum_label.config(text=parsed_msg + "%",
                              fg="black")
        elif msg.topic == "sensor/2/temp":
            temp_label_1.config(text=parsed_msg + "%",
                                fg="black")
        elif msg.topic == "sensor/2/hum":
            hum_label_1.config(text=parsed_msg + "%",
                               fg="black")
        elif msg.topic == "sensor/3/temp":
            temp_label_2.config(text=parsed_msg + "%",
                                fg="black")
        elif msg.topic == "sensor/3/hum":
            hum_label_2.config(text=parsed_msg + "%",
                               fg="black")
        elif msg.topic == "sensor/4/temp":
            temp_label_3.config(text=parsed_msg + "%",
                                fg="black")
        elif msg.topic == "sensor/4/hum":
            hum_label_3.config(text=parsed_msg + "%",
                               fg="black")
        elif msg.topic == "sensor/5/temp":
            temp_label_4.config(text=parsed_msg + "%",
                                fg="black")
        elif msg.topic == "sensor/5/hum":
            hum_label_4.config(text=parsed_msg + "%",
                               fg="black")
        elif msg.topic == "sensor/1/water":
            switch_led(parsed_msg)
        elif msg.topic == "sensor/2/water":
            switch_led1(parsed_msg)
        elif msg.topic == "sensor/3/water":
            switch_led2(parsed_msg)
        elif msg.topic == "sensor/4/water":
            switch_led3(parsed_msg)
        elif msg.topic == "sensor/5/water":
            switch_led4(parsed_msg)
        if "water" in msg.topic:
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        else:
            print(f"Received `{parsed_msg}` from `{msg.topic}` topic")

    client.subscribe(temp_topic)
    client.subscribe(humidity_topic)
    client.subscribe(water_topic)
    client.on_message = on_message

def publish(client, status, sensor_num):
    topic = f"sensor/{sensor_num}/status"
    msg = status
    result = client.publish(topic, msg)
    # result: [0, 1]
    status = result[0]
    if status == 0:
        print(f"Send `{msg}` to topic `{topic}`")
    else:
        print(f"Failed to send message to topic {topic}")

#############
# Dashboard #
#############

def update_graph(msg):
    # Swipe al values to the left
    x[:] = x[1:5] + x[0:1]
    y[:] = y[1:5] + y[0:1]
    # Then update the last value for the graph
    x[len(x) - 1] = float(x[len(x) - 2] + 0.1)
    parsed_msg = ""
    if "water" not in msg.topic:
        split_msg = msg.payload.decode().split("\\")[0]

        char_num = 0
        parsed_msg = ""
        for char in split_msg:
            if char_num < 5:
                if char.isdigit():
                    parsed_msg += char
                elif char == ".":
                    parsed_msg += char
                char_num += 1
    y[len(y) - 1] = float(parsed_msg)

    # Replot the graph
    plt.cla()
    subplot.set_xlim(0.1 + x[len(x) - 1] - 2, x[len(x) - 1])
    subplot.set_ylim(20, 40)
    subplot.plot(x, y, c=line_color)
    graph_canvas.draw()


window = Tk()
window.title("MQTT Dashboard")
window.geometry("1920x1080")
window.configure(bg="grey")

# Base canvas
canvas = Canvas(window, bg="grey", width=1920, height=1080)
# To erase the border of the canvas
canvas.config(highlightthickness=0)
canvas.place(x=65, y=10)
img = Image.open("../images/upm_logo.png")
resized_img = img.resize((330, 130), Image.ANTIALIAS)
img = ImageTk.PhotoImage(resized_img)
canvas.create_image(0, 0, anchor=NW, image=img)

# Temperature canvas 1
canvas2 = Canvas(window, bg="grey", width=100, height=100)
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
                   bg="grey",
                   fg="black",
                   font=("Helvetica", 32))

temp_label.place(x=180, y=190)

# Temperature canvas 2
canvas2_1 = Canvas(window, bg="grey", width=100, height=100)
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
                     bg="grey",
                     fg="black",
                     font=("Helvetica", 32))

temp_label_1.place(x=510, y=190)

# Temperature canvas 3
canvas2_2 = Canvas(window, bg="grey", width=100, height=100)
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
                     bg="grey",
                     fg="black",
                     font=("Helvetica", 32))

temp_label_2.place(x=840, y=190)

# Temperature canvas 4
canvas2_3 = Canvas(window, bg="grey", width=100, height=100)
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
                     bg="grey",
                     fg="black",
                     font=("Helvetica", 32))

temp_label_3.place(x=1170, y=190)

# Temperature canvas 5
canvas2_4 = Canvas(window, bg="grey", width=100, height=100)
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
                     bg="grey",
                     fg="black",
                     font=("Helvetica", 32))

temp_label_4.place(x=1500, y=190)

# Humidity canvas 1
canvas3 = Canvas(window, bg="grey", width=100, height=100)
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
                  bg="grey",
                  fg="black",
                  font=("Helvetica", 32))

hum_label.place(x=180, y=325)

# Humidity canvas 2
canvas3_1 = Canvas(window, bg="grey", width=100, height=100)
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
                    bg="grey",
                    fg="black",
                    font=("Helvetica", 32))

hum_label_1.place(x=510, y=325)

# Humidity canvas 3
canvas3_2 = Canvas(window, bg="grey", width=100, height=100)
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
                    bg="grey",
                    fg="black",
                    font=("Helvetica", 32))

hum_label_2.place(x=840, y=325)

# Humidity canvas 4
canvas3_3 = Canvas(window, bg="grey", width=100, height=100)
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
                    bg="grey",
                    fg="black",
                    font=("Helvetica", 32))

hum_label_3.place(x=1170, y=325)

# Humidity canvas 5
canvas3_4 = Canvas(window, bg="grey", width=100, height=100)
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
                    bg="grey",
                    fg="black",
                    font=("Helvetica", 32))

hum_label_4.place(x=1500, y=325)


def switch():
    global is_on
    if is_on:
        on_button.config(image=off)
        print("Button is off now")
        publish(client, "0", "1")
        is_on = False
    else:
        on_button.config(image=on)
        print("Button is On now")
        publish(client, "1", "1")
        is_on = True


is_on = False
on = Image.open("../images/button_on.png")
resized_img = on.resize((100, 100), Image.ANTIALIAS)
on = ImageTk.PhotoImage(resized_img)

off = Image.open("../images/button_off.png")
resized_img = off.resize((100, 100), Image.ANTIALIAS)
off = ImageTk.PhotoImage(resized_img)
# Create A Button
on_button = Button(window, image=off, bd=10,
                   command=switch)
on_button.place(x=57, y=480)


def switch1():
    global is_on1
    if is_on1:
        on_button_1.config(image=off_1)
        print("Button1 is off now")
        publish(client, "0", "2")
        is_on1 = False
    else:
        on_button_1.config(image=on_1)
        print("Button1 is On now")
        publish(client, "1", "2")
        is_on1 = True


is_on1 = False
on_1 = Image.open("../images/button_on.png")
resized_img = on_1.resize((100, 100), Image.ANTIALIAS)
on_1 = ImageTk.PhotoImage(resized_img)

off_1 = Image.open("../images/button_off.png")
resized_img = off_1.resize((100, 100), Image.ANTIALIAS)
off_1 = ImageTk.PhotoImage(resized_img)
# Create A Button
on_button_1 = Button(window, image=off_1, bd=10,
                     command=switch1)
on_button_1.place(x=387, y=480)

def switch2():
    global is_on2
    if is_on2:
        on_button_2.config(image=off_2)
        print("Button2 is off now")
        publish(client, "0", "3")
        is_on2 = False
    else:
        on_button_2.config(image=on_2)
        print("Button2 is On now")
        publish(client, "1", "3")
        is_on2 = True


is_on2 = False
on_2 = Image.open("../images/button_on.png")
resized_img = on_2.resize((100, 100), Image.ANTIALIAS)
on_2 = ImageTk.PhotoImage(resized_img)

off_2 = Image.open("../images/button_off.png")
resized_img = off_2.resize((100, 100), Image.ANTIALIAS)
off_2 = ImageTk.PhotoImage(resized_img)
# Create A Button
on_button_2 = Button(window, image=off_2, bd=10,
                     command=switch2)
on_button_2.place(x=717, y=480)

def switch3():
    global is_on3
    if is_on3:
        on_button_3.config(image=off_3)
        print("Button3 is off now")
        publish(client, "0", "4")
        is_on3 = False
    else:
        on_button_3.config(image=on_3)
        print("Button3 is On now")
        publish(client, "1", "4")
        is_on3 = True


is_on3 = False
on_3 = Image.open("../images/button_on.png")
resized_img = on_3.resize((100, 100), Image.ANTIALIAS)
on_3 = ImageTk.PhotoImage(resized_img)

off_3 = Image.open("../images/button_off.png")
resized_img = off_3.resize((100, 100), Image.ANTIALIAS)
off_3 = ImageTk.PhotoImage(resized_img)
# Create A Button
on_button_3 = Button(window, image=off_3, bd=10,
                     command=switch3)
on_button_3.place(x=1047, y=480)

def switch4():
    global is_on4
    if is_on4:
        on_button_4.config(image=off_4)
        print("Button4 is off now")
        publish(client, "0", "5")
        is_on4 = False
    else:
        on_button_4.config(image=on_4)
        print("Button4 is On now")
        publish(client, "1", "5")
        is_on4 = True


is_on4 = False
on_4 = Image.open("../images/button_on.png")
resized_img = on_4.resize((100, 100), Image.ANTIALIAS)
on_4 = ImageTk.PhotoImage(resized_img)

off_4 = Image.open("../images/button_off.png")
resized_img = off_4.resize((100, 100), Image.ANTIALIAS)
off_4 = ImageTk.PhotoImage(resized_img)
# Create A Button
on_button_4 = Button(window, image=off_4, bd=10,
                     command=switch4)
on_button_4.place(x=1377, y=480)

def switch_led(msg):
    global r_is_on
    if msg == "1":
        canvasl.itemconfig(ron_button, image=ron)
        r_is_on = False
    elif msg == "0":
        canvasl.itemconfig(ron_button, image=roff)
        r_is_on = True
# Watering led 1
r_is_on = False
canvasl = Canvas(window, bg="grey", width=75, height=75)
ron = Image.open("../images/led_on.png")
resized_img = ron.resize((75, 75), Image.ANTIALIAS)
ron = ImageTk.PhotoImage(resized_img)

roff = Image.open("../images/led_off.png")
resized_img = roff.resize((75, 75), Image.ANTIALIAS)
roff = ImageTk.PhotoImage(resized_img)
# Create A Button
canvasl.config(highlightthickness=0)
canvasl.place(x=77, y=630)
ron_button = canvasl.create_image(0, 0, anchor=NW, image=roff)

def switch_led1(msg):
    global r_is_on_1
    if msg == "1":
        canvasl_1.itemconfig(ron_button_1, image=ron_1)
        r_is_on_1 = False
    elif msg == "0":
        canvasl_1.itemconfig(ron_button_1, image=roff_1)
        r_is_on_1 = True
# Watering led 2
r_is_on_1 = False
canvasl_1 = Canvas(window, bg="grey", width=75, height=75)
ron_1 = Image.open("../images/led_on.png")
resized_img = ron_1.resize((75, 75), Image.ANTIALIAS)
ron_1 = ImageTk.PhotoImage(resized_img)

roff_1 = Image.open("../images/led_off.png")
resized_img = roff_1.resize((75, 75), Image.ANTIALIAS)
roff_1 = ImageTk.PhotoImage(resized_img)
# Create A Button

canvasl_1.config(highlightthickness=0)
canvasl_1.place(x=407, y=630)
ron_button_1 = canvasl_1.create_image(0, 0, anchor=NW, image=roff_1)


def switch_led2(msg):
    global r_is_on_2
    if msg == "1":
        canvasl_2.itemconfig(ron_button_2, image=ron_2)
        r_is_on_2 = False
    elif msg == "0":
        canvasl_2.itemconfig(ron_button_2, image=roff_2)
        r_is_on_2 = True
# Watering led 3
r_is_on_2 = False
canvasl_2 = Canvas(window, bg="grey", width=75, height=75)
ron_2 = Image.open("../images/led_on.png")
resized_img = ron_2.resize((75, 75), Image.ANTIALIAS)
ron_2 = ImageTk.PhotoImage(resized_img)

roff_2 = Image.open("../images/led_off.png")
resized_img = roff_2.resize((75, 75), Image.ANTIALIAS)
roff_2 = ImageTk.PhotoImage(resized_img)
# Create A Button
canvasl_2.config(highlightthickness=0)
canvasl_2.place(x=737, y=630)
ron_button_2 = canvasl_2.create_image(0, 0, anchor=NW, image=roff_2)

def switch_led3(msg):
    global r_is_on_3
    if msg == "1":
        canvasl_3.itemconfig(ron_button_3, image=ron_3)
        r_is_on_3 = False
    elif msg == "0":
        canvasl_3.itemconfig(ron_button_3, image=roff_3)
        r_is_on_3 = True
# Watering led 4
r_is_on_3 = False
canvasl_3 = Canvas(window, bg="grey", width=75, height=75)
ron_3 = Image.open("../images/led_on.png")
resized_img = ron_3.resize((75, 75), Image.ANTIALIAS)
ron_3 = ImageTk.PhotoImage(resized_img)

roff_3 = Image.open("../images/led_off.png")
resized_img = roff_3.resize((75, 75), Image.ANTIALIAS)
roff_3 = ImageTk.PhotoImage(resized_img)
# Create A Button
canvasl_3.config(highlightthickness=0)
canvasl_3.place(x=1067, y=630)
ron_button_3 = canvasl_3.create_image(0, 0, anchor=NW, image=roff_3)

def switch_led4(msg):
    global r_is_on_4
    if msg == "1":
        canvasl_4.itemconfig(ron_button_4, image=ron_4)
        r_is_on_4 = False
    elif msg == "0":
        canvasl_4.itemconfig(ron_button_4, image=roff_4)
        r_is_on_4 = True
# Watering led 5
r_is_on_4= False
canvasl_4 = Canvas(window, bg="grey", width=75, height=75)
ron_4 = Image.open("../images/led_on.png")
resized_img = ron_4.resize((75, 75), Image.ANTIALIAS)
ron_4 = ImageTk.PhotoImage(resized_img)

roff_4 = Image.open("../images/led_off.png")
resized_img = roff_4.resize((75, 75), Image.ANTIALIAS)
roff_4 = ImageTk.PhotoImage(resized_img)
# Create A Button
canvasl_4.config(highlightthickness=0)
canvasl_4.place(x=1397, y=630)
ron_button_4 = canvasl_4.create_image(0, 0, anchor=NW, image=roff_4)

# Real time graph
line_color = "r"
fig = Figure(figsize=(4, 3), dpi=100)
fig.patch.set_facecolor("grey")
fig.suptitle("Sensor1 temperature")
t = 0.1
x = [0, 0, 0, 0, 0]
y = [0, 0, 0, 0, 0]
subplot = fig.add_subplot(111)
subplot.plot(x, y, c=line_color)

graph_canvas = FigureCanvasTkAgg(fig, master=window)  # A tk.DrawingArea.
graph_canvas.draw()
graph_canvas.get_tk_widget().pack(side=BOTTOM)

client = connect_mqtt()
subscribe(client)
client.loop_start()

window.mainloop()
client.loop_stop()
