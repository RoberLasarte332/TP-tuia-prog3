from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize root node
        root = Node("", state=grid.initial, cost=0, parent=None, action=None) 
        root.estimated_distance=grid.heuristic(grid.initial)

        # Initialize reached with the initial state
        reached = {}
        reached[root.state] = root.cost

        # Initialize frontier with the root node
        frontier = PriorityQueueFrontier()
        frontier.add(root, root.cost + root.estimated_distance)
        # TODO Complete the rest!!
        # ...
        while not frontier.is_empty():
            node = frontier.pop()
            if grid.objective_test(node.state):
                return Solution(node, reached)
            
            for action in grid.actions(node.state):
                succesor = grid.result(node.state, action)
                cost_step = grid.individual_cost(node.state, action)
                g_cost = node.cost + cost_step
                h_cost = grid.heuristic(succesor)

                if succesor not in reached or g_cost < reached[succesor]:
                    son = Node("", state=succesor, cost=g_cost, parent=node, action=action) 
                    son.estimated_distance=h_cost 
                    reached[succesor] = g_cost
                    frontier.add(son, g_cost + h_cost)

        return NoSolution(reached)
