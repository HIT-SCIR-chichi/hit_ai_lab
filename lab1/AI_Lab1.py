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
            猴子目前在%s处
            猴子到%s处
            猴子推着箱子到%s处
            猴子爬上箱子
            猴子从箱子上爬下来
            猴子拿到了香蕉
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
    return system


if __name__ == "__main__":
    s = input('请输入状态: 猴子位置(A/B/C), 箱子位置(A/B/C), 香蕉位置(A/B/C), 猴子是否在箱子上(是/否)\n')
    run(tuple(s.split(' ')))
