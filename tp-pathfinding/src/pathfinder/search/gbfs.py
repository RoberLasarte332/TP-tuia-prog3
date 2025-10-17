from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = root.cost

        # Initialize frontier with the root node
        frontier = PriorityQueueFrontier()
        frontier.add(root, grid.heuristic(grid.initial, grid.end))
        
        
        while not frontier.is_empty():
            # Elimina el nodo con el menor valor heurístico en la frontera.
            node = frontier.pop()
            
            # Comprueba si el nodo actual es el objetivo.
            if grid.objective_test(node.state):
                return Solution(node, reached)
            
            # Expande el nodo actual (genera sucesores)
            for action in grid.actions(node.state):
                successor = grid.result(node.state, action)
                step_cost = grid.individual_cost(node.state, action)
                g_cost = node.cost + step_cost
                
                # Si el sucesor no se ha visitado o se encuentra un camino con menor costo, se agrega a la frontera.
                if successor not in reached or g_cost < reached[successor]:
                    child = Node("", state=successor,  cost=g_cost, parent=node, action=action)
                    reached[successor] = g_cost
                    h_cost = grid.heuristic(successor, grid.end)
                    frontier.add(child, h_cost)
                    
        return NoSolution(reached)