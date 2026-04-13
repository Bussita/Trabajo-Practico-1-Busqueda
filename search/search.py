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

from util import *
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
    fringe = Stack()
    start_state = problem.getStartState()
    fringe.push((start_state, [])) # Guardamos (estado, camino de acciones)

    visited = set()

    while not fringe.isEmpty():
        current_state, actions = fringe.pop()
        print("Current State: ", current_state)
        print("Actions: ", actions)
        if problem.isGoalState(current_state):
            return actions
        
        if current_state not in visited: 
            # Si el estado actual ya fue visitado, se salta el bloque if y se sigue con la siguiente
            # iteracion del while. Esto hace que se eviten los ciclos dentro del grafo (en nuestro caso la grilla)
            # y que ademas se ahorren iteraciones si hay múltiples caminos hacia un mismo nodo.
            visited.add(current_state)
            for succesor, action, cost in problem.getSuccessors(current_state):
                new_actions = actions + [action] # Meto al final la accion de ir al siguiente estado
                fringe.push((succesor, new_actions))

    return []

def breadthFirstSearch(problem: SearchProblem) -> List[Directions]:
    """Search the shallowest nodes in the search tree first."""
    fringe = Queue()
    start_state = problem.getStartState()
    fringe.push((start_state, []))  # Guardamos (estado, camino de acciones)

    visited = set()

    while not fringe.isEmpty():
        current_state, actions = fringe.pop()
        if problem.isGoalState(current_state):
            return actions

        if current_state not in visited:
            visited.add(current_state)
            for succesor, action, cost in problem.getSuccessors(current_state):
                new_actions = actions + [action]
                fringe.push((succesor, new_actions))

    return []

def uniformCostSearch(problem: SearchProblem) -> List[Directions]:
    """Search the node of least total cost first."""
    start_state = problem.getStartState()
    visited = set()
    fringe = PriorityQueue()
    fringe.push((start_state, [] ), 0)
    while not fringe.isEmpty():
        current_state, actions = fringe.pop()
        if problem.isGoalState(current_state):
            return actions
        if current_state not in visited:
            visited.add(current_state)
            for successor, action, stepCost in problem.getSuccessors(current_state):
                if successor not in visited:
                    new_actions = actions + [action]
                    cost = problem.getCostOfActions(new_actions)
                    fringe.push((successor, new_actions), cost)
    return []

def nullHeuristic(state, problem=None) -> float:
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

"""
Usar:
python pacman.py -l mediumMaze -p SearchAgent -a fn=astar,heuristic=manhattanHeuristic
TODO: ManhattanHeuristica ya estaba definido como una heuristica, deberiamos hacer otra? 
"""
def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> List[Directions]:
    """Search the node that has the lowest combined cost and heuristic first."""
    # Hacemos una cola de prioridad donde la mayor prioridad la tienen los menos costosos.
    fringe = PriorityQueue()
    start_state = problem.getStartState()
    # Guardamos (estado, acciones); prioridad = g(n) + h(n)
    fringe.push((start_state, []), heuristic(start_state, problem)) # En el estado inicial el valor es 0 + h

    # Usamos un diccionario como estructura de datos para manejar los visitados, la razon para esto
    # es que A* puede revisitar nodos pero esta vez llegando con un costo mas bajo y entonces
    # deberiamos volver a expandir con este costo.
    visited = {}

    while not fringe.isEmpty():
        current_state, actions = fringe.pop()

        current_cost = problem.getCostOfActions(actions) # Calculamos g(n)

        if problem.isGoalState(current_state):
            return actions

        if current_state not in visited or (current_state in visited and current_cost < visited[current_state]):
            # Esto es, si no visitamos ya a current_state O si lo hemos visitado antes, ahora le llegamos con un costo menor.
            visited[current_state] = current_cost
            for successor, action, stepCost in problem.getSuccessors(current_state):
                    new_actions = actions + [action]
                    g = problem.getCostOfActions(new_actions)   # costo real acumulado
                    h = heuristic(successor, problem)           # estimacion heuristica
                    fringe.push((successor, new_actions), g + h)
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
