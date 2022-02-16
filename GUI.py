from tkinter import *
from PIL import Image, ImageTk
import exhentai


class Gui(object):
    def __init__(self):
        self.root = Tk()
        self.root.title('EXDownloader')
        self.text1 = Label(self.root, text="一、開始新一輪的漫畫下載", bd=10)
        self.text1.grid(row=0)
        self.text2 = Label(self.root, text="輸入本子網址: ")
        self.text2.grid(row=1, column=0)
        self.input_url = Entry(self.root)
        self.input_url.grid(row=1, column=1)
        self.btn1 = Button(self.root, text="開始下載", command = self.get_url)
        self.btn1.grid(row=2, column=1)
        self.text3 = Label(self.root, text='二、接續前一輪中斷的漫畫下載', bd=10)
        self.text3.grid(row=3)
        self.text4 = Label(self.root, text='輸入本子網站: ')
        self.text4.grid(row=4, column=0)
        self.input_url2 = Entry(self.root)
        self.input_url2.grid(row=4, column=1)
        self.text5 = Label(self.root, text='輸入指定頁數: ')
        self.text5.grid(row=5, column=0)
        self.input_page = Entry(self.root)
        self.input_page.grid(row=5, column=1)
        self.btn2 = Button(self.root, text='開始下載', command = self.get_url2)
        self.btn2.grid(row=6, column=1)
        self.output = Label(self.root, text='歡迎使用本程式', bd=10)
        self.output.grid(row=8, column=0)
        self.text6 = Label(self.root, text='Copyright © 2021 shisukon0210.')
        self.text6.grid(row=7, column=0)
        self.img_open = Image.open('./icon/shizika.jpg')
        self.img1 = ImageTk.PhotoImage(self.img_open)
        self.label_img = Label(self.root, image=self.img1)
        self.label_img.grid(row=0, rowspan=9, column=2, padx=5, pady=5)


    def get_url(self):
        url = self.input_url.get()
        exhentai.downloader_a(url)

    def get_url2(self):
        url2 = self.input_url2.get()
        page = int(self.input_page.get())
        exhentai.downloader_b(url2, page)

    def print_output(self, str):
        self.output = Label(self.root, text=str, bd=10)

if __name__ == "__main__":
    G = Gui()
    mainloop()

