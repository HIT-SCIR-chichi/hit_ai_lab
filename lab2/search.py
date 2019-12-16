# -*- coding:utf-8 -*-
# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    深度优先搜索算法
    实例化类GenericSearch为dfs,使用util.py中定义的
    数据结构栈Stack来作为open表的数据结构
    param: problem 搜索算法要解决的问题对象
    return值: actions列表,即,吃豆人吃到豆子所执行的一个action序列
    """
    dfs = GenericSearch(problem, util.Stack)
    return dfs.genericSearch()


def breadthFirstSearch(problem):
    """
    广度优先搜索算法
    实例化类GenericSearch为bfs,使用util.py中定义的
    数据结构队列Queue来作为open表的数据结构
    param: problem 搜索算法要解决的问题对象
    return值: actions列表,即,吃豆人吃到豆子所执行的一个action序列
    """
    bfs = GenericSearch(problem, util.Queue)
    return bfs.genericSearch()


def uniformCostSearch(problem):
    """
    代价一致搜索算法
    实例化类GenericSearch为ucs,使用util.py中定义的
    数据结构优先队列PriorityQueue来作为open表的数据结构
    param: problem 搜索算法要解决的问题对象
    return值: actions列表,即,吃豆人吃到豆子所执行的一个action序列
    """
    ucs = GenericSearch(problem, util.PriorityQueue, True)
    return ucs.genericSearch()


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    A*算法
    实例化类GenericSearch为astar,使用util.py中定义的
    数据结构优先队列PriorityQueue来作为open表的数据结构
    同时指定启发式函数heuristic,使用该启发式函数来估算当前结点到目标结点的代价
    param1: problem 搜索算法要解决的问题对象
    param2: heuristic 启发式函数对象
    return值: actions列表,即,吃豆人吃到豆子所执行的一个action序列
    """
    astar = GenericSearch(problem, util.PriorityQueue, True, heuristic)
    return astar.genericSearch()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


class GenericSearch:
    """
    通用的搜索算法类,通过配置不同的参数可以实现DFS,BFS,UCS,A*搜索
    """

    def __init__(self, problem, data_struct_type, usePriorityQueue=False, heuristic=nullHeuristic):
        """
        通过配置不同的参数(搜索算法要解决的问题对象,采用的数据结构,是否使用优先队列[即,是否每条路径具有不同的代价],启发式函数)
        可实现DFS(深度搜索),BFS(广度搜索),UCS(代价一致),A*算法(代价一致+启发式函数)搜索
        param1: problem (搜索算法要解决的问题对象)
        param2: data_struct_type (搜索算法中的open表采用的数据结构)
        param3: usePriorityQueue (bool值,默认False,是否采用优先队列数据结构,用于代价一致搜索和A*搜索算法)
        param4: heuristic (启发式函数,默认为nullHeuristic[返回值为0,相当于没有该函数],用于A*算法)
        """
        self.problem = problem
        self.data_struct_type = data_struct_type
        self.usePriorityQueue = usePriorityQueue
        self.heuristic = heuristic

    def genericSearch(self):
        """
        节点(node)：
        对于DFS和BFS,open表中的每个节点(node)均是(state, actions)的二元组,其中state为状态,即为吃豆人所在的坐标(coord),
        actions为从初始结点到达本状态所要执行的操作序列["South","North",....]
        对于UCS和A*,open表中的每个节点(node)均是((state, actions),cost)的二元组,其中state为状态,即为吃豆人所在的坐标(coord),
        actions为从初始结点到达本状态所要执行的操作序列["South","North",....],cost为从初始结点到当前结点的代价(对于UCS)或
        从初始结点到当前结点的代价+启发式函数值(对于A*)

        return值: actions列表,即,吃豆人吃到豆子所执行的一个action序列
        """
        openList = self.data_struct_type()  # data_struct_type为util中的一个数据结构(Stack、Queue、PriorityQueue)类
        # 将其实例化,创建open表
        if self.usePriorityQueue:  # 判断是否使用优先队列,如果是,则push二元组((state, actions),cost)
            openList.push((self.problem.getStartState(), []),
                          self.heuristic(self.problem.getStartState(),
                                         self.problem))
            """
            需要说明的是:在进行UCS和A*搜索时,usePriorityQueue同样为True,而UCS没有启发式函数,而当进行UCS搜索时同样会进入该if判断,
            那这是为什么呢？因为heuristic默认为函数nullHeuristic(返回值为0),当进行UCS搜索时,不传相应的启发式函数参数即可,
            那就会默认调用函数nullHeuristic,该函数返回值为0,相当于没有。
            """
        else:
            openList.push((self.problem.getStartState(), []))

        closed = []  # 初始化closed表为空表
        while True:
            if openList.isEmpty():  # 如果fringe表为空，则搜索问题无解
                return []
            coord, actions = openList.pop()  # 从open表中pop出一个节点
            """
            注意:当进行UCS和A*搜索时,虽然我们push进入的为((state, actions),cost)结构
            但当pop时,只pop(state, actions),具体可参照util.py文件中的类PriorityQueue中pop函数的实现方式
            """
            if self.problem.isGoalState(coord):  # 如果当前结点是目标状态,则搜索成功,返回操作序列actions
                return actions
            if coord not in closed:  # 若当前结点不在closed表中
                closed.append(coord)  # 将当前结点加入closed表,coord=(x,y)
                for successor_coord, action, step_cost in \
                        self.problem.getSuccessors(coord):
                    """
                    遍历当前结点的后继节点
                    for example, problem.getSuccessors(coord) = [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
                    """
                    if self.usePriorityQueue:
                        """
                        若使用优先队列，则在push时要给出优先级信息,为从起始节点通过actions到达当前结点的代价加
                        以当前结点为参数的启发式函数的值,即((state, actions),cost)
                        """
                        openList.push((successor_coord, actions + [action]),
                                      self.problem.getCostOfActions(actions + [action]) +
                                      self.heuristic(successor_coord, self.problem))
                    else:
                        openList.push((successor_coord, actions + [action]))


bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
