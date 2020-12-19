import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

window = tk.Tk()
# 設定視窗標題、大小和背景顏色
window.title('NTU 美食票選')
window.geometry('800x650')
header_label = tk.Label(window, text='玩家資料登入', font=('宋體-繁', 30, 'bold'), pady=10, fg='#3D7F47')
header_label.pack()


def create_new_window():
    new_window = tk.Toplevel(window)


def get_information():
    name = name_entry.get()
    print(name_entry.get())
    age = age_entry.get()
    print(age_entry.get())
    gender = gender_var.get()
    print(gender_var.get())
    department = department_box.get()
    print(department_box.get())


label_frame = tk.Frame(window)
label_frame.pack(side=tk.TOP)
name_label = tk.Label(label_frame, text='姓名 : ', font=('宋體-繁', 16))
name_label.grid(row=0, padx=5, sticky=tk.W)
age_label = tk.Label(label_frame, text='年齡 : ', font=('宋體-繁', 16))
age_label.grid(row=1, padx=5, sticky=tk.W)
gender_label = tk.Label(label_frame, text='性別 : ', font=('宋體-繁', 16))
gender_label.grid(row=3, padx=5, sticky=tk.W, pady=10)
department_label = tk.Label(label_frame, text='院別 : ', font=('宋體-繁', 16))
department_label.grid(row=5, padx=5, sticky=tk.W, pady=20)
name_entry = tk.Entry(label_frame)
name_entry.grid(row=0, column=1)
age_entry = tk.Entry(label_frame, relief='sunken')
age_entry.grid(row=1, column=1)
age_note = tk.Label(label_frame, text='(請輸入純數字 例：18)', font=('宋體-繁', 16))
age_note.grid(row=2, column=1)
# 以下為 gender_var 群組
gender_var = tk.IntVar(label_frame)
gender_m = tk.Radiobutton(label_frame, text='男', font='宋體-繁', variable=gender_var, value=0).grid(column=1, row=3,
                                                                                                 sticky=tk.W)
gender_f = tk.Radiobutton(label_frame, text='女', font='宋體-繁', variable=gender_var, value=1).grid(column=1, row=4,
                                                                                                 sticky=tk.W)

# 以下為 department_var 群組
department_box = ttk.Combobox(label_frame, font='宋體-繁', values=['文學院', '工學院', '管理學院', '社會科學院', '理學院', '醫學院',
                                                                '法律學院', '公共衛生學院', '商學院', '生命科學院', '電機資訊學院',
                                                                '生物資源暨農學院', '其他', ])
department_box.grid(row=5, column=1)
department_box.current(0)
enter_btn = tk.Button(window, text='進入遊戲', font=('宋體-繁', 16), bg='black', fg='#1D7381', width=10, height=3,
                      activeforeground='red',
                      command=lambda: [get_information(), create_new_window()])
enter_btn.pack()

canvas = tk.Canvas(window, width=800, height=600, bd=0, highlightthickness=0)
imgPath = "fr3.gif"
img = Image.open(imgPath)
photo = ImageTk.PhotoImage(img)

canvas.create_image(400, -30, image=photo)
photo.side = tk.CENTER
canvas.pack()

enter_btn = tk.Button(window, text='進入遊戲', command=lambda: [get_information(), create_new_window()])
enter_btn.pack()
window.mainloop()