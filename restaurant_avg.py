import pygsheets
import tkinter as tk
from PIL import ImageTk,Image

gc = pygsheets.authorize(service_file='/Users/bonnie/Desktop/Google python.json')  # 讀取金鑰

sht = gc.open_by_url('https://docs.google.com/spreadsheets/d/13Fh7Y7yw4pUvHfYCu3z1zZjCVC0UIYU9_X1uaijgU-E/edit#gid=0')
wks_list = sht.worksheets()

wks = sht[0]  # 確認為哪一個sheet

x = []
y = []
# 餐廳平均數座標
for i in range(20):
    X = wks.cell('A'+str(i+1))  # 讀取該表單的X值
    x_val = X.value  # 只取該格的值
    x.append(x_val)
    Y = wks.cell('B'+str(i+1))  # 讀取該表單的Y值
    y_val = Y.value
    y.append(y_val)


root = tk.Tk()

APP_WIDTH = 1200
APP_HEIGHT = 800

# canva創建畫布
cv = tk.Canvas(width=APP_WIDTH, height=APP_HEIGHT, bg="white")
cv.create_line(100, 400, 1100, 400, fill="gray", width=5)
cv.create_line(600, 100, 600, 700, fill="gray", width=5)
cv.create_text(50, 400, fill="Gray", font=("Purisa", 30), text="難吃")
cv.create_text(1150, 400, fill="Gray", font=("Purisa", 30), text="好吃")
cv.create_text(600, 50, fill="Gray", font=("Purisa", 30), text="健康")
cv.create_text(600, 750, fill="Gray", font=("Purisa", 30), text="不健康")


img_ref = []  # 餐廳圖片list
name = ["01.png","02.png","03.png","04.png","05.png","06.png","07.png","08.png","09.png","010.png",
            "011.png","012.png","013.png","014.png","015.png","016.png","017.png","018.png","019.png","020.png"]

# 在canva上加上圖片logo
for i in range(20):
    img = Image.open(name[i]).resize((50, 50)).save(name[i])  # 調整圖片大小
    img_1 = ImageTk.PhotoImage(Image.open(name[i]))
    cv.create_image(x[i], y[i], image=img_1)  # 將img_ref list裡的餐廳放上canva
    img_ref.append(img_1)  # 存放圖片

cv.pack()
root.mainloop()
