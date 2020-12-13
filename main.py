import tkinter as tk

APP_TITLE = "台大附近吃什麼？"
# 設定視窗大小
APP_WIDTH = 1200
APP_HEIGHT = 800
# 設定物件起始座標位置
APP_XPOS = APP_WIDTH/2
APP_YPOS = APP_HEIGHT/2
# 設定圖檔路徑
IMAGE_PATH = "ref/img/"


class CreateCanvasObject(object):
    def __init__(self, canvas, image_name, xpos, ypos):
        self.canvas = canvas
        self.image_name = image_name
        self.xpos, self.ypos = xpos, ypos

        self.tk_image = tk.PhotoImage(
            file="{}{}".format(IMAGE_PATH, image_name))
        self.image_obj = canvas.create_image(
            xpos, ypos, image=self.tk_image)

        # function to be called when mouse is clicked
        def printcoords(event):
            # outputting x and y coords to console
            print("x:{} y:{}".format(event.x, event.y))

        canvas.tag_bind(self.image_obj, '<Button1-Motion>', self.move)
        canvas.tag_bind(self.image_obj, '<ButtonRelease-1>', self.release)
        canvas.tag_bind(self.image_obj, '<ButtonRelease-1>', printcoords)

        self.move_flag = False

    def move(self, event):
        if self.move_flag:
            new_xpos, new_ypos = event.x, event.y

            self.canvas.move(self.image_obj,
                             new_xpos - self.mouse_xpos, new_ypos - self.mouse_ypos)

            self.mouse_xpos = new_xpos
            self.mouse_ypos = new_ypos

        else:
            self.move_flag = True
            self.canvas.tag_raise(self.image_obj)
            self.mouse_xpos = event.x
            self.mouse_ypos = event.y

    def release(self, event):
        self.move_flag = False


class Application(tk.Frame):

    def __init__(self, master):
        self.close = None
        self.master = master
        self.master.protocol("WM_DELETE_WINDOW", self.close)
        tk.Frame.__init__(self, master)

        self.canvas = tk.Canvas(self, width=APP_WIDTH, height=APP_HEIGHT, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_line(100, 400, 1100, 400, fill="gray", width=5)
        self.canvas.create_line(600, 100, 600, 700, fill="gray", width=5)
        self.canvas.create_text(50, 400, fill="Gray", font=("Purisa", 30), text="難吃")
        self.canvas.create_text(1150, 400, fill="Gray", font=("Purisa", 30), text="好吃")
        self.canvas.create_text(600, 50, fill="Gray", font=("Purisa", 30), text="健康")
        self.canvas.create_text(600, 750, fill="Gray", font=("Purisa", 30), text="不健康")
        self.image_1 = CreateCanvasObject(self.canvas, "1.png", 520, 360)

        # self.previous = Button(self, text="前一個")
        # self.previous.pack(side=BOTTOM, ipadx=20, padx=30)

        self.next = tk.Button(self.canvas, text="新增下一個")
        # self.next.pack(side="bottom", ipadx=20, padx=30)

        self.quitBtn = tk.Button(self.canvas, text="quit", fg="red", command=self.master.destroy)
        # self.quitBtn.pack(side="bottom", ipadx=20, padx=30)

        self.next.place(rely=1.0, relx=1.0, x=-100, y=0, anchor=tk.SE)
        self.quitBtn.place(rely=1.0, relx=1.0, x=-40, y=0, anchor=tk.SE)


def main():
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry("1200x800")
    # root.geometry("+{}+{}".format(APP_XPOS, APP_YPOS))
    app = Application(root).pack(fill='both', expand=True)
    root.mainloop()


if __name__ == '__main__':
    main()