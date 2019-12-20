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
    UCS                 open表数据结构是util.PriorityQueueWithFunction

    @param problem:     算法中的问题对象实例
    @return:            actions列表，吃豆人吃到豆子所执行的操作序列
    """
    priorityFunction = lambda item: problem.getCostOfActions(item[1])
    return general_search(problem, util.PriorityQueueWithFunction(priorityFunction))


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    A*                  open表数据结构是util.PriorityQueueWithFunction

    @param problem:     算法中的问题对象实例
    @param heuristic:   启发式函数对象，默认为nullHeurisitic
    @return:            actions列表，吃豆人吃到豆子所执行的操作序列
    """
    priorityFunction = lambda item: problem.getCostOfActions(item[1]) + heuristic(item[0], problem)
    return general_search(problem, util.PriorityQueueWithFunction(priorityFunction))


def general_search(prob, open_lst):
    """
    不同的输入参数，可以分别实现DFS、BFS、UCS和A*搜索
    state:              吃豆人坐标(x,y)
    actions:            action列表，初始结点到当前坐标的操作序列
    cost:               对于UCS，其为初始结点到当前结点的代价
                        对于A*，其为初始结点到当前结点的代价+启发式函数值
                        可由PriorityQueueWithFunction的优先级函数根据state和actions计算得到
    DFS and BFS:        open_lst中元素为(state, actions)
    UCS and A*:         open_lst中元素为(state,actions),cost

    @param prob:        搜索算法要解决的问题对象
    @param open_lst:    搜索算法中的open_lst采用的数据结构
    @return:            actions列表,吃豆人吃到豆子所执行的操作序列
    """
    closed_lst = []
    open_lst.push((prob.getStartState(), []))
    while not open_lst.isEmpty():
        state, actions = open_lst.pop()  # 取一个拓展节点
        if prob.isGoalState(state):  # 拓展节点为目标节点
            return actions
        if state not in closed_lst:  # 当前结点未被拓展过
            closed_lst.append(state)  # 将当前结点坐标加入close表
            for successor_state, action, step_cost in prob.getSuccessors(state):
                open_lst.push((successor_state, actions + [action]))
    return []  # open_lst为空，说明问题无解


bfs = breadthFirstSearch
dfs = depthFirstSearch
ucs = uniformCostSearch
astar = aStarSearch
