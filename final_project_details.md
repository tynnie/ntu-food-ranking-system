# 開發細節

### 系統使用之Python module
```python
import tkinter as tk  # 設定GUI
import tkinter.font as tkfont  # 管理GUI字體
import tkinter.messagebox as tkmb  # GUI的訊息框
import tkinter.ttk as ttk  # GUI有關的其他元件
import time  # 處理與時間相關的任務
import csv  # 處理csv檔案
from PIL import ImageTk, Image  # 處理影像
from sqlalchemy import create_engine, exc  # 連接資料庫
import pandas as pd  # 處理資料
```

### 程式結構
```properties
main.py
    |
    |--共用變數
    |
    |--class Application(tk.Tk) *基本設定*
    |
    |--class StartPage(tk.Frame) *登入頁*
    |
    |--class PageOne(tk.Frame) *評分及結果頁*

```



#### 設定共用變數
```python
　
"""與資料庫相關"""
DB_PATH = "/ref/sql/result.db"

"""與視窗設定相關"""
WINDOW_W = float()  # The width of the window
WINDOW_H = float()  # The height of the window
INIT_X = float()  # The initial x coordinate of the object
INIT_Y = float()  # The initial y coordinate of the object
ITEM_PADDING = 90  # the padding of the objects on the canvas

"""與運算結果相關"""
usr_data = []  # Record usr info
res_img_record = []  # Record img info of the objects on the canvas
data = []  # Record the ranking results
final_res = []  # Save the final results of different filter conditions

"""與視窗物件相關"""
X_POS = 0  # x coordinate of the object
Y_POS = 0  # y coordinate of the object
CURRENT_PLAYER = 0  # Record username
FINISH = False  # Check if the user has completed all ranking tasks
SKIP = False  # Check if the user has skipped all ranking tasks
CURRENT_IMG_NUMBER = 0  # Current order of ranking tasks

"""設定影像清單、餐廳清單"""
# Get the path of all restaurant pics
# e.g. ['ref/img/1.png', 'ref/img/2.png', ...]  
IMAGE_FILE_PATH = "ref/img/"
IMAGE_NUM = 20
images = ["".join([IMAGE_FILE_PATH, str(n), ".png"]) for n in range(1, IMAGE_NUM + 1)]

# Get the list of restaurants
# e.g. [('1','溏老鴨平價火鍋'), ('2','鍋in'), ...]
with open("ref/restaurant_list.csv") as f:
    next(f)
    r = csv.reader(f)
    restaurant = [tuple(line) for line in r]

```

#### 基本設定-連接資料庫
```python
@classmethod
def connect_db(cls):
    con = create_engine("sqlite://" + DB_PATH)
    return con

@classmethod
def upload_data(cls, d, table_name):
    """Insert data into the database"""
    d.to_sql(table_name, cls.connect_db(),
             if_exists='append', index=False)
```

#### 登入頁-創造及安排物件
```python
　
"""影像"""
# Set logo
logo = ImageTk.PhotoImage(Image.open("ref/logo.png").resize((120, 120)))
self.logo_img = tk.Label(self, image=logo)
self.logo_img.image = logo  # keep a reference!
self.logo_img.grid(row=0, pady=(70, 14), padx=INIT_X - 170, sticky=tk.NW)

"""文字標籤"""
# Set title
self.label = tk.Label(self, text="NTU 校園美食評分",
                      font=controller.title_font, fg='#3D7F47')
self.label.grid(row=0, pady=(100, 14), padx=INIT_X - 30, sticky=tk.NW)

"""輸入框"""
# Set the name input field
self.name_label = tk.Label(self, text='使用者名稱 : ', font=controller.label_font)
self.name_label.grid(row=1, pady=(30, 6), padx=INIT_X - 110, sticky=tk.NW)
self.name_entry = tk.Entry(self)
self.name_entry.grid(row=1, pady=(36, 6), padx=INIT_X + 25, sticky=tk.NW)

"""下拉式選單"""
# Set the age input field
self.age_label = tk.Label(self, text='年級 : ', font=controller.label_font)
self.age_label.grid(row=2, pady=6, padx=INIT_X - 110, sticky=tk.NW)
self.age_box = ttk.Combobox(self, state='readonly',
                            font=controller.note_font,
                            values=['大一', '大二', '大三', '大四', '碩士', '博士'])
self.age_box.grid(row=2, pady=6, padx=INIT_X - 30, sticky=tk.NW)
self.age_box.current(0)

"""單選按鈕選單"""
# Set the gender input field
self.gender_label = tk.Label(self, text='性別 : ', font=controller.label_font)
self.gender_label.grid(row=3, pady=6, padx=INIT_X - 110, sticky=tk.NW)
self.gender_var = tk.IntVar(self)
self.gender_m = tk.Radiobutton(self, text='男',
                               font=controller.label_font, variable=self.gender_var, value=0)
self.gender_m.grid(row=3, pady=7, padx=INIT_X - 10, sticky=tk.NW)
self.gender_f = tk.Radiobutton(self, text='女',
                               font=controller.label_font, variable=self.gender_var, value=1)
self.gender_f.grid(row=3, pady=7, padx=INIT_X + 90, sticky=tk.NW)
self.gender_var.set(0)
...
```

#### 登入頁-避免重複姓名或未輸入名稱
```python
...

# Get all username
self.all_usr_name = []
try:
    all_usr_name_df = pd.read_sql_query('SELECT * FROM usr', Application.connect_db())
    self.all_usr_name = all_usr_name_df["name"].to_list()
except exc.OperationalError:  # 避免資料庫無資料時出現error
    pass

...

# check if input is empty
if self.name_entry.get() == "":
    Application.show_message("請輸入使用者名稱")

# check if username is used
elif self.name_entry.get() in self.all_usr_name:
    Application.show_message("請輸入其他使用者名稱")

...
```

#### 評分及結果頁-使物件可以在頁面上被滑鼠控制拖曳
```python
...

# Make objects on the canvas movable
self.my_canvas.bind("<B1-Motion>", self.move)

...

# Set first img
self.img = tk.PhotoImage(file=images[0])
self.my_image = self.my_canvas.create_image(INIT_X - 90,
                                            INIT_Y - 90, anchor=tk.NW, image=self.img)

...

def move(self, event):
    """Use the mouse to display the object and get the coordinates"""
    global X_POS, Y_POS
    self.img = tk.PhotoImage(file=images[CURRENT_IMG_NUMBER])
    self.my_image = self.my_canvas.create_image(event.x, event.y, image=self.img)
    X_POS = event.x
    Y_POS = event.y

...
```

#### 評分及結果頁-紀錄評分結果（座標）
```python
...

# Record current results
if (X_POS == 0) and (Y_POS == 0):  # 檢查使用者是否拖曳，若無，則給定值
    X_POS, Y_POS = INIT_X - 32.5, INIT_Y - 32.5
# 紀錄 [目前的使用者, 評分的餐廳, x座標, y座標]
item = [CURRENT_PLAYER, str(restaurant[CURRENT_IMG_NUMBER][0]), X_POS, Y_POS]
data.append(item)
# Reset the coordinates
X_POS = 0
Y_POS = 0

...
```

#### 評分及結果頁-若使用者未完成評分：繼續評分
```python
...

CURRENT_IMG_NUMBER += 1
# del current object
self.my_canvas.delete("progress")
self.my_canvas.delete(self.my_image)
# update processing progress
self.progress_label.config(font=self.controller.label_font,
                           text="已評分或跳過的餐廳：" + str(CURRENT_IMG_NUMBER) + " / 20")
self.res_label.config(font=self.controller.label_font,
                      text="目前評分餐廳：" + restaurant[CURRENT_IMG_NUMBER][1])
self.img = tk.PhotoImage(file=images[CURRENT_IMG_NUMBER])
self.my_image = self.my_canvas.create_image(INIT_X - 90,
                                            INIT_Y - 90, anchor=tk.NW, image=self.img)

...
```

#### 評分及結果頁-若使用者已完成評分：送出評分結果並視覺化
```python
...

data_df = pd.DataFrame(data)
data_df.columns = ["name", "index", "x", "y"]

"""送進資料庫"""
Application.upload_data(data_df, table_name="ranking")

"""紀錄使用者填答狀況：是否完成"""
# Add the "finish" tag because the ranking process has been finished
FINISH = True

"""紀錄使用者填答狀況：是否跳過全部題目"""
# If the user has not ranked any restaurants, add the "skip" tag
if tuple(set([tuple(d[2:]) for d in data])) == ((INIT_X - 32.5, INIT_Y - 32.5),):
    SKIP = True

"""視覺化"""
self.show_result()
CURRENT_IMG_NUMBER += 1

...
```

