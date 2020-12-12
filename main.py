from tkinter import *

root = Tk()
root.title("台大附近吃什麼？")
root.geometry("1200x800")

w = 1200
h = 800
x = w/2
y = h/2

my_canvas = Canvas(root, width=w, height=h, bg="white")
my_canvas.pack(pady=20)
my_canvas.create_line(100, 400, 1100, 400, fill="gray",width=5)
my_canvas.create_line(600, 100, 600, 700, fill="gray",width=5) 
my_canvas.create_text(50,400,fill="Gray",font=("Purisa", 30),text="難吃")
my_canvas.create_text(1150,400,fill="Gray",font=("Purisa", 30),text="好吃")
my_canvas.create_text(600,50,fill="Gray",font=("Purisa", 30),text="健康")
my_canvas.create_text(600,750,fill="Gray",font=("Purisa", 30),text="不健康")

img = PhotoImage(file = "1.png")
my_image = my_canvas.create_image(600,400, anchor=NW, image=img)
current_image_number = 0

def on_click():
    global current_image_number
    current_image_number += 1
    if current_image_number == len(images):
        current_image_number = 0

    
#image_id = my_canvas.create_image(600, 400, anchor='nw', image=images[current_image_number])

def move(e):
    global img
    images = ["1.png","2.png"]
    img = PhotoImage(file=images[current_image_number])
    #img=images[current_image_number]
    my_image = my_canvas.create_image(e.x,e.y, image=img)
    my_label.config(text="Coordinate x: " + str(e.x) + "  | y: " + str(e.y))
button_skip = Button(root, text="SKIP", command=on_click)
button_skip.pack(side='left', ipadx=50, padx=200)
button_save = Button(root, text="SUBMUT", command=on_click)
button_save.pack(side='left', ipadx=50, padx=200)
my_label = Label(root, text="")
my_label.pack(pady=20)

my_canvas.bind("<B1-Motion>", move)

root.mainloop()