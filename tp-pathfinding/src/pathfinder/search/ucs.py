from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """ Encuentra el camino entre dos puntos en una grilla usando Búsqueda de Costo Uniforme.
            Este algoritmo se basa en explorar siempre el camino con el menor costo acumulado.
     
        Argumentos:
            grid (Grid): Grid of points

        Retorna:
            Solucion: Solucion encontrada
        """

        # Inicializar el nodo raíz, punto de partida del problema
        raiz = Node("", state=grid.initial, cost=0, parent=None, action=None)

        # llamamos a la cola de prioridad
        # se añade el nodo raíz a la frontera con prioridad 0
        frontera = PriorityQueueFrontier()
        frontera.add(raiz, raiz.cost)

        # creamos el diccioario donde se van a guardar los estados alcanzados
        # dict[Any, float]
        # colocamos el estado inicial con un costo 0
        alcanzados = {}
        alcanzados[raiz.state] = raiz.cost

        # mientras haya nodos que explorar 
        while not frontera.is_empty():
            #se va extrayendo de la frontera el nodo con menor costo
            n = frontera.pop()
            # comprobamos si es un estado obj
            if grid.objective_test(n.state):
                # si lo es entonces encontramos la solucion optima en costo
                return Solution(n, alcanzados)
        
            # sino expandimos el nodo actual
            # asumo que grid.acciones() retorna una lista de tuplas: (accion, estado_resultante, costo_individual)
            for accion in grid.actions(n.state):
                # calculamos el nuevo costo acumulado para llegar al estado vecino
                # Para cada acción, calcular el estado resultante y su costo
                s_prima = grid.result(n.state, accion)
                individual_cost = grid.individual_cost(n.state, accion)

                #Un nodo se descarta únicamente cuando su estado ya había sido alcanzado con un costo de camino menor o igual
                if s_prima not in alcanzados or individual_cost < alcanzados[s_prima]:
                    # creamos un nuevo nodo para este camino prometedor
                    n_prima = Node("", state=s_prima, cost=individual_cost, parent=n, action=accion)
                    # actualizamos el diccionario 'alcanzados' con el nuevo costo
                    alcanzados[s_prima] = individual_cost
                    # añadimos el nuevo nodo a la frontera para que sea considerado en futuras iteraciones
                    frontera.add(n_prima,individual_cost)
        
        # Si el bucle termina (se quedo vacio) sin encontrar el objetivo 
        # devolvemos que no hay solucion
        return NoSolution(alcanzados)
