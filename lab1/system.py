# -*- coding: utf-8 -*-
class System:
    """
    要求：每次执行一个操作后，要同时修改以下两个列表
        States中每一个元素均为四元组(x,y,z,w)
            x表示猴子位置，取值范围['A','B','C']
            y表示箱子位置，取值范围['A','B','C']
            z表示香蕉位置，取值范围['A','B','C']
            w表示猴子是否在箱子上，取值范围['是','否']
        Routes中每一个元素均为要输出的合适的操作语句，可取的文字为
            猴子目前在%s处、猴子到%s处、猴子推着箱子到%s处
            猴子爬上箱子、猴子从箱子上爬下来、猴子拿到了香蕉
    """

    def __init__(self, start_state, start_route):
        self.__states = [start_state]
        self.__routes = [start_route]
        self.__count = 0

    def append(self, state, route):  # 每次更新必须调用此方法
        self.__states.append(state)
        self.__routes.append(route)
        self.__count += 1

    @property
    def states(self):
        return self.__states[:]  # 第一层拷贝

    @property
    def routes(self):
        return self.__routes[:]  # 第一层拷贝

    def current_state(self):
        """
        获取当前状态
        """
        return self.__states[self.__count]

    """
    表示猴子运动的函数
    """

    def monkey_go(self, x):
        old_state = self.current_state()
        new_state = (x, old_state[1], old_state[2], old_state[3])
        self.append(new_state, "猴子到" + x + "处")  # 在状态列表里添加状态

    """
    表示猴子推箱子的函数
    """

    def move_box(self, y):
        old_state = self.current_state()
        new_state = (y, y, old_state[2], old_state[3])
        # 在状态列表里添加状态
        self.append(new_state, "猴子推着箱子到" + y + "处")

    """
    表示猴子爬上箱子的函数
    """

    def climb_on(self):
        old_state = self.current_state()
        new_state = (old_state[0], old_state[1], old_state[2], '是')
        self.append(new_state, "猴子爬上箱子")  # 在状态列表里添加状态

    """
    表示猴子从箱子上爬下来的函数
    """

    def climb_down(self):
        old_state = self.current_state()
        new_state = (old_state[0], old_state[1], old_state[2], '否')
        self.append(new_state, "猴子从箱子上爬下来")  # 在状态列表里添加状态


def run(start_state):  # 输入参数为含有4元组，格式如上图规约，该函数被GUI模块调用
    (monkey, box, banana, on_box), pos_lst = start_state, ['A', 'B', 'C']
    if monkey not in pos_lst or box not in pos_lst or banana not in pos_lst or on_box \
            not in ['是', '否'] or (on_box == '是' and monkey != box):
        print("输入不符合格式！")
        exit(-1)
    system = System(start_state, '猴子开始运动')
    """
    完善代码，调用system.append()修改状态，调用system.current_state()获取当前最新状态
    """
    while not (system.current_state()[0] == system.current_state()[1] and
               system.current_state()[1] == system.current_state()[2] and system.current_state()[
                   3] == "是"):
        now_state = system.current_state()
        if now_state[1] == now_state[2]:  # 箱子和香蕉同位置
            system.climb_on() if now_state[0] == now_state[1] else system.monkey_go(now_state[1])
        else:  # 箱子和香蕉不同位置
            if now_state[0] == now_state[1]:  # 猴子和箱子同位置
                system.climb_down() if now_state[3] == "是" else system.move_box(now_state[2])
            else:
                system.monkey_go(now_state[1])
    return system


if __name__ == "__main__":
    s = input('请输入状态: 猴子位置(A/B/C), 箱子位置(A/B/C), 香蕉位置(A/B/C), 猴子是否在箱子上(是/否)\n')
    run(tuple(s.split(' ')))