#### 評分及結果頁-視覺化：計算不同篩選條件的評分結果
```python
...

"""把資料拉出來"""
df1 = pd.read_sql_query('SELECT * FROM ranking', Application.connect_db())
df2 = pd.read_sql_query('SELECT * FROM usr', Application.connect_db())

# Get the average value of xy coordinates
"""先算全部人的結果（座標取平均）"""
df_main = df1.groupby(['index']).mean().reset_index()

"""再依據不同條件算評分結果（依照使用者名稱合併大表，分組，然後座標取平均）"""
df_m = df1.join(df2.set_index('name'), on='name')
# Filter by age
df_age = df_m.groupby(['index', "age"]).mean().reset_index()
df_age_f = df_age[df_age["age"] == "大一"]
df_age_f2 = df_age[df_age["age"] == "大四"]
# Filter by budget
df_budget = df_m.groupby(['index', "budget"]).mean().reset_index()
df_budget_f = df_budget[df_budget["budget"] == 1]
# Filter by place
df_place = df_m.groupby(['index', "place"]).mean().reset_index()
df_place_f = df_place[df_place["place"] == 2]
# Filter by current user
df_my_ans = df_m[df_m["name"] == CURRENT_PLAYER]
final_res = [df_place_f, df_budget_f, df_age_f, df_age_f2, df_my_ans, df_main]

...
```

#### 評分及結果頁-視覺化：呈現評分結果
```python
...

"""清空頁面"""
# Del current object
self.my_canvas.delete("progress")
self.my_canvas.delete(self.my_image)
# Del the progress label
self.progress_label.destroy()
self.res_label.destroy()

"""讀資料"""
# Fetch the data
df = self.read_data()
# Del the progress bar
self.progress_bar.destroy()
self.res_uploading_label.destroy()

"""依據評分結果（座標取平均）顯示餐廳圖像"""
for index, line in df.iterrows():
    # Show all img on the canvas
    res_final_label = tk.Label(self.my_canvas,
                               font=self.controller.label_font, text="最終評分結果", fg="red")
    res_final_label.place(rely=.035, relx=0.0, x=50, y=0, anchor=tk.NW)
    res_img_path = images[int(line["index"]) - 1]
    res_img = Image.open(res_img_path).resize((75, 75))
    res_img.load()
    photo_img = ImageTk.PhotoImage(res_img)
    images.append(photo_img)  # Keep the reference
    res_img_record.append(self.my_canvas.create_image(int(line["x"]), int(line["y"]),
                                                      anchor=tk.NW, image=photo_img))

"""提供不同篩選條件選單"""
# See different results
self.filter_var = tk.IntVar(self)
filter_position = 90
if (FINISH is True) and (SKIP is False):
    self.filter_my = tk.Radiobutton(self, text='我的答案',
                                    font=self.controller.label_font,
                                    variable=self.filter_var, value=4,
                                    command=lambda: self.filter_btn(final_res[4]))
    self.filter_my.place(rely=.035, relx=0.0, x=50, y=filter_position, anchor=tk.NW)
    filter_position += 40

self.filter_label = tk.Label(self, text='看其他人 : ', font=self.controller.label_font)
self.filter_label.place(rely=.035, relx=0.0, x=50, y=filter_position, anchor=tk.NW)

self.filter_1 = tk.Radiobutton(self, text='公館人',
                               font=self.controller.label_font,
                               variable=self.filter_var, value=0,
                               command=lambda: self.filter_btn(final_res[0]))
self.filter_1.place(rely=.035, relx=0.0, x=50, y=filter_position + 35, anchor=tk.NW)
self.filter_2 = tk.Radiobutton(self, text='小資族',
                               font=self.controller.label_font,
                               variable=self.filter_var, value=1,
                               command=lambda: self.filter_btn(final_res[1]))
self.filter_2.place(rely=.035, relx=0.0, x=50, y=filter_position + 70, anchor=tk.NW)
self.filter_3 = tk.Radiobutton(self, text='大一新生',
                               font=self.controller.label_font,
                               variable=self.filter_var, value=2,
                               command=lambda: self.filter_btn(final_res[2]))
self.filter_3.place(rely=.035, relx=0.0, x=50, y=filter_position + 105, anchor=tk.NW)
self.filter_4 = tk.Radiobutton(self, text='大四老屁股',
                               font=self.controller.label_font,
                               variable=self.filter_var, value=3,
                               command=lambda: self.filter_btn(final_res[3]))
self.filter_4.place(rely=.035, relx=0.0, x=50, y=filter_position + 140, anchor=tk.NW)
self.filter_5 = tk.Radiobutton(self, text='所有人',
                               font=self.controller.label_font,
                               variable=self.filter_var, value=5,
                               command=lambda: self.filter_btn(final_res[5]))
self.filter_5.place(rely=.035, relx=0.0, x=50, y=filter_position + 175, anchor=tk.NW)

self.filter_var.set(-1)

...
```

## 心得與未來展望

- 還可以更好：
    - 介面呈現（UI）
    - 更多個人化的結果呈現
    
- 學習與收穫：
    - 探索不熟悉功能：拆解工作任務、分頭研究
    - 互相學習與快速達成共識：定期開會review
    - 培養自學能力：
      - 從Stack Overflow, Google找template
      - try and error
    
    
    
