from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = True

        # Initialize frontier with the root node
        frontier = QueueFrontier()
        frontier.add(root)
        # TODO Complete the rest!!
        # ...
        
        
        #Bucle principal
        while not frontier.is_empty():
            node = frontier.remove() #Saca el primer nodo agregado
            
            #Si llega al objetivo, devuelve la solución
            if grid.objective_test(node.state):
                return Solution(node, reached)
            
            
            #Expande los sucesores del nodo actual
            for action in grid.actions(node.state):
                succesor = grid.result(node.state, action)

                #Si el sucesor no fue visitado, lo agrega a la frontera
                if succesor not in reached:
                    son = Node("", succesor, cost=node.cost + grid.individual_cost(node.state, action), parent=node, action=action)
                    reached[succesor] = True
                    frontier.add(son)

        #Si no se encuentra el objetivo, devuelve "Sin solución"
        return NoSolution(reached)