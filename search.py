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
import sys
import node
import searchAgents
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
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem): #Same as slides
    n = node.Node(problem.getStartState())
    if problem.isGoalState(problem.getStartState()):
        return n.total_path()

    fringe = util.Stack() #Stack as fringe
    fringe.push(n)
    generated = set()

    while not fringe.isEmpty():
        n = fringe.pop()
        generated.add(n.state)

        for successor, action, cost in (problem.getSuccessors(n.state)):
            ns = node.Node(successor, n, action, n.cost + cost)
            if ns.state not in generated: # Not in expanded or fringe
                if problem.isGoalState(ns.state):
                    return ns.total_path()
                fringe.push(ns)
                generated.add(ns.state) # Add to expanded (Fringe)

    print("No solution for this problem.")
    sys.exit(-1)

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"

    n = node.Node(problem.getStartState())
    if problem.isGoalState(problem.getStartState()):
        return n.total_path()

    fringe = util.Queue() #Queue as fringe
    fringe.push(n)
    generated = set()

    while not fringe.isEmpty():
        n = fringe.pop()
        generated.add(n.state)  # Add to generated

        for successor, action, cost in (problem.getSuccessors(n.state)):
            ns = node.Node(successor, n, action, n.cost + cost)
            if ns.state not in generated:  # Not in expanded or fringe
                if problem.isGoalState(ns.state):
                    return ns.total_path()
                fringe.push(ns)
                generated.add(ns.state)  # Add to expanded (Fringe)

    print("No solution for this problem.")
    sys.exit(-1)

def uniformCostSearch(problem):
    n = node.Node(problem.getStartState())
    if problem.isGoalState(problem.getStartState()):
        return n.total_path()
    fringe = util.PriorityQueue() #Priority Queue as fringe
    expanded = {}
    fringe.push(n, 0) #Push the start node with cost 0
    expanded[n.state] = ("F", 0) #Fringe and cost
    while not fringe.isEmpty():
        n = fringe.pop()
        if problem.isGoalState(n.state):
            return n.total_path()
        expanded[n.state] = ("E", n.cost) #Expanded and cost
        for successor, action, cost in (problem.getSuccessors(n.state)):
            ns = node.Node(successor, n, action, n.cost + cost)
            if ns.state not in expanded:
                fringe.push(ns, ns.cost)
                expanded[ns.state] = ("F", ns.cost)
            elif expanded[ns.state][0] == "F" and expanded[ns.state][1] > ns.cost:
                fringe.update(ns, ns.cost)
                expanded[ns.state] = ("F", ns.cost)

    print("No solution for this problem.")
    sys.exit(-1)

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return util.manhattanDistance(state, problem.goal)

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    #Copied from uniformCostSearch and added heuristic as sum into the cost of the node
    n = node.Node(problem.getStartState())
    if problem.isGoalState(problem.getStartState()):
        return n.total_path()
    fringe = util.PriorityQueue()
    expanded = {}
    fringe.push(n, 0)
    expanded[n.state] = ("F", 0)
    while not fringe.isEmpty():
        n = fringe.pop()
        if problem.isGoalState(n.state):
            return n.total_path()
        expanded[n.state] = ("E", n.cost)
        for successor, action, cost in (problem.getSuccessors(n.state)):
            ns = node.Node(successor, n, action, n.cost + cost + heuristic(successor, problem)) #Added heuristic
            if ns.state not in expanded:
                fringe.push(ns, ns.cost)
                expanded[ns.state] = ("F", ns.cost)
            elif expanded[ns.state][0] == "F" and expanded[ns.state][1] > ns.cost:
                fringe.update(ns, ns.cost)
                expanded[ns.state] = ("F", ns.cost)

    print("No solution for this problem.")
    sys.exit(-1)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch