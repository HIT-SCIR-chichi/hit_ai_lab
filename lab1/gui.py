# -*- coding: utf-8 -*-
from PIL import Image, ImageTk
from tkinter import ttk
from system import run
import tkinter as tk
import time

Pos = ['A', 'B', 'C']  # 默认位置A在最左边，B在中间，C在最右边
Rate = 100  # 刷新时间单位为ms
width, height = 960, 540
On_Box = ['否', '是']


def run_model():
    start_state = [monkey_combo.get(), box_combo.get(), banana_combo.get(), is_on_box_combo.get()]
    set_pos(start_state)
    system = run(start_state)
    for state, route in zip(system.states, system.routes):
        time.sleep(Rate / 1000)  # 这里采用暴力的阻塞式睡眠
        set_pos(state)
        print(state, route)
    return system.states, system.routes


def set_pos(start_state):
    p_monkey, p_box, p_banana, is_on_box = start_state
    ii, jj, kk = Pos.index(p_monkey) * 2 + 1, Pos.index(p_box) * 2 + 1, Pos.index(p_banana) * 2 + 1
    aa = On_Box.index(is_on_box) * img_1.height()
    monkey_img.place(x=ii * width / 8 - img_0.width() / 2, y=height - img_0.height() - aa)
    box_img.place(x=jj * width / 8 - img_1.width() / 2, y=height - img_1.height())
    banana_img.place(x=kk * width / 8 - img_2.width() / 2, y=height / 3 - img_2.height())


def add_display():
    display_txt.insert('end', '好的')
    display_txt.configure(state='disabled')
    display_txt.place(x=3 * width / 4, y=2 * height / 3)


root = tk.Tk()
root.resizable(width=False, height=False)
root.iconbitmap('./image/system.ico')
root.geometry('960x540+480+270')
root.title('知识表示')

canvas = tk.Canvas(root, width=width, height=height)
canvas.place(x=0, y=0)
for i in range(1, 4):
    canvas.create_line(i * width / 4, 0, i * width / 4, height, fill='green', width=2)
for i in range(1, 3):
    canvas.create_line(0, i * height / 3, width, i * height / 3, fill='green', width=2)

img_0 = ImageTk.PhotoImage(Image.open('./image/monkey.png').resize((100, 100), Image.ANTIALIAS))
monkey_img = tk.Label(root, image=img_0)
monkey_img.place(x=width / 8 - img_0.width() / 2, y=height - img_0.height())

img_1 = ImageTk.PhotoImage(Image.open('./image/box.jpg').resize((100, 100), Image.ANTIALIAS))
box_img = tk.Label(root, image=img_1)
box_img.place(x=3 * width / 8 - img_1.width() / 2, y=height - img_1.height())

img_2 = ImageTk.PhotoImage(Image.open('./image/banana.jpg').resize((100, 50), Image.ANTIALIAS))
banana_img = tk.Label(root, image=img_2)
banana_img.place(x=5 * width / 8 - img_2.width() / 2, y=height / 3 - img_2.height())

button_width, button_height = 100, 30
run_button = tk.Button(root, text='运行', command=run_model, bitmap='info', width=button_width,
                       height=button_height, compound=tk.LEFT)
run_button.place(x=7 * width / 8 - button_width / 2, y=0)
monkey_combo = ttk.Combobox(root, state='readonly')
monkey_combo['values'] = ('猴子位置', 'A', 'B', 'C')  # 设置下拉列表的值
monkey_combo.current(0)
monkey_combo.place(x=7 * width / 8 - 100, y=0 + 30)

box_combo = ttk.Combobox(root, state='readonly')
box_combo['values'] = ('箱子位置', 'A', 'B', 'C')  # 设置下拉列表的值
box_combo.current(0)
box_combo.place(x=7 * width / 8 - 100, y=30 * 2)

banana_combo = ttk.Combobox(root, state='readonly')
banana_combo['values'] = ('香蕉位置', 'A', 'B', 'C')  # 设置下拉列表的值
banana_combo.current(0)
banana_combo.place(x=7 * width / 8 - 100, y=30 * 3)

is_on_box_combo = ttk.Combobox(root, state='readonly')
is_on_box_combo['values'] = ('猴子在箱子上', '是', '否')  # 设置下拉列表的值
is_on_box_combo.current(0)
is_on_box_combo.place(x=7 * width / 8 - 100, y=30 * 4)

display_txt = tk.Text(root, state='normal')
state_txt = tk.Text(root, state='normal')
add_display()
root.mainloop()
