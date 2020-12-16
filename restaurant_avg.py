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

name = ["01.png","02.png","03.png","04.png","05.png","06.png","07.png","08.png","09.png","010.png",
            "011.png","012.png","013.png","014.png","015.png","016.png","017.png","018.png","019.png","020.png"]


# 預計20間餐廳用迴圈跑，但目前最後一間餐廳會覆蓋前面，尚未解決
'''
for i in range(20):
    img = Image.open(name[i]).resize((50, 50)).save(name[i])  # 調整大小
    img_1 = ImageTk.PhotoImage(Image.open(name[i]))
    img_1 = img_1.subsample(x[i], y[i])

    cv.create_image(x[i], y[i], image=img_1)
 '''   

# 改圖片大小、將圖放在其座標上
img = Image.open('01.png').resize((50, 50)).save('01.png')
img_1 = ImageTk.PhotoImage(Image.open("01.png"))
cv.create_image(x[0], y[0], image=img_1)

img = Image.open('02.png').resize((50, 50)).save('02.png')
img_2 = ImageTk.PhotoImage(Image.open("02.png"))
cv.create_image(x[1], y[1], image=img_2)

img = Image.open('03.png').resize((50, 50)).save('03.png')
img_3 = ImageTk.PhotoImage(Image.open("03.png"))
cv.create_image(x[2], y[2], image=img_3)

img = Image.open('04.png').resize((50, 50)).save('04.png')
img_4 = ImageTk.PhotoImage(Image.open("04.png"))
cv.create_image(x[3], y[3], image=img_4)

img = Image.open('05.png').resize((50, 50)).save('05.png')
img_5 = ImageTk.PhotoImage(Image.open("05.png"))
cv.create_image(x[4], y[4], image=img_5)

img = Image.open('06.png').resize((50, 50)).save('06.png')
img_6 = ImageTk.PhotoImage(Image.open("06.png"))
cv.create_image(x[5], y[5], image=img_6)

img = Image.open('07.png').resize((50, 50)).save('07.png')
img_7 = ImageTk.PhotoImage(Image.open("07.png"))
cv.create_image(x[6], y[6], image=img_7)

img = Image.open('08.png').resize((50, 50)).save('08.png')
img_8 = ImageTk.PhotoImage(Image.open("08.png"))
cv.create_image(x[7], y[7], image=img_8)

img = Image.open('09.png').resize((50, 50)).save('09.png')
img_9 = ImageTk.PhotoImage(Image.open("09.png"))
cv.create_image(x[8], y[8], image=img_9)

img = Image.open('010.png').resize((50, 50)).save('010.png')
img_10 = ImageTk.PhotoImage(Image.open("010.png"))
cv.create_image(x[9], y[9], image=img_10)

img = Image.open('011.png').resize((50, 50)).save('011.png')
img_11 = ImageTk.PhotoImage(Image.open("011.png"))
cv.create_image(x[10], y[10], image=img_11)

img = Image.open('012.png').resize((50, 50)).save('012.png')
img_12 = ImageTk.PhotoImage(Image.open("012.png"))
cv.create_image(x[11], y[11], image=img_12)

img = Image.open('013.png').resize((50, 50)).save('013.png')
img_13 = ImageTk.PhotoImage(Image.open("013.png"))
cv.create_image(x[12], y[12], image=img_13)

img = Image.open('014.png').resize((50, 50)).save('014.png')
img_14 = ImageTk.PhotoImage(Image.open("014.png"))
cv.create_image(x[13], y[13], image=img_14)

img = Image.open('015.png').resize((50, 50)).save('015.png')
img_15 = ImageTk.PhotoImage(Image.open("015.png"))
cv.create_image(x[14], y[14], image=img_15)

img = Image.open('016.png').resize((50, 50)).save('016.png')
img_16 = ImageTk.PhotoImage(Image.open("016.png"))
cv.create_image(x[15], y[15], image=img_16)

img = Image.open('017.png').resize((50, 50)).save('017.png')
img_17 = ImageTk.PhotoImage(Image.open("017.png"))
cv.create_image(x[16], y[16], image=img_17)

img = Image.open('018.png').resize((50, 50)).save('018.png')
img_18 = ImageTk.PhotoImage(Image.open("018.png"))
cv.create_image(x[17], y[17], image=img_18)

img = Image.open('019.png').resize((50, 50)).save('019.png')
img_19 = ImageTk.PhotoImage(Image.open("09.png"))
cv.create_image(x[18], y[18], image=img_19)

img = Image.open('020.png').resize((50, 50)).save('020.png')
img_20 = ImageTk.PhotoImage(Image.open("020.png"))
cv.create_image(x[19], y[19], image=img_20)

cv.pack()
root.mainloop()