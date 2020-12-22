import tkinter as tk
import tkinter.font as tkfont
import tkinter.messagebox as tkmb
import tkinter.ttk as ttk
from PIL import ImageTk, Image
import time
import pandas as pd
import pygsheets
import csv

WINDOW_W = None  # The width of the window
WINDOW_H = None  # The height of the window
INIT_X = None  # The initial x coordinate of the object
INIT_Y = None  # The initial y coordinate of the object
item_pad = 90  # the padding of the objects on the canvas
usr_data = []  # Record usr info
res_img_record = []  # Record img info of the objects on the canvas
data = []  # Record the ranking results
final_res = []
xpos = 0  # x coordinate of the object
ypos = 0  # y coordinate of the object
current_player = 0  # Record usr name
current_image_number = 0  # The order of the object

# Get the path of all restaurant pics
IMAGE_PATH = "ref/img/"
IMAGE_NUM = 20
images = ["".join([IMAGE_PATH, str(n), ".png"]) for n in range(1, IMAGE_NUM+1)]

# Get the list of restaurants
with open("ref/restaurant_list.csv") as f:
    next(f)
    r = csv.reader(f)
    restaurant = [tuple(line) for line in r]


class Application(tk.Tk):

    def __init__(self, *args, **kwargs):
        global WINDOW_W, WINDOW_H, INIT_X, INIT_Y, item_pad
        tk.Tk.__init__(self, *args, **kwargs)
        # Set the font style
        self.title_font = tkfont.Font(family='Noto Sans CJK TC', size=40, weight="bold")
        self.label_font = tkfont.Font(family='Noto Sans CJK TC', size=22, weight="normal")
        self.note_font = tkfont.Font(family='Noto Sans CJK TC', size=16, weight="normal")
        # Set the frame size
        container = tk.Frame(self)
        WINDOW_W = container.winfo_screenwidth()
        WINDOW_H = container.winfo_screenheight()
        INIT_X = WINDOW_W / 2
        INIT_Y = WINDOW_H / 2
        # Set the layout of the frame
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid(row=0, column=0, sticky="nsew")

        # Collect all pages
        self.frames = {}
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Set the landing page
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        """Show a frame for the given page name"""
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Set logo
        logo = ImageTk.PhotoImage(Image.open("ref/logo.png").resize((120, 120)))
        self.logo_img = tk.Label(self, image=logo)
        self.logo_img.image = logo  # keep a reference!
        self.logo_img.grid(row=0, pady=(70, 14), padx=INIT_X - 170, sticky=tk.NW)
        # Set title
        self.label = tk.Label(self, text="NTU 校園美食評分", font=controller.title_font, fg='#3D7F47')
        self.label.grid(row=0, pady=(100, 14), padx=INIT_X - 30, sticky=tk.NW)
        # Set the name input field
        self.name_label = tk.Label(self, text='姓名 : ', font=controller.label_font)
        self.name_label.grid(row=1, pady=(30, 6), padx=INIT_X - 110, sticky=tk.NW)
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=1, pady=(30, 6), padx=INIT_X - 30, sticky=tk.NW)
        # Set the age input field
        self.age_label = tk.Label(self, text='年級 : ', font=controller.label_font)
        self.age_label.grid(row=2, pady=6, padx=INIT_X - 110, sticky=tk.NW)
        self.age_box = ttk.Combobox(self, state='readonly',
                               font=controller.note_font, values=['大一', '大二', '大三', '大四', '碩士', '博士'])
        self.age_box.grid(row=2, pady=6, padx=INIT_X - 30, sticky=tk.NW)  # TODO 想一下怎麼讓樣式比較好看
        self.age_box.current(0)
        # Set the gender input field
        self.gender_label = tk.Label(self, text='性別 : ', font=controller.label_font)
        self.gender_label.grid(row=3, pady=6, padx=INIT_X - 110, sticky=tk.NW)
        self.gender_var = tk.IntVar(self)
        self.gender_m = tk.Radiobutton(self, text='男', font=controller.label_font, variable=self.gender_var, value=0)
        self.gender_m.grid(row=3, pady=7, padx=INIT_X - 10, sticky=tk.NW)
        self.gender_f = tk.Radiobutton(self, text='女', font=controller.label_font, variable=self.gender_var, value=1)
        self.gender_f.grid(row=3, pady=7, padx=INIT_X + 90, sticky=tk.NW)
        self.gender_var.set(0)
        # Set the department input field
        self.department_label = tk.Label(self, text='院別 : ', font=controller.label_font)
        self.department_label.grid(row=4, pady=6, padx=INIT_X - 110, sticky=tk.NW)
        self.department_box = ttk.Combobox(self, state='readonly', font=controller.note_font,
                                      values=['文學院', '工學院', '管理學院', '社會科學院',
                                              '理學院', '醫學院', '法律學院', '公共衛生學院', '商學院',
                                              '生命科學院', '電機資訊學院', '生物資源暨農學院', '其他'])
        self.department_box.grid(row=4, pady=6, padx=INIT_X - 30, sticky=tk.NW)  # TODO 想一下怎麼讓樣式比較好看
        self.department_box.current(0)
        # Set the budget input field
        self.budget_label = tk.Label(self, text='平均每餐的預算（元） : ', font=controller.label_font)
        self.budget_label.grid(row=5, pady=6, padx=INIT_X - 110, sticky=tk.NW)
        self.budget_var = tk.IntVar(self)
        self.budget_100_under = tk.Radiobutton(self, text='100以下', font=controller.label_font, variable=self.budget_var, value=0)
        self.budget_100_under.grid(row=6, pady=4, padx=INIT_X - 100, sticky=tk.NW)
        self.budget_100_199 = tk.Radiobutton(self, text='100~199', font=controller.label_font, variable=self.budget_var, value=1)
        self.budget_100_199.grid(row=6, pady=4, padx=INIT_X + 60, sticky=tk.NW)
        self.budget_200_299 = tk.Radiobutton(self, text='200~299', font=controller.label_font, variable=self.budget_var, value=2)
        self.budget_200_299.grid(row=7, pady=4, padx=INIT_X - 100, sticky=tk.NW)
        self.budget_300_399 = tk.Radiobutton(self, text='300~399', font=controller.label_font, variable=self.budget_var, value=3)
        self.budget_300_399.grid(row=7, pady=4, padx=INIT_X + 60, sticky=tk.NW)
        self.budget_400_499 = tk.Radiobutton(self, text='400~499', font=controller.label_font, variable=self.budget_var, value=4)
        self.budget_400_499.grid(row=8, pady=4, padx=INIT_X - 100, sticky=tk.NW)
        self.budget_500_above = tk.Radiobutton(self, text='500以上', font=controller.label_font, variable=self.budget_var, value=5)
        self.budget_500_above.grid(row=8, pady=4, padx=INIT_X + 60, sticky=tk.NW)
        self.budget_var.set(0)
        # Set the place input field
        self.place_label = tk.Label(self, text='最常到哪裡用餐 : ', font=controller.label_font)
        self.place_label.grid(row=9, pady=6, padx=INIT_X - 110, sticky=tk.NW)
        self.place_var = tk.IntVar(self)
        self.place_1 = tk.Radiobutton(self, text='水源校區', font=controller.label_font, variable=self.place_var, value=0)
        self.place_1.grid(row=10, pady=4, padx=INIT_X - 100, sticky=tk.NW)
        self.place_2 = tk.Radiobutton(self, text='新生南路', font=controller.label_font, variable=self.place_var, value=1)
        self.place_2.grid(row=10, pady=4, padx=INIT_X + 60, sticky=tk.NW)
        self.place_3 = tk.Radiobutton(self, text='公館商區', font=controller.label_font, variable=self.place_var, value=2)
        self.place_3.grid(row=11, pady=4, padx=INIT_X - 100, sticky=tk.NW)
        self.place_4 = tk.Radiobutton(self, text='118巷', font=controller.label_font, variable=self.place_var, value=3)
        self.place_4.grid(row=11, pady=4, padx=INIT_X + 60, sticky=tk.NW)
        self.place_var.set(0)
        # Get the instructions
        self.info_btn = tk.Button(self, text="玩法說明", font=controller.label_font,
                             fg='#1D7381', width=10, height=2, activeforeground='red',
                             command=self.info_window)
        self.info_btn.grid(row=12, pady=(20, 0), padx=INIT_X - 110, sticky=tk.NW)
        # Start to rank the restaurants
        self.str_btn = tk.Button(self, text="開始評分", font=controller.label_font,
                            fg='#1D7381', width=10, height=2, activeforeground='red',
                            command=lambda: [self.get_information()])
        self.str_btn.grid(row=12, pady=(20, 0), padx=INIT_X + 40, sticky=tk.NW)

    def info_window(self):
        """Show the instructions"""
        new_window = tk.Toplevel(self)
        info = ImageTk.PhotoImage(Image.open("ref/info.png"))
        info_img = tk.Label(new_window, image=info)
        info_img.image = info  # keep a reference!
        info_img.grid(row=2, pady=(0, 0), padx=170, sticky=tk.NW)  # TODO 有空再做一個離開的 btn

    def get_information(self):
        global current_player, usr_data
        current_player = self.name_entry.get()
        usr_data = [self.name_entry.get(),
                    self.age_box.get(),
                    self.gender_var.get(),
                    self.department_box.get(),
                    self.budget_var.get(),
                    self.place_var.get()]
        if self.name_entry.get() == "":
            PageOne.show_message(self, "請輸入姓名")
        else:
            # PageOne.upload_data(usr_data, 'usr', ["name", "age", "gender", "department", "budget", "place"])
            self.controller.show_frame("PageOne")


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        # Set the canvas
        self.my_canvas = tk.Canvas(self, width=WINDOW_W, height=WINDOW_H, bg="white")
        self.my_canvas.pack(side="top", fill='both', expand=True)
        # Set the coordinates axis and title
        self.my_canvas.create_line(150, INIT_Y, WINDOW_W - 150, INIT_Y, fill="gray", width=5)
        self.my_canvas.create_line(INIT_X, 125, INIT_X, WINDOW_H - 125, fill="gray", width=5)
        self.my_canvas.create_text(item_pad, INIT_Y, fill="Gray",
                                   font=controller.label_font, text="難吃")
        self.my_canvas.create_text(WINDOW_W - item_pad, INIT_Y,
                                   fill="Gray", font=controller.label_font, text="好吃")
        self.my_canvas.create_text(INIT_X, item_pad,
                                   fill="Gray", font=controller.label_font, text="健康")
        self.my_canvas.create_text(INIT_X, WINDOW_H - item_pad,
                                   fill="Gray", font=controller.label_font, text="不健康")
        # Set first img
        self.img = tk.PhotoImage(file=images[0])
        self.my_image = self.my_canvas.create_image(INIT_X - 90, INIT_Y - 90, anchor=tk.NW, image=self.img)
        # Create buttons
        button_save = tk.Button(self.my_canvas, font=controller.note_font,
                                fg='#1D7381', width=15, height=2, activeforeground='red',
                                text="提交餐廳評分", command=self.submit_btn)
        button_save.place(rely=1.0, relx=1.0, x=-720, y=-50, anchor=tk.SE)
        button_skip = tk.Button(self.my_canvas, font=controller.note_font,
                                fg='#1D7381', width=10, height=2, activeforeground='red',
                                text="跳過餐廳", command=self.submit_btn)
        button_skip.place(rely=1.0, relx=1.0, x=-610, y=-50, anchor=tk.SE)
        button_quit = tk.Button(self.my_canvas, font=controller.note_font,
                                fg='#1D7381', width=18, height=2, activeforeground='red',
                                text="直接看評分結果", command=self.show_res_btn)
        button_quit.place(rely=1.0, relx=1.0, x=-420, y=-50, anchor=tk.SE)
        button_quit = tk.Button(self.my_canvas, font=controller.note_font,
                                fg='#1D7381', width=6, height=2, activeforeground='red',
                                text="結束", command=controller.destroy)
        button_quit.place(rely=1.0, relx=1.0, x=-350, y=-50, anchor=tk.SE)
        # Create labels
        self.progress_label = tk.Label(self.my_canvas, text="", fg="red")
        self.progress_label.place(rely=.035, relx=0.0, x=50, y=0, anchor=tk.NW)
        self.res_label = tk.Label(self.my_canvas, text="", fg="black")
        self.res_label.place(rely=.07, relx=0.0, x=50, y=0, anchor=tk.NW)
        self.progress_label.config(font=controller.label_font,
                                   text="已評分或跳過的餐廳：" + str(current_image_number) + " / 20")
        self.res_label.config(font=controller.label_font,
                              text="目前評分餐廳：" + restaurant[current_image_number][1])
        # Make objects on the canvas movable
        self.my_canvas.bind("<B1-Motion>", self.move)

    def move(self, event):
        """Use the mouse to display the object and get the coordinates"""
        global xpos, ypos
        self.img = tk.PhotoImage(file=images[current_image_number])
        self.my_image = self.my_canvas.create_image(event.x, event.y, image=self.img)
        xpos = event.x
        ypos = event.y

    def submit_btn(self):
        """
        Define different click events:
        - Ranking process is not completed -> continue processing
        - Ranking process is completed -> show completed message
        """
        global current_image_number, xpos, ypos, current_player
        if current_image_number <= IMAGE_NUM-1:  # Ranking process is not completed
            # Record current results
            if (xpos == 0) and (ypos == 0):
                xpos, ypos = INIT_X, INIT_Y
            item = [current_player, str(restaurant[current_image_number][0]), xpos, ypos]
            data.append(item)
            # Reset the coordinates
            xpos = 0
            ypos = 0
            # If the ranking process is completed, upload and show the results
            if current_image_number == IMAGE_NUM-1:
                # self.upload_data(data, 'data', ["name", "index", "x", "y"])
                self.show_result()
                current_image_number += 1

            # If the ranking process is not completed, continue processing
            else:
                current_image_number += 1
                # del current object
                self.my_canvas.delete("progress")
                self.my_canvas.delete(self.my_image)
                # update processing progress
                self.progress_label.config(font=self.controller.label_font,
                                           text="已評分或跳過的餐廳：" + str(current_image_number) + " / 20")
                self.res_label.config(font=self.controller.label_font,
                                      text="目前評分餐廳：" + restaurant[current_image_number][1])
                self.img = tk.PhotoImage(file=images[current_image_number])
                self.my_image = self.my_canvas.create_image(INIT_X-90, INIT_Y-90, anchor=tk.NW, image=self.img)
        else:
            self.show_message("所有餐廳已完成評分")

    @classmethod
    def connect_db(self, table_name):
        """Connect the Google spreadsheet"""
        gc = pygsheets.authorize(service_file='ref/client_secret.json')  # Don't share the secret.json on GitHub
        sh = gc.open('NTU_ranking')
        wks = sh[0]
        wks = sh.worksheet_by_title(table_name)
        cells = wks.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False, returnas='matrix')
        return wks, cells

    @classmethod
    def upload_data(self, d, table_name, col):
        """Upload data to Google spreadsheet"""
        last_row = len(self.connect_db(table_name)[1])
        wks = self.connect_db(table_name)[0]

        if len(wks.get_as_df()) == 0:
            wks.insert_rows(row=0, number=1, values=col)
            wks.insert_rows(last_row, number=1, values=d)
        else:
            wks.insert_rows(last_row, number=1, values=d)

    def read_data(self):
        """Fetch data from Google spreadsheet"""
        global final_res
        self.progress_bar_running()
        wks1 = self.connect_db(table_name='data')[0]
        df1 = wks1.get_as_df()
        wks2 = self.connect_db(table_name='usr')[0]
        df2 = wks2.get_as_df()
        # Get the average value of xy coordinates
        df_main = df1.groupby(['index']).mean().reset_index()
        df_m = df1.join(df2.set_index('name'), on='name')
        df_age = df_m.groupby(['index', "age"]).mean().reset_index()
        df_age_f = df_age[df_age["age"] == "大一"]
        df_age_f2 = df_age[df_age["age"] == "大四"]
        df_budget = df_m.groupby(['index', "budget"]).mean().reset_index()
        df_budget_f = df_budget[df_budget["budget"] == 1]
        df_place = df_m.groupby(['index', "place"]).mean().reset_index()
        df_place_f = df_place[df_place["place"] == 2]
        final_res = [df_place_f, df_budget_f, df_age_f, df_age_f2]
        return df_main

    def show_result(self):
        """Show final ranking result"""
        global res_img_record
        # Del current object
        self.my_canvas.delete("progress")
        self.my_canvas.delete(self.my_image)
        # Del the progress label
        self.progress_label.destroy()
        self.res_label.destroy()
        # Fetch the data
        df = self.read_data()
        # Del the progress bar
        self.progress_bar.destroy()
        self.res_uploading_label.destroy()
        for index, line in df.iterrows():
            # Show all img on the canvas
            res_final_label = tk.Label(self.my_canvas, font=self.controller.label_font, text="最終結果", fg="red")
            res_final_label.place(rely=.035, relx=0.0, x=50, y=0, anchor=tk.NW)
            res_img_path = images[int(line["index"])-1]
            res_img = Image.open(res_img_path).resize((75, 75))
            res_img.load()
            photoimg = ImageTk.PhotoImage(res_img)
            images.append(photoimg)  # Keep the reference
            res_img_record.append(self.my_canvas.create_image(int(line["x"]), int(line["y"]), anchor=tk.NW, image=photoimg))

    def show_res_btn(self):
        """
        Display the final ranking result directly:
        - Final ranking result is not displayed -> continue processing
        - Final ranking result is displayed -> show completed message
        """
        global current_image_number, final_res
        if current_image_number <= IMAGE_NUM-1:
            current_image_number = IMAGE_NUM-1
            # Del current object
            self.my_canvas.delete("progress")
            self.my_canvas.delete(self.my_image)
            # Del the progress label
            self.progress_label.destroy()
            self.res_label.destroy()
            # Display the final ranking result
            self.show_result()
            current_image_number += 1
            # Del the progress bar
            self.progress_bar.destroy()
            self.res_uploading_label.destroy()
            res_final_label = tk.Label(self.my_canvas, font=self.controller.label_font, text="最終結果", fg="red")
            res_final_label.place(rely=.035, relx=0.0, x=50, y=0, anchor=tk.NW)
            # Set the place input field
            self.filter_label = tk.Label(self, text='看其他人 : ', font=self.controller.label_font)
            self.filter_label.place(rely=.035, relx=0.0, x=50, y=90, anchor=tk.NW)
            self.filter_var = tk.IntVar(self)
            self.filter_1 = tk.Radiobutton(self, text='公館人',
                                           font=self.controller.label_font,
                                           variable=self.filter_var, value=0,
                                           command=lambda: self.filter_btn(final_res[0]))
            self.filter_1.place(rely=.035, relx=0.0, x=50, y=130, anchor=tk.NW)
            self.filter_2 = tk.Radiobutton(self, text='小資族',
                                           font=self.controller.label_font, variable=self.filter_var, value=1,
                                           command=lambda: self.filter_btn(final_res[1]))
            self.filter_2.place(rely=.035, relx=0.0, x=50, y=160, anchor=tk.NW)
            self.filter_3 = tk.Radiobutton(self, text='大一新生',
                                           font=self.controller.label_font, variable=self.filter_var, value=2,
                                           command=lambda: self.filter_btn(final_res[2]))
            self.filter_3.place(rely=.035, relx=0.0, x=50, y=190, anchor=tk.NW)
            self.filter_4 = tk.Radiobutton(self, text='大四老屁股',
                                           font=self.controller.label_font, variable=self.filter_var, value=3,
                                           command=lambda: self.filter_btn(final_res[3]))
            self.filter_4.place(rely=.035, relx=0.0, x=50, y=220, anchor=tk.NW)
            self.filter_var.set(-1)

        else:
            self.show_message("已顯示最終結果")

    def filter_btn(self, f):
        global res_img_record
        # Del current object
        for item in res_img_record:
            self.my_canvas.delete(item)
        df = f
        for index, line in df.iterrows():
            # Show all img on the canvas
            res_img_path = images[int(line["index"]) - 1]
            res_img = Image.open(res_img_path).resize((75, 75))
            res_img.load()
            photoimg = ImageTk.PhotoImage(res_img)
            images.append(photoimg)  # Keep the reference
            res_img_record.append(
                self.my_canvas.create_image(int(line["x"]), int(line["y"]), anchor=tk.NW, image=photoimg))

    def show_message(self, msg):
        """Display message in new window"""
        info_message = msg
        # info message box
        tkmb.showinfo("Output", info_message)

    def progress_bar_running(self):
        """Display progress bar"""
        self.res_uploading_label = tk.Label(self.my_canvas,
                                            font=self.controller.label_font, text="計算最終結果中...", fg="red")
        self.res_uploading_label.place(rely=.5, relx=0.5, x=-220, y=-50, anchor=tk.NW)
        self.progress_bar = ttk.Progressbar(self.my_canvas, orient="horizontal", length=250, mode="determinate")
        self.progress_bar.place(rely=.5, relx=.5, x=-15, y=0, anchor=tk.SE)
        self.progress_bar['maximum'] = 100
        for i in range(101):
            time.sleep(0.05)
            self.progress_bar["value"] = i
            self.progress_bar.update()
            self.progress_bar["value"] = 0


if __name__ == "__main__":
    app = Application()
    # Open the window in full screen
    app.overrideredirect(True)
    app.overrideredirect(False)
    app.attributes('-fullscreen', True)
    app.mainloop()
