import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

window = tk.Tk()
# 設定視窗標題、大小和背景顏色
window.title('NTU 美食票選')
window.geometry('700x1000')
header_label = tk.Label(window, text='玩家資料登入', font=('黑體-繁', 30, 'bold'), pady=10, fg='#3D7F47')
header_label.pack()


def create_new_window():
    new_window = tk.Toplevel(window)


def get_information():
    name = name_entry.get()
    print(name)
    age = age_box.get()
    print(age)
    gender = gender_var.get()
    print(gender)
    department = department_box.get()
    print(department)
    budget = budget_var.get()
    print(budget)
    place = place_var.get()
    print(place)


label_frame = tk.Frame(window)
label_frame.pack(side=tk.TOP)
name_label = tk.Label(label_frame, text='姓名 : ', font=('黑體-繁', 16))
name_label.grid(row=0, padx=5, sticky=tk.W)
age_label = tk.Label(label_frame, text='年級 : ', font=('黑體-繁', 16))
age_label.grid(row=1, padx=5, pady=10, sticky=tk.W)
gender_label = tk.Label(label_frame, text='性別 : ', font=('黑體-繁', 16))
gender_label.grid(row=2, padx=5, sticky=tk.W, pady=10)
department_label = tk.Label(label_frame, text='院別 : ', font=('黑體-繁', 16))
department_label.grid(row=4, padx=5, sticky=tk.W, pady=20)
question_frame = tk.Frame(window)
question_frame.pack(side=tk.TOP)
budget_label = tk.Label(question_frame, text='平均每餐的預算(元): ', font=('黑體-繁', 16))
budget_label.grid(row=0, padx=5, sticky=tk.W, pady=10)
place_label = tk.Label(question_frame, text='最常到哪裡用餐 : ', font=('黑體-繁', 16))
place_label.grid(row=2, padx=5, sticky=tk.W, pady=10)

name_entry = tk.Entry(label_frame)
name_entry.grid(row=0, column=1)
age_box = ttk.Combobox(label_frame, font='黑體-繁', values=['大一', '大二', '大三', '大四', '碩士', '博士'])
age_box.grid(row=1, column=1, sticky=tk.W)
age_box.current(0)
# 以下為 gender_var 群組
gender_var = tk.IntVar(label_frame)
gender_m = tk.Radiobutton(label_frame, text='男', font='黑體-繁', variable=gender_var, value=0).grid(column=1, row=2,
                                                                                                 sticky=tk.W)
gender_f = tk.Radiobutton(label_frame, text='女', font='黑體-繁', variable=gender_var, value=1).grid(column=1, row=3,
                                                                                                 sticky=tk.W)

# 以下為 department_var 群組
department_box = ttk.Combobox(label_frame, font='黑體-繁', values=['文學院', '工學院', '管理學院', '社會科學院', '理學院', '醫學院',
                                                                '法律學院', '公共衛生學院', '商學院', '生命科學院', '電機資訊學院',
                                                                '生物資源暨農學院', '其他', ])
department_box.grid(row=4, column=1, sticky=tk.W)
department_box.current(0)

# 以下為 budget_var 群組
budget_var = tk.StringVar(question_frame)
budget_var.set('100以下')
tk.Radiobutton(question_frame, text='100以下', font=('黑體-繁', 15), variable=budget_var, value='100以下').grid(column=1, row=0,
                                                                                                   sticky=tk.W)
tk.Radiobutton(question_frame, text='100~199', font=('黑體-繁', 15), variable=budget_var, value='100~200').grid(column=2, row=0,
                                                                                                       sticky=tk.W)
tk.Radiobutton(question_frame, text='200~299', font=('黑體-繁', 15), variable=budget_var, value='200~299').grid(column=1, row=1,
                                                                                                     sticky=tk.W)
tk.Radiobutton(question_frame, text='300~499', font=('黑體-繁', 15), variable=budget_var, value='300~499').grid(column=2, row=1,
                                                                                                       sticky=tk.W)
tk.Radiobutton(question_frame, text='500以上', font=('黑體-繁', 15), variable=budget_var, value='500以上').grid(column=3, row=1,
                                                                                                   sticky=tk.W)

# 以下為 place_var 群組
place_var = tk.StringVar(question_frame)
place_var.set('水源校區')
tk.Radiobutton(question_frame, text='水源校區', font=('黑體-繁', 15), variable=place_var, value='水源校區').grid(column=1, row=2,
                                                                                                   sticky=tk.W)
tk.Radiobutton(question_frame, text='新生南路', font=('黑體-繁', 15), variable=place_var, value='新生南路').grid(column=2, row=2,
                                                                                                       sticky=tk.W)
tk.Radiobutton(question_frame, text='公館商圈', font=('黑體-繁', 15), variable=place_var, value='公館商圈').grid(column=1, row=3,
                                                                                                     sticky=tk.W)
tk.Radiobutton(question_frame, text='118巷', font=('黑體-繁', 15), variable=place_var, value='118巷', pady=5).grid(column=2, row=3,
                                                                                                       sticky=tk.W)

enter_btn = tk.Button(window, text='開始評分', font=('黑體-繁', 16), bg='black', fg='#1D7381', width=10, height=3,
                      activeforeground='red',
                      command=lambda: [get_information(), create_new_window()])
enter_btn.pack()

canvas = tk.Canvas(window, width=700, height=1000, bd=0, highlightthickness=0)
imgPath = "fr8.gif"
img = Image.open(imgPath)
photo = ImageTk.PhotoImage(img)

canvas.create_image(350, -230, image=photo)
photo.side = tk.CENTER
canvas.pack()

enter_btn = tk.Button(window, text='開始評分', command=lambda: [get_information(), create_new_window()])
enter_btn.pack()
window.mainloop()
