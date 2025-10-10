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
        raiz = Node("", estado=grid.inicial, costo=0, padre=None, accion=None)

        # llamamos a la cola de prioridad
        # se añade el nodo raíz a la frontera con prioridad 0
        frontera = PriorityQueueFrontier()
        frontera.add(raiz, raiz.costo)

        # creamos el diccioario donde se van a guardar los estados alcanzados
        # dict[Any, float]
        # colocamos el estado inicial con un costo 0
        alcanzados = {}
        alcanzados[raiz.estado] = raiz.costo

        # mientras haya nodos que explorar 
        while len(frontera.frontier) > 0:
            #se va extrayendo de la frontera el nodo con menor costo
            n = frontera.pop()
            # comprobamos si es un estado obj
            if grid.test_obj(n.estado):
                # si lo es entonces encontramos la solucion optima en costo
                return Solution(n, alcanzados)
        
            # sino expandimos el nodo actual
            # asumo que grid.acciones() retorna una lista de tuplas: (accion, estado_resultante, costo_individual)
            for accion, s_prima, cost_ind in grid.acciones(n.estado):
                # calculamos el nuevo costo acumulado para llegar al estado vecino
                c_prima = n.costo + cost_ind

                #Un nodo se descarta únicamente cuando su estado ya había sido alcanzado con un costo de camino menor o igual
                if s_prima not in alcanzados or c_prima < alcanzados[s_prima]:
                    # creamos un nuevo nodo para este camino prometedor
                    n_prima = Node("", estado=s_prima, costo=c_prima, padre=n, accion=accion)
                    # actualizamos el diccionario 'alcanzados' con el nuevo costo
                    alcanzados[s_prima] = c_prima
                    # añadimos el nuevo nodo a la frontera para que sea considerado en futuras iteraciones
                    frontera.add(n_prima,c_prima)
        
        # Si el bucle termina (se quedo vacio) sin encontrar el objetivo 
        # devolvemos que no hay solucion
        return NoSolution(alcanzados)
