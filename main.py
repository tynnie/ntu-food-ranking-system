import tkinter as tk
from tkinter import font as tkfont
import tkinter.messagebox as tkmb
import tkinter.ttk as ttk
import time
from PIL import ImageTk, Image
import pygsheets
import csv

WINDOW_W = None
WINDOW_H = None
INIT_X = None
INIT_Y = None
item_pad = 90

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


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        global WINDOW_W, WINDOW_H, INIT_X, INIT_Y, item_pad
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=40, weight="bold")
        self.label_font = tkfont.Font(family='Helvetica', size=22, weight="normal")
        self.note_font = tkfont.Font(family='Helvetica', size=16, weight="normal")
        container = tk.Frame(self)
        WINDOW_W = container.winfo_screenwidth()
        WINDOW_H = container.winfo_screenheight()
        INIT_X = WINDOW_W / 2
        INIT_Y = WINDOW_H / 2
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid(row=0, column=0, sticky="nsew")

        self.frames = {}
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()

    def quit(self):
        self.destroy()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        logo = ImageTk.PhotoImage(Image.open("ref/logo.png").resize((120, 120)))
        logo_img = tk.Label(self, image=logo)
        logo_img.image = logo  # keep a reference!
        logo_img.grid(row=0, pady=(70, 20), padx=INIT_X - 170, sticky=tk.NW)

        label = tk.Label(self, text="NTU 校園美食評分", font=controller.title_font, fg='#3D7F47')
        label.grid(row=0, pady=(100, 20), padx=INIT_X - 30, sticky=tk.NW)
        # name
        name_label = tk.Label(self, text='姓名 : ', font=controller.label_font)
        name_label.grid(row=1, pady=(30, 10), padx=INIT_X - 110, sticky=tk.NW)
        name_entry = tk.Entry(self)
        name_entry.grid(row=1, pady=(30, 10), padx=INIT_X - 30, sticky=tk.NW)
        # age

        age_label = tk.Label(self, text='年級 : ', font=controller.label_font)
        age_label.grid(row=2, pady=10, padx=INIT_X - 110, sticky=tk.NW)
        age_box = ttk.Combobox(self, state='readonly',
                               font=controller.note_font, values=['大一', '大二', '大三', '大四', '碩士', '博士'])
        age_box.grid(row=2, pady=10, padx=INIT_X - 30, sticky=tk.NW)  # TODO 想一下怎麼讓樣式比較好看
        age_box.current(0)
        # gender
        gender_label = tk.Label(self, text='性別 : ', font=controller.label_font)
        gender_label.grid(row=3, pady=10, padx=INIT_X - 110, sticky=tk.NW)
        gender_var = tk.IntVar(self)
        gender_m = tk.Radiobutton(self, text='男', font=controller.label_font, variable=gender_var, value=0)
        gender_m.grid(row=3, pady=11, padx=INIT_X - 10, sticky=tk.NW)
        gender_f = tk.Radiobutton(self, text='女', font=controller.label_font, variable=gender_var, value=1)
        gender_f.grid(row=3, pady=11, padx=INIT_X + 90, sticky=tk.NW)
        # department
        department_label = tk.Label(self, text='院別 : ', font=controller.label_font)
        department_label.grid(row=4, pady=10, padx=INIT_X - 110, sticky=tk.NW)
        department_box = ttk.Combobox(self, state='readonly', font=controller.note_font,
                                      values=['文學院', '工學院', '管理學院', '社會科學院',
                                              '理學院', '醫學院', '法律學院', '公共衛生學院', '商學院',
                                              '生命科學院', '電機資訊學院', '生物資源暨農學院', '其他'])
        department_box.grid(row=4, pady=10, padx=INIT_X - 30, sticky=tk.NW)  # TODO 想一下怎麼讓樣式比較好看
        department_box.current(0)
        # budget
        budget_label = tk.Label(self, text='平均每餐的預算（元） : ', font=controller.label_font)
        budget_label.grid(row=5, pady=10, padx=INIT_X - 110, sticky=tk.NW)
        budget_var = tk.IntVar(self)
        budget_100_under = tk.Radiobutton(self, text='100以下', font=controller.label_font, variable=budget_var, value=0)
        budget_100_under.grid(row=6, pady=6, padx=INIT_X - 100, sticky=tk.NW)
        budget_100_199 = tk.Radiobutton(self, text='100~199', font=controller.label_font, variable=budget_var, value=1)
        budget_100_199.grid(row=6, pady=6, padx=INIT_X + 60, sticky=tk.NW)
        budget_200_299 = tk.Radiobutton(self, text='200~299', font=controller.label_font, variable=budget_var, value=2)
        budget_200_299.grid(row=7, pady=6, padx=INIT_X - 100, sticky=tk.NW)
        budget_300_399 = tk.Radiobutton(self, text='300~399', font=controller.label_font, variable=budget_var, value=3)
        budget_300_399.grid(row=7, pady=6, padx=INIT_X + 60, sticky=tk.NW)
        budget_400_499 = tk.Radiobutton(self, text='400~499', font=controller.label_font, variable=budget_var, value=4)
        budget_400_499.grid(row=8, pady=6, padx=INIT_X - 100, sticky=tk.NW)
        budget_500_above = tk.Radiobutton(self, text='500以上', font=controller.label_font, variable=budget_var, value=5)
        budget_500_above.grid(row=8, pady=6, padx=INIT_X + 60, sticky=tk.NW)
        # place
        place_label = tk.Label(self, text='最常到哪裡用餐 : ', font=controller.label_font)
        place_label.grid(row=9, pady=10, padx=INIT_X - 110, sticky=tk.NW)
        place_var = tk.IntVar(self)
        place_1 = tk.Radiobutton(self, text='水源校區', font=controller.label_font, variable=place_var, value=0)
        place_1.grid(row=10, pady=6, padx=INIT_X - 100, sticky=tk.NW)
        place_2 = tk.Radiobutton(self, text='新生南路', font=controller.label_font, variable=place_var, value=1)
        place_2.grid(row=10, pady=6, padx=INIT_X + 60, sticky=tk.NW)
        place_3 = tk.Radiobutton(self, text='公館商區', font=controller.label_font, variable=place_var, value=2)
        place_3.grid(row=11, pady=6, padx=INIT_X - 100, sticky=tk.NW)
        place_4 = tk.Radiobutton(self, text='118巷', font=controller.label_font, variable=place_var, value=3)
        place_4.grid(row=11, pady=6, padx=INIT_X + 60, sticky=tk.NW)

        info_btn = tk.Button(self, text="玩法說明", font=controller.label_font,
                             fg='#1D7381', width=10, height=2, activeforeground='red',
                             command=self.info_window)
        info_btn.grid(row=12, pady=(20, 0), padx=INIT_X - 110, sticky=tk.NW)
        str_btn = tk.Button(self, text="開始評分", font=controller.label_font,
                            fg='#1D7381', width=10, height=2, activeforeground='red',
                            command=lambda: controller.show_frame("PageOne"))
        str_btn.grid(row=12, pady=(20, 0), padx=INIT_X + 40, sticky=tk.NW)

    def info_window(self):
        new_window = tk.Toplevel(self)
        info = ImageTk.PhotoImage(Image.open("ref/info.png"))
        info_img = tk.Label(new_window, image=info)
        info_img.image = info  # keep a reference!
        info_img.grid(row=2, pady=(0, 0), padx=170, sticky=tk.NW)  # TODO 有空再做一個離開的 btn

    # def get_information(self):  # TODO 這邊的資料還沒上傳
    #     name = name_entry.get()
    #     print(name_entry.get())
    #     age = age_entry.get()
    #     print(age_entry.get())
    #     gender = gender_var.get()
    #     print(gender_var.get())
    #     department = department_box.get()
    #     print(department_box.get())


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # label = tk.Label(self, text="This is page 1", font=controller.title_font)
        # label.pack(side="top", fill="x", pady=10)
        # button = tk.Button(self, text="Go to the start page",
        #                    command=lambda: controller.show_frame("StartPage"))
        # button.pack()
        self.my_canvas = tk.Canvas(self, width=WINDOW_W, height=WINDOW_H, bg="white")
        self.my_canvas.pack(side="top", fill='both', expand=True)

        # 畫出座標軸及文字
        self.my_canvas.create_line(150, INIT_Y, WINDOW_W - 150, INIT_Y, fill="gray", width=5)
        self.my_canvas.create_line(INIT_X, 125, INIT_X, WINDOW_H - 125, fill="gray", width=5)
        self.my_canvas.create_text(item_pad, INIT_Y, fill="Gray", font=("Purisa", 30), text="難吃")
        self.my_canvas.create_text(WINDOW_W - item_pad, INIT_Y, fill="Gray", font=("Purisa", 30), text="好吃")
        self.my_canvas.create_text(INIT_X, item_pad, fill="Gray", font=("Purisa", 30), text="健康")
        self.my_canvas.create_text(INIT_X, WINDOW_H - item_pad, fill="Gray", font=("Purisa", 30), text="不健康")
        self.img = tk.PhotoImage(file=images[0])
        self.my_image = self.my_canvas.create_image(INIT_X - 90, INIT_Y - 90, anchor=tk.NW, image=self.img)

        # create buttons
        button_save = tk.Button(self.my_canvas, font=controller.note_font,
                                fg='#1D7381', width=15, height=2, activeforeground='red',
                                text="提交餐廳評分", command=self.on_click)
        button_save.place(rely=1.0, relx=1.0, x=-710, y=-50, anchor=tk.SE)
        button_skip = tk.Button(self.my_canvas, font=controller.note_font,
                                fg='#1D7381', width=10, height=2, activeforeground='red',
                                text="跳過餐廳", command=self.on_click)
        button_skip.place(rely=1.0, relx=1.0, x=-600, y=-50, anchor=tk.SE)
        button_quit = tk.Button(self.my_canvas, font=controller.note_font,
                                fg='#1D7381', width=18, height=2, activeforeground='red',
                                text="看其他人評分結果", command=self.show_res_btn)
        button_quit.place(rely=1.0, relx=1.0, x=-420, y=-50, anchor=tk.SE)
        button_quit = tk.Button(self.my_canvas, font=controller.note_font,
                                fg='#1D7381', width=6, height=2, activeforeground='red',
                                text="結束", command=controller.destroy)
        button_quit.place(rely=1.0, relx=1.0, x=-350, y=-50, anchor=tk.SE)

        # create labels
        self.progress_label = tk.Label(self.my_canvas, text="", fg="red")
        self.progress_label.place(rely=.035, relx=0.0, x=50, y=0, anchor=tk.NW)
        self.res_label = tk.Label(self.my_canvas, text="", fg="black")
        self.res_label.place(rely=.07, relx=0.0, x=50, y=0, anchor=tk.NW)
        self.progress_label.config(font=("Purisa", 20), text="已評分或跳過的餐廳：" + str(current_image_number) + " / 20")
        self.res_label.config(font=("Purisa", 20), text="目前評分餐廳：" + restaurant[current_image_number][1])

        # 套用一下拖曳事件
        self.my_canvas.bind("<B1-Motion>", self.move)

    # 設定一下拖曳事件
    def move(self, event):
        global xpos, ypos
        self.img = tk.PhotoImage(file=images[current_image_number])
        self.my_image = self.my_canvas.create_image(event.x, event.y, image=self.img)
        # 儲存一下物件最後的座標
        xpos = event.x
        ypos = event.y
        print(event.x, event.y)

    # 設定按鈕事件
    def on_click(self):
        global current_image_number, xpos, ypos

        if current_image_number <= IMAGE_NUM-1:
            # 儲存已評分餐廳資訊
            item = [str(restaurant[current_image_number][0]), xpos, ypos]
            data.append(item)
            # 重新設定座標
            xpos = 0
            ypos = 0
            # 如果已經是最後一家，就上傳此次評分紀錄以及顯示結果
            if current_image_number == IMAGE_NUM-1:
                # upload_data(data)
                # 顯示一下結果
                self.show_result()

            # 如果還不是最後一家，就繼續進行評分
            else:
                current_image_number += 1
                # 刪除畫面上現有的物件
                self.my_canvas.delete("progress")
                self.my_canvas.delete(self.my_image)
                # 顯示評價進度
                self.progress_label.config(font=("Purisa", 20), text="已評分或跳過的餐廳：" + str(current_image_number) + " / 20")
                self.res_label.config(font=("Purisa", 20), text="目前評分餐廳：" + restaurant[current_image_number][1])
                self.img = tk.PhotoImage(file=images[current_image_number])
                self.my_image = self.my_canvas.create_image(INIT_X-90, INIT_Y-90, anchor=tk.NW, image=self.img)
        else:
            self.show_message_finish()

    # 設定一下請求資料庫的方式
    def connect_db(self):
        gc = pygsheets.authorize(service_file='ref/client_secret.json')
        sh = gc.open('NTU_rating')
        wks = sh[0]
        wks = sh.worksheet_by_title('data')
        cells = wks.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
        return wks, cells

    # upload data to Google spreadsheet
    def upload_data(self, d):
        columns = ["index", "x", "y"]
        last_row = len(self.connect_db()[1])
        wks = self.connect_db()[0]

        if len(wks.get_as_df()) == 0:
            wks.insert_rows(row=0, number=1, values=columns)
            wks.insert_rows(last_row, number=1, values=data)
        else:
            wks.insert_rows(last_row, number=1, values=data)

    # fetch data from Google spreadsheet
    def read_data(self):
        self.progress_bar_running()
        wks = self.connect_db()[0]
        df = wks.get_as_df()
        # 算一下平均
        df = df.groupby(['index']).mean().reset_index()
        return df

    # 顯示結果
    def show_result(self):
        # global progress_bar, res_uploading_label
        # 刪除畫面上現有的物件
        self.my_canvas.delete("progress")
        self.my_canvas.delete(self.my_image)
        # 因為顯示結果了，店名跟評分進度都不需要
        self.progress_label.destroy()
        self.res_label.destroy()
        df = self.read_data()
        self.progress_bar.destroy()
        self.res_uploading_label.destroy()
        for index, line in df.iterrows():
            # 把結果畫上去
            res_final_label = tk.Label(self.my_canvas, font=("Purisa", 20), text="最終結果", fg="red")
            res_final_label.place(rely=.035, relx=0.0, x=50, y=0, anchor=tk.NW)
            res_img_path = images[int(line["index"])-1]
            res_img = Image.open(res_img_path).resize((75, 75))
            res_img.load()
            photoimg = ImageTk.PhotoImage(res_img)
            images.append(photoimg)  # debug用，沒什麼function
            self.my_canvas.create_image(int(line["x"]), int(line["y"]), anchor=tk.NW, image=photoimg)

    # 直接看結果的按鈕
    def show_res_btn(self):
        global current_image_number
        if current_image_number <= IMAGE_NUM-1:
            current_image_number = IMAGE_NUM-1
            # 刪除畫面上現有的物件
            self.my_canvas.delete("progress")
            self.my_canvas.delete(self.my_image)
            # 顯示評價進度
            current_image_number += 1
            # 因為直接顯示結果了，店名跟評分進度都不需要
            self.progress_label.destroy()
            self.res_label.destroy()
            # 顯示一下結果
            self.show_result()
            self.progress_bar.destroy()
            self.res_uploading_label.destroy()
            res_final_label = tk.Label(self.my_canvas,font=("Purisa", 20), text="最終結果", fg="red")
            res_final_label.place(rely=.035, relx=0.0, x=50, y=0, anchor=tk.NW)

        else:
            self.show_message_already_show_res()

    def show_message_finish(self):
        info_message = "所有餐廳已完成評分"
        # info message box
        tkmb.showinfo("Output", info_message)

    def show_message_already_show_res(self):
        info_message = "已顯示最終結果"
        # info message box
        tkmb.showinfo("Output", info_message)

    def progress_bar_running(self):
        # global progress_bar, res_uploading_label
        self.res_uploading_label = tk.Label(self.my_canvas, font=("Purisa", 20), text="計算最終結果中...", fg="red")
        self.res_uploading_label.place(rely=.5, relx=0.5, x=-220, y=-40, anchor=tk.NW)
        self.progress_bar = ttk.Progressbar(self.my_canvas, orient="horizontal", length=250, mode="determinate")
        self.progress_bar.place(rely=.5, relx=.5, x=-15, y=0, anchor=tk.SE)
        self.progress_bar['maximum'] = 100
        for i in range(101):
            time.sleep(0.05)
            self.progress_bar["value"] = i
            self.progress_bar.update()
            self.progress_bar["value"] = 0


if __name__ == "__main__":
    # 介面基本設定
    app = Application()
    # 打開全螢幕
    app.overrideredirect(True)
    app.overrideredirect(False)
    app.attributes('-fullscreen', True)
    app.mainloop()
