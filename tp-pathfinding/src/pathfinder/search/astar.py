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
        
        #Bucle principal
        while not frontier.is_empty():
            #Extrae el nodo con el menor costo estimado total
            node = frontier.pop()
            
            #Si el nodo actual cumple el objetivo, se devuelve la solución
            if grid.objective_test(node.state):
                return Solution(node, reached)
            
            #Recorre todas las acciones posibles desde el estado actual
            for action in grid.actions(node.state):
                #Calcula el estado sucesor al aplicar la acción
                succesor = grid.result(node.state, action)
                #Costo del paso entre el nodo actual y el sucesor
                cost_step = grid.individual_cost(node.state, action)
                #Costo acumulado hasta el sucesor
                g_cost = node.cost + cost_step
                #Costo heurístico desde el sucesor hasta el objetivo
                h_cost = grid.heuristic(succesor)
                
                
                #Si el sucesor no fue alcanzado o encontramos un camino más barato
                if succesor not in reached or g_cost < reached[succesor]:
                    #Crea el nuevo nodo hijo con su costo acumulado
                    son = Node("", state=succesor, cost=g_cost, parent=node, action=action) 
                    son.estimated_distance=h_cost  #Guarda la estimación heurística
                    reached[succesor] = g_cost #Actualiza el costo más bajo encontrado para ese estado
                    frontier.add(son, g_cost + h_cost)  #Agrega el nodo hijo a la frontera 

        #Si la frontera se vacía sin encontrar el objetivo, no hay solución
        return NoSolution(reached)
