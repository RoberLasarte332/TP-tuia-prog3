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
        frontier.add(root, GreedyBestFirstSearch.heuristic(grid.initial, grid.end))
        
        
        while not frontier.is_empty():
            # Elimina el nodo con el menor valor heurístico en la frontera.
            node = frontier.pop()
            
            # Comprueba si el nodo actual es el objetivo.
            if grid.objective_test(node.state):
                return Solution(node, reached)
            
            # Expande el nodo actual (genera sucesores)
            for action, succesor, step_cost in grid.expand(node.state):
                g_cost = node.cost + step_cost
                
                # Si el sucesor no se ha visitado o se encuentra un camino con menor costo, se agrega a la frontera.
                if succesor not in reached or g_cost < reached[succesor]:
                    child = Node(action, state=succesor,  cost=g_cost, parent=node)
                    reached[succesor] = g_cost
                    h_cost = GreedyBestFirstSearch.heuristic(succesor, grid.objective_test)
                    frontier.add(child, h_cost)
                    
        return NoSolution(reached)
    
    
    def heuristic(a, b):
        """"Función heurística (distancia de Manhattan)"""
        return abs(a.row - b.row) + abs(a.col - b.col)
        
                    
                    
            
        

