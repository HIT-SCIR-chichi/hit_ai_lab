# -*- coding: utf-8 -*-
from PIL import Image, ImageTk
from tkinter import ttk
from system import run
import tkinter as tk
import time

Start_State = ('A', 'B', 'C', '否')
Pos = ['A', 'B', 'C']  # 默认位置A在最左边，B在中间，C在最右边
Rate = 500  # 刷新时间单位为ms
width, height = 960, 540
On_Box = ['否', '是']
Font = 'Arial, 10'
Fg = 'green'


def set_img(start_state):  # 根据状态设置图像位置
    p_monkey, p_box, p_banana, is_on_box = start_state
    ii, jj, kk = Pos.index(p_monkey) * 2 + 1, Pos.index(p_box) * 2 + 1, Pos.index(p_banana) * 2 + 1
    aa = On_Box.index(is_on_box) * img_1.height()
    bb = 1 if start_state[0] == start_state[1] and start_state[3] == '否' else 0
    monkey_img.place(x=ii * width / 8 - img_0.width() * (bb + 1) / 2,
                     y=height - img_0.height() - aa)
    box_img.place(x=jj * width / 8 - abs(bb - 1) * img_1.width() / 2, y=height - img_1.height())
    banana_img.place(x=kk * width / 8 - img_2.width() / 2, y=height / 3 - img_2.height())


def set_txt(idx, state, route):
    display_txt.configure(state='normal')
    display_txt.insert('end', '\n' + str(idx) + route + '\t')
    display_txt.configure(state='disabled')
    set_state(state)


def add_combobox():
    combo_height = 30
    monkey_combo['values'] = ('猴子位置', 'A', 'B', 'C')  # 设置下拉列表的值
    monkey_combo.current(0)
    monkey_combo.place(x=7 * width / 8 - 100, y=combo_height)

    box_combo['values'] = ('箱子位置', 'A', 'B', 'C')  # 设置下拉列表的值
    box_combo.current(0)
    box_combo.place(x=7 * width / 8 - 100, y=combo_height * 2)

    banana_combo['values'] = ('香蕉位置', 'A', 'B', 'C')  # 设置下拉列表的值
    banana_combo.current(0)
    banana_combo.place(x=7 * width / 8 - 100, y=combo_height * 3)

    is_on_box_combo['values'] = ('猴子在箱子上', '是', '否')  # 设置下拉列表的值
    is_on_box_combo.current(0)
    is_on_box_combo.place(x=7 * width / 8 - 100, y=combo_height * 4)


def set_state(state):
    display_state_0['text'] = '猴子默认位置：' + state[0]
    display_state_1['text'] = '箱子默认位置：' + state[1]
    display_state_2['text'] = '香蕉默认位置：' + state[2]
    display_state_3['text'] = '猴子默认状态：' + state[3]


def add_display():
    display_state_0.place(x=3 * width / 4 + 1, y=height / 3 + 1)
    display_state_1.place(x=3 * width / 4 + 1, y=height / 3 + 1 + 25)
    display_state_2.place(x=3 * width / 4 + 1, y=height / 3 + 1 + 25 * 2)
    display_state_3.place(x=3 * width / 4 + 1, y=height / 3 + 1 + 25 * 3)
    set_state(Start_State)

    display_txt.place(x=3 * width / 4, y=2 * height / 3)
    display_txt.insert('end', '猴子运行输出\n**************************')
    display_txt.configure(state='disabled')


def run_model():
    start_state = (monkey_combo.get(), box_combo.get(), banana_combo.get(), is_on_box_combo.get())
    set_img(start_state)
    system = run(start_state)
    for idx, (state, route) in enumerate(zip(system.states, system.routes)):
        time.sleep(Rate / 1000)  # 这里采用暴力的阻塞式睡眠
        set_img(state)
        set_txt(idx, state, route)
        root.update()
    return system.states, system.routes


root = tk.Tk()
root.resizable(width=False, height=False)
root.iconbitmap('./image/system.ico')
root.geometry('960x540+480+270')
root.title('知识表示')

canvas = tk.Canvas(root, width=width, height=height)
canvas.place(x=0, y=0)
for i in range(1, 4):
    canvas.create_line(i * width / 4, 0, i * width / 4, height, fill='green', width=1)
    canvas.create_text((2 * i - 1) * width / 8, height / 3 + 50, text=Pos[i - 1])
for i in range(1, 3):
    canvas.create_line(0, i * height / 3, width, i * height / 3, fill='green', width=1)

img_0 = ImageTk.PhotoImage(Image.open('./image/monkey.png').resize((100, 100), Image.ANTIALIAS))
img_1 = ImageTk.PhotoImage(Image.open('./image/box.jpg').resize((100, 100), Image.ANTIALIAS))
img_2 = ImageTk.PhotoImage(Image.open('./image/banana.jpg').resize((100, 50), Image.ANTIALIAS))
monkey_img = tk.Label(root, image=img_0)
box_img = tk.Label(root, image=img_1)
banana_img = tk.Label(root, image=img_2)
set_img(Start_State)

run_button = tk.Button(root, text='运行', command=run_model, font=Font, fg=Fg)
run_button.place(x=7 * width / 8 - 25, y=0)

monkey_combo = ttk.Combobox(root, state='readonly')
box_combo = ttk.Combobox(root, state='readonly')
banana_combo = ttk.Combobox(root, state='readonly')
is_on_box_combo = ttk.Combobox(root, state='readonly')
add_combobox()

display_txt = tk.Text(root, font=Font, fg=Fg)
display_state_0 = tk.Label(root, font=Font, fg=Fg)
display_state_1 = tk.Label(root, font=Font, fg=Fg)
display_state_2 = tk.Label(root, font=Font, fg=Fg)
display_state_3 = tk.Label(root, font=Font, fg=Fg)
add_display()

root.mainloop()
