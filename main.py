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
    if current_image_number == image_num-1:
        upload_data(data)
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
        my_image = my_canvas.create_image(455, 265, anchor=tk.NW, image=img)


# 設定一下拖曳事件
def move(event):
    global img, my_image, xpos, ypos
    img = tk.PhotoImage(file=images[current_image_number])
    my_image = my_canvas.create_image(event.x, event.y, image=img)
    # 儲存一下物件最後的座標
    xpos = event.x
    ypos = event.y


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
        res_img = Image.open(res_img_path).resize((50, 50))
        res_img.load()
        photoimg = ImageTk.PhotoImage(res_img)
        images.append(photoimg)  # debug用，沒什麼function
        my_canvas.create_image(int(line["x"]), int(line["y"]), anchor=tk.NW, image=photoimg)


# 設定圖檔路徑
IMAGE_PATH = "ref/img/"
image_num = 20
images = ["".join([IMAGE_PATH, str(n), ".png"]) for n in range(1, image_num+1)]
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

# 介面基本設定
root = tk.Tk()
root.title("台大附近吃什麼？")
root.geometry("1080x720")

w = 1080
h = 720
x = w / 2
y = h / 2
current_image_number = 0

# 畫出視窗
my_canvas = tk.Canvas(root, width=w, height=h, bg="white")
my_canvas.pack(pady=20)

# 畫出座標軸及文字
my_canvas.create_line(100, 360, 980, 360, fill="gray", width=5)
my_canvas.create_line(540, 100, 540, 620, fill="gray", width=5)
my_canvas.create_text(50, 360, fill="Gray", font=("Purisa", 30), text="難吃")
my_canvas.create_text(1030, 360, fill="Gray", font=("Purisa", 30), text="好吃")
my_canvas.create_text(540, 50, fill="Gray", font=("Purisa", 30), text="健康")
my_canvas.create_text(540, 680, fill="Gray", font=("Purisa", 30), text="不健康")
img = tk.PhotoImage(file=images[0])
my_image = my_canvas.create_image(455, 265, anchor=tk.NW, image=img)

# create buttons
button_skip = tk.Button(root, text="SKIP", command=on_click)
button_skip.pack(fill="both", expand=True, side='left', ipadx=50, padx=20)
button_save = tk.Button(root, text="SUBMIT", command=on_click)
button_save.pack(fill="both", expand=True, side='left', ipadx=50, padx=20)
button_quit = tk.Button(root, text="QUIT", command=root.destroy)  # 之後記得再新增一個直接show出結果的button
button_quit.pack(fill="both", expand=True, side='left', ipadx=50, padx=20)

# create labels
progress_label = tk.Label(root, text="", fg="red")
progress_label.pack(fill="both", expand=True, side='left', ipadx=50, padx=20)
res_label = tk.Label(root, text="", fg="black")
res_label.pack(fill="both", expand=True, side='left', ipadx=50, padx=20)
progress_label.config(font=("Purisa", 20), text="已評分或跳過的餐廳：" + str(current_image_number) + " / 20")
res_label.config(font=("Purisa", 20), text="目前評分餐廳：" + restaurant[current_image_number][1])

# 套用一下拖曳事件
my_canvas.bind("<B1-Motion>", move)
root.mainloop()
