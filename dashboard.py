from tkinter import *
from PIL import Image, ImageTk

window = Tk()
window.title("MQTT Dashboard")
window.geometry("720x720")
window.configure(bg="white")

canvas = Canvas(window, bg="white", width=720, height=720)
# To erase the border of the canvas
canvas.config(highlightthickness=0)
canvas.place(x=0, y=0)
img = PhotoImage(file="images/logo_test.png")
canvas.create_image(0, 0, anchor=NW, image=img)

canvas2 = Canvas(window, bg="white", width=100, height=100)
# To erase the border of the canvas
canvas2.config(highlightthickness=0)
canvas2.place(x=50, y=165)
img2 = Image.open("images/temp.png")
resized_img = img2.resize((100, 100), Image.ANTIALIAS)
img2 = ImageTk.PhotoImage(resized_img)
canvas2.create_image(0, 0, anchor=NW, image=img2)

window.mainloop()
