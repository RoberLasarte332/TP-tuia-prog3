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
        while not frontier.is_empty():
            node = frontier.remove()

            if grid.objective_test(node.state):
                return Solution(node, reached)
            
            for action in grid.actions(node.state):
                succesor = grid.result(node.state, action)

                if succesor not in reached:
                    son = Node("", succesor, cost=node.cost + grid.individual_cost(node.state, action), parent=node, action=action)
                    reached[succesor] = True
                    frontier.add(son)

        return NoSolution(reached)