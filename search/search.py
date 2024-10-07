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
from game import Directions
from typing import List

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




def tinyMazeSearch(problem: SearchProblem) -> List[Directions]:
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    from util import Stack
    nodesToVisit = Stack()
    visited = set()
    nodesToVisit.push((problem.getStartState(), []))
    while nodesToVisit:
        val, temppath = nodesToVisit.pop()
        if problem.isGoalState(val):
            return temppath
        visited.add(val)
        for node in problem.getSuccessors(val):
            if node[0] not in visited:
                nodesToVisit.push((node[0], temppath + [node[1]]))
    return []

    # util.raiseNotDefined()
#     hi chat were gonna make a stack with the node and how to get there
#  we also need to avoid alr visited, so check against list

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    from util import Queue
    nodesToVisit = Queue()
    visited = set()
    nodesToVisit.push((problem.getStartState(), []))
    visited.add(problem.getStartState())
    while nodesToVisit:
        val, temppath = nodesToVisit.pop()
        if problem.isGoalState(val):
            return temppath
        for node in problem.getSuccessors(val):
            if node[0] not in visited:
                nodesToVisit.push((node[0], temppath + [node[1]]))
                visited.add(node[0])
    return []
    #util.raiseNotDefined()
# hi chat i edited bfs after fixing the issue w/ ucs, essentially update does not delete the one down the q

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    nodesToVisit = PriorityQueue()
    visited = set()
    nodesToVisit.push((problem.getStartState(), []), 0)
    while nodesToVisit:
        val, temppath = nodesToVisit.pop()
        if val in visited:
            continue
        visited.add(val)
        if problem.isGoalState(val):
            return temppath
        for node in problem.getSuccessors(val):
            # update OP
            if node[0] not in visited:
                nodesToVisit.update((node[0], temppath + [node[1]]), problem.getCostOfActions(temppath + [node[1]]))
    return []
    #util.raiseNotDefined()

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

"""
AHHHH CHAT I DO NOT KNOW IF I CAN CREATE MY OWN FUNCTION

I WILL MAKE ONE BECAUSE PRIORITYQUEUEWITHFUNCTION SAYS I NEED TO MAKE ONE

IF IT DOESNT WORK PLEASE DONT BE MAD ;-;

"""
def createPriorityFunction(problem, heuristic):
    def priorityFunction(node):
        val, temppath = node
        return problem.getCostOfActions(temppath) + heuristic(val, problem)
    return priorityFunction
# ill be honest i did not know how to create a wrapper function https://www.geeksforgeeks.org/function-wrappers-in-python/

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueueWithFunction
    priorityFunction = createPriorityFunction(problem, heuristic)
    nodesToVisit = PriorityQueueWithFunction(priorityFunction)
    visited = set()
    best = {}
    nodesToVisit.push((problem.getStartState(), []))
    best[problem.getStartState()] = 0
    while nodesToVisit:
        val, temppath = nodesToVisit.pop()
        visited.add(val)
        if problem.isGoalState(val):
            return temppath
        for node in problem.getSuccessors(val):
            nodepath = temppath + [node[1]]
            nodecost = problem.getCostOfActions(nodepath)
            if node[0] not in best or nodecost < best[node[0]]:
                best[node[0]] = nodecost
                nodesToVisit.push((node[0], nodepath))
    return []
    # util.raiseNotDefined()
# ok chat so what i did was i removed the restriction to visit again cuz it says ur gonna visit it again LOL
# we know that u have to keep track of best cost there so i did it w/ dictionary
# essentially if i found a better cost i update the dictionary, then start searching from there as well!

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
