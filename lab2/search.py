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


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def depthFirstSearch(problem):
    """
    DFS                 open表数据结构是util.py中的Stack

    @param problem:     算法中的问题对象实例
    @return:            actions列表，吃豆人吃到豆子所执行的操作序列
    """
    return general_search(problem, util.Stack())


def breadthFirstSearch(problem):
    """
    BFS                 open表数据结构是util.py中的Queue

    @param problem:     算法中的问题对象实例
    @return:            actions列表，吃豆人吃到豆子所执行的操作序列
    """
    return general_search(problem, util.Queue())


def uniformCostSearch(problem):
    """
    UCS                 open表数据结构是util.py中的PriorityQueue

    @param problem:     算法中的问题对象实例
    @return:            actions列表，吃豆人吃到豆子所执行的操作序列
    """
    return general_search(problem, util.PriorityQueue())


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    A*                  open表数据结构是util.py中的PriorityQueue

    @param problem:     算法中的问题对象实例
    @param heuristic:   启发式函数对象，默认为nullHeurisitic
    @return:            actions列表，吃豆人吃到豆子所执行的操作序列
    """
    return general_search(problem, util.PriorityQueue(), heuristic)


def general_search(prob, open_lst, heuristic=nullHeuristic):
    """
    不同的输入参数，可以分别实现DFS、BFS、UCS和A*搜索
    state:              吃豆人坐标(x,y)
    actions:            action列表，初始结点到当前坐标的操作序列
    is_pri:             标识open_lst是否为util.PriorityQueue对象实例
    cost:               对于UCS，其为初始结点到当前结点的代价
                        对于A*，其为初始结点到当前结点的代价+启发式函数值
    DFS and BFS:        open_lst中元素为(state, actions)
    UCS and A*:         open_lst中元素为((state, actions),cost)

    @param prob:        搜索算法要解决的问题对象
    @param open_lst:    搜索算法中的open_lst采用的数据结构
    @param heuristic:   默认为nullHeuristic函数，是启发式函数，用于A*和UCS算法
    @return:            actions列表,吃豆人吃到豆子所执行的操作序列
    """
    close_lst, is_pri = [], isinstance(open_lst, util.PriorityQueue)
    item = (prob.getStartState(), [])
    open_lst.push(item, heuristic(prob.getStartState(), prob)) if is_pri else open_lst.push(item)
    while not open_lst.isEmpty():
        state, actions = open_lst.pop()  # 取一个拓展节点
        if prob.isGoalState(state):  # 拓展节点为目标节点
            return actions
        if state not in close_lst:  # 当前结点未被拓展过
            close_lst.append(state)  # 将当前结点坐标加入close表
            for successor_state, action, step_cost in prob.getSuccessors(state):
                item = (successor_state, actions + [action])
                open_lst.push(item, prob.getCostOfActions(actions + [action]) + heuristic(
                    successor_state, prob)) if is_pri else open_lst.push(item)
    return []  # open_lst为空，说明问题无解


bfs = breadthFirstSearch
dfs = depthFirstSearch
ucs = uniformCostSearch
astar = aStarSearch
