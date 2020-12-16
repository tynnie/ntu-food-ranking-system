from tkinter import *
from PIL import ImageTk, Image

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
current_image_number = 0
img = PhotoImage(file = "01.png")
my_image = my_canvas.create_image(555,355, anchor=NW, image=img)



def on_click():
    global current_image_number, img
    images = ["01.png","02.png","03.png","04.png","05.png","06.png","07.png","08.png","09.png","10.png","11.png","12.png","13.png","14.png","15.png","16.png","17.png","18.png","19.png","20.png"]
    res_name = ["溏老鴨平價火鍋", "鍋in", "YU POKE", "親來食堂", "阿英滷肉飯","麥子磨麵", "I'm PASTA", "七里亭", "上賀麵食館", "韓庭州","五九麵館", "瑪莉珍", "采味食光", "季丼屋", "韓天閣","鱷吐司", "小飯廳", "雲泰泰式料理", "稻咖哩","極麵屋"]
    current_image_number += 1
    if current_image_number == len(images):
        current_image_number = 0
    my_canvas.delete("progress")
    my_canvas.delete(my_image)
    progress_label.config(font=("Purisa", 20),text="已評分或跳過的餐廳：" + str(current_image_number) + " / 20")
    res_label.config(font=("Purisa", 20),text="餐廳：" + res_name[current_image_number])
    img = ImageTk.PhotoImage(file=images[current_image_number])
    my_image_next = my_canvas.create_image(555,355, anchor=NW, image=img)
    

def move(e):
    global img, my_image
    images = ["01.png","02.png","03.png","04.png","05.png","06.png","07.png","08.png","09.png","10.png","11.png","12.png","13.png","14.png","15.png","16.png","17.png","18.png","19.png","20.png"]
    img = ImageTk.PhotoImage(file=images[current_image_number])
    my_image = my_canvas.create_image(e.x,e.y, image=img)
    #my_label.config(text="Coordinate x: " + str(e.x) + "  | y: " + str(e.y))

button_skip = Button(root, text="SKIP", command=on_click)
button_skip.pack(side='left', ipadx=50, padx=20)
button_save = Button(root, text="SUBMUT", command=on_click)
button_save.pack(side='left', ipadx=50, padx=20)
#my_label = Label(root, text="")
#my_label.pack(side='left', ipadx=50, padx=20)
progress_label = Label(root, text="",fg="red")
progress_label.pack(side='left', ipadx=50, padx=20)
res_label = Label(root, text="",fg="black")
res_label.pack(side='left', ipadx=50, padx=20)


my_canvas.bind("<B1-Motion>", move)

root.mainloop()