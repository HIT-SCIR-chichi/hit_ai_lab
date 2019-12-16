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
    深度优先搜索算法
    实例化类GenericSearch为dfs, 使用util.py中定义的数据结构栈Stack来作为open表的数据结构

    @param problem:     搜索算法要解决的问题对象
    @return:            actions列表,即,吃豆人吃到豆子所执行的一个action序列
    """
    dfs = GenericSearch(problem, util.Stack)
    return dfs.genericSearch()


def breadthFirstSearch(problem):
    """
    广度优先搜索算法
    实例化类GenericSearch为bfs,使用util.py中定义的数据结构队列Queue来作为open表的数据结构

    @param problem:     搜索算法要解决的问题对象
    @return:            actions列表,即,吃豆人吃到豆子所执行的一个action序列
    """
    bfs = GenericSearch(problem, util.Queue)
    return bfs.genericSearch()


def uniformCostSearch(problem):
    """
    代价一致搜索算法
    实例化类GenericSearch为ucs,使用util.py中定义的数据结构优先队列PriorityQueue来作为open表的数据结构

    @param problem:     搜索算法要解决的问题对象
    @return:            actions列表,即,吃豆人吃到豆子所执行的一个action序列
    """
    ucs = GenericSearch(problem, util.PriorityQueue, True)
    return ucs.genericSearch()


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    A*算法
    实例化类GenericSearch为astar,使用util.py中定义的数据结构
    优先队列PriorityQueue来作为open表的数据结构同时指定启发式函数heuristic,
    使用该启发式函数来估算当前结点到目标结点的代价

    @param problem:     搜索算法要解决的问题对象
    @param heuristic:   启发式函数对象
    @return:            actions列表,即,吃豆人吃到豆子所执行的一个action序列
    """
    astar = GenericSearch(problem, util.PriorityQueue, True, heuristic)
    return astar.genericSearch()


class GenericSearch:
    """
    通用的搜索算法类,通过配置不同的参数可以实现DFS,BFS,UCS,A*搜索
    """

    def __init__(self, problem, struct_type, use_pri_queue=False, heuristic=nullHeuristic):
        """
        不同的参数可实现不同的搜索策略：DFS、BFS、UCS、A*算法

        @param problem:         搜索算法要解决的问题对象
        @param struct_type:     搜索算法中的open表采用的数据结构
        @param use_pri_queue:   bool值,默认False,是否采用优先队列数据结构,用于代价一致搜索和A*搜索算法
        @param heuristic:       默认为nullHeuristic函数，是启发式函数，用于A*和UCS算法
        """
        self.problem = problem
        self.struct_type = struct_type
        self.use_pri_queue = use_pri_queue
        self.heuristic = heuristic

    def genericSearch(self):
        """
        state:      吃豆人目前坐标
        actions:    从初始结点到当前坐标的操作序列，形如["South","North",....]
        cost:       对于UCS，其为从初始结点到当前结点的代价
                    对于A*，其为从初始结点到当前结点的代价+启发式函数值
        DFS+BFS:    open表中节点为(state, actions)二元组
        UCS+A*:     open表中节点为((state, actions),cost)二元组

        @return:    actions列表
        """
        open_lst, close_lst = self.struct_type, []
        item = (self.problem.getStartState, [])
        open_lst.push((item, self.heuristic(self.problem.getStartState, self.problem))
                      if self.use_pri_queue else item)
        while True:
            if open_lst.isEmpty():  # 如果open表为空，则搜索问题无解
                return []
            coord, actions = open_lst.pop()
            if self.problem.isGoalState(coord):
                return actions
            if coord not in close_lst:  # 若当前结点不在closed表中
                close_lst.append(coord)  # 将当前结点加入closed表,coord=(x,y)
                for successor_coord, action, step_cost in self.problem.getSuccessors(coord):
                    # 遍历当前结点的后继节点for example, problem.getSuccessors(coord) = [((5, 4), 'South', 1), ((4, 5), 'West', 1)]
                    if self.use_pri_queue:
                        # 若使用优先队列，则在push时要给出优先级信息,为从起始节点通过actions到达当前结点的代价
                        # 加以当前结点为参数的启发式函数的值,即((state, actions),cost)
                        open_lst.push((successor_coord, actions + [action]),
                                      self.problem.getCostOfActions(actions + [action]) +
                                      self.heuristic(successor_coord, self.problem))
                    else:
                        open_lst.push((successor_coord, actions + [action]))


bfs = breadthFirstSearch
dfs = depthFirstSearch
ucs = uniformCostSearch
astar = aStarSearch
