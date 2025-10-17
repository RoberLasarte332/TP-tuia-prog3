from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # Initialize explored with the initial state
        explored = {}
        explored[root.state] = True

        # Initialize frontier with the root node
        frontier = StackFrontier()
        frontier.add(root)
        
        while not frontier.is_empty():
            node = frontier.remove()
            
            # Check if the goal is reached
            if grid.objetive_test(node.state):
                return Solution(node, explored)
            
            # Expand node
            for action in grid.actions(node.state):
                succesor = grid.result(node.state, action)
                cost_step = grid.individual_cost(node.state, action)
                g_cost = node.cost + cost_step
                
                if succesor not in explored:
                    child = Node("", state=succesor, cost=g_cost, parent=node, action=action)
                    explored[succesor] = True
                    frontier.add(child)
    

        return NoSolution(explored)
