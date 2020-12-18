import tkinter as tk
from PIL import ImageTk, Image
import pygsheets
import csv
import pandas as pd


# 設定按鈕事件
def on_click():
    global current_image_number, img, my_image, xpos, ypos
    # 儲存已評分餐廳資訊
    item = [str(restaurant[current_image_number][0]), xpos, ypos]
    data.append(item)
    # 重新設定座標
    xpos = 0
    ypos = 0
    # 如果已經是最後一家，就顯示結果
    if current_image_number == IMAGE_NUM-1:
        # upload_data(data)
        # 刪除畫面上現有的物件
        my_canvas.delete("progress")
        my_canvas.delete(my_image)
        # 顯示評價進度
        current_image_number += 1
        progress_label.config(font=("Purisa", 20), text="已評分或跳過的餐廳：" + str(current_image_number) + " / 20")
        # 因為要顯示結果了，不需要再知道店名
        res_label.destroy()
        # 顯示一下結果
        show_result(read_data())
        # my_canvas.destroy()
        # new_can()

    # 如果還不是最後一家，就繼續進行評分
    else:
        current_image_number += 1
        # 刪除畫面上現有的物件
        my_canvas.delete("progress")
        my_canvas.delete(my_image)
        # 顯示評價進度
        progress_label.config(font=("Purisa", 20), text="已評分或跳過的餐廳：" + str(current_image_number) + " / 20")
        res_label.config(font=("Purisa", 20), text="目前評分餐廳：" + restaurant[current_image_number][1])
        img = tk.PhotoImage(file=images[current_image_number])
        my_image = my_canvas.create_image(INIT_X-90, INIT_Y-90, anchor=tk.NW, image=img)


# 設定一下拖曳事件
def move(event):
    global img, my_image, xpos, ypos
    img = tk.PhotoImage(file=images[current_image_number])
    my_image = my_canvas.create_image(event.x, event.y, image=img)
    # 儲存一下物件最後的座標
    xpos = event.x
    ypos = event.y
    print(event.x, event.y)


# 設定一下請求資料庫的方式
def connect_db():
    gc = pygsheets.authorize(service_file='ref/client_secret.json')
    sh = gc.open('NTU_rating')
    wks = sh[0]
    wks = sh.worksheet_by_title('data')
    cells = wks.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
    return wks, cells


# upload data to Google spreadsheet
def upload_data(d):
    columns = ["index", "x", "y"]
    last_row = len(connect_db()[1])
    wks = connect_db()[0]

    if len(wks.get_as_df()) == 0:
        wks.insert_rows(row=0, number=1, values=columns)
        wks.insert_rows(last_row, number=1, values=data)
    else:
        wks.insert_rows(last_row, number=1, values=data)


# fetch data from Google spreadsheet
def read_data():
    wks = connect_db()[0]
    df = wks.get_as_df()
    # 算一下平均
    df = df.groupby(['index']).mean().reset_index()
    return df


# 顯示結果
def show_result(s):
    for index, line in s.iterrows():
        res_img_path = images[int(line["index"])-1]
        res_img = Image.open(res_img_path).resize((75, 75))
        res_img.load()
        photoimg = ImageTk.PhotoImage(res_img)
        images.append(photoimg)  # debug用，沒什麼function
        my_canvas.create_image(int(line["x"]), int(line["y"]), anchor=tk.NW, image=photoimg)


# 直接看結果的按鈕
def show_res_btn():
    global current_image_number
    current_image_number = IMAGE_NUM-1
    # 刪除畫面上現有的物件
    my_canvas.delete("progress")
    my_canvas.delete(my_image)
    # 顯示評價進度
    current_image_number += 1
    progress_label.config(font=("Purisa", 20), text="已評分或跳過的餐廳：" + str(current_image_number) + " / 20")
    # 因為要顯示結果了，不需要再知道店名
    res_label.destroy()
    # 顯示一下結果
    show_result(read_data())


def new_can():
    first_canvas = tk.Canvas(root, width=w, height=h, bg="white")
    first_canvas.pack(pady=20)


# 設定圖檔路徑
IMAGE_PATH = "ref/img/"
IMAGE_NUM = 20
images = ["".join([IMAGE_PATH, str(n), ".png"]) for n in range(1, IMAGE_NUM+1)]
# 讀取餐廳基本資訊
with open("ref/restaurant_list.csv") as f:
    next(f)
    r = csv.reader(f)
    restaurant = [tuple(line) for line in r]
# 儲存餐廳位置的list
data = []

# 圖片座標
xpos = 0
ypos = 0

current_image_number = 0

# 介面基本設定
root = tk.Tk()
root.title("台大附近吃什麼？")

# 打開全螢幕
root.overrideredirect(True)
root.overrideredirect(False)
root.attributes('-fullscreen', True)

WINDOW_W = root.winfo_screenwidth()
WINDOW_H = root.winfo_screenheight()
INIT_X = WINDOW_W/2
INIT_Y = WINDOW_H/2
item_pad = 75
root.geometry("{}x{}".format(WINDOW_W, WINDOW_H))

# 畫出視窗
my_canvas = tk.Canvas(root, width=WINDOW_W, height=WINDOW_H, bg="white")
my_canvas.pack(fill='both', expand=True)

# 畫出座標軸及文字
my_canvas.create_line(150, INIT_Y, WINDOW_W-150, INIT_Y, fill="gray", width=5)
my_canvas.create_line(INIT_X, 125, INIT_X, WINDOW_H-125, fill="gray", width=5)
my_canvas.create_text(item_pad, INIT_Y, fill="Gray", font=("Purisa", 30), text="難吃")
my_canvas.create_text(WINDOW_W-item_pad, INIT_Y, fill="Gray", font=("Purisa", 30), text="好吃")
my_canvas.create_text(INIT_X, item_pad, fill="Gray", font=("Purisa", 30), text="健康")
my_canvas.create_text(INIT_X, WINDOW_H-item_pad, fill="Gray", font=("Purisa", 30), text="不健康")
img = tk.PhotoImage(file=images[0])
my_image = my_canvas.create_image(INIT_X-90, INIT_Y-90, anchor=tk.NW, image=img)

# create buttons
button_skip = tk.Button(my_canvas, text="SKIP", command=on_click)
button_skip.place(rely=1.0, relx=1.0, x=-500, y=0, anchor=tk.SE)
button_save = tk.Button(my_canvas, text="SUBMIT", command=on_click)
button_save.place(rely=1.0, relx=1.0, x=-350, y=0, anchor=tk.SE)
button_quit = tk.Button(my_canvas, text="SHOW RESULT", command=show_res_btn)
button_quit.place(rely=1.0, relx=1.0, x=-200, y=0, anchor=tk.SE)
button_quit = tk.Button(my_canvas, text="QUIT", command=root.destroy)
button_quit.place(rely=1.0, relx=1.0, x=-100, y=0, anchor=tk.SE)

# create labels
progress_label = tk.Label(my_canvas, text="", fg="red")
progress_label.place(rely=.035, relx=0.0, x=50, y=0, anchor=tk.NW)
res_label = tk.Label(my_canvas, text="", fg="black")
res_label.place(rely=.07, relx=0.0, x=50, y=0, anchor=tk.NW)
progress_label.config(font=("Purisa", 20), text="已評分或跳過的餐廳：" + str(current_image_number) + " / 20")
res_label.config(font=("Purisa", 20), text="目前評分餐廳：" + restaurant[current_image_number][1])

# 套用一下拖曳事件
my_canvas.bind("<B1-Motion>", move)


root.mainloop()
