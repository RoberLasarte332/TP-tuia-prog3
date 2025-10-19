"""
Módulo de estrategias para el juego del Tateti

Este módulo contiene las estrategias para elegir la acción a realizar.
Los alumnos deben implementar la estrategia minimax.

Por defecto, se incluye una estrategia aleatoria como ejemplo base.
"""

import random
from typing import List, Tuple
from tateti import Tateti, JUGADOR_MAX, JUGADOR_MIN

def estrategia_aleatoria(tateti: Tateti, estado: List[List[str]]) -> Tuple[int, int]:
    """
    Estrategia aleatoria: elige una acción al azar entre las disponibles.
  
    Args:
        tateti: Instancia de la clase Tateti
        estado: Estado actual del tablero
        
    Returns:
        Tuple[int, int]: Acción elegida (fila, columna)

    Raises:
        ValueError: Si no hay acciones disponibles
    """
    acciones_disponibles = tateti.acciones(estado)
    if not acciones_disponibles:
        raise ValueError("No hay acciones disponibles")
    
    return random.choice(acciones_disponibles)


# --- Implementación del Algoritmo Minimax ---
#
# Basado en el pseudocódigo:
# function MINIMAX(problema, estado)
#   if problema.JUGADOR(estado) == MAX:
#     sucs ← {acción: MINIMAX-MIN(...) ...}
#     return max(sucs, key=sucs.get)
#   if problema.JUGADOR(estado) == MIN:
#     sucs ← {acción: MINIMAX-MAX(...) ...}
#     return min(sucs, key=sucs.get)
#
# (Se implementan MINIMAX-MAX y MINIMAX-MIN como funciones auxiliares)

def minimax_max(tateti: Tateti, estado: List[List[str]]) -> float:
    """
    Función de valor MAX (MINIMAX-MAX en el pseudocódigo).
    Calcula el máximo valor de utilidad que MAX puede obtener desde este estado.
    """
    # Caso base: Si el estado es terminal, devuelve su utilidad
    if tateti.test_terminal(estado):
        return tateti.utilidad(estado, JUGADOR_MAX) # Utilidad desde la perspectiva de MAX
    
    valor = -float('inf') # Inicializamos con el valor más bajo posible
    
    # Recorremos las acciones y llamamos a MIN
    for accion in tateti.acciones(estado):
        estado_siguiente = tateti.resultado(estado, accion)
        valor = max(valor, minimax_min(tateti, estado_siguiente))
    return valor

def minimax_min(tateti: Tateti, estado: List[List[str]]) -> float:
    """
    Función de valor MIN (MINIMAX-MIN en el pseudocódigo).
    Calcula el mínimo valor de utilidad que MIN puede forzar desde este estado.
    """
    # Caso base: Si el estado es terminal, devuelve su utilidad
    if tateti.test_terminal(estado):
        return tateti.utilidad(estado,JUGADOR_MAX) # Utilidad desde la perspectiva de MAX
    
    valor = float('inf') # Inicializamos con el valor más alto posible
    
    # Recorremos las acciones y llamamos a MAX
    for accion in tateti.acciones(estado):
        estado_siguiente = tateti.resultado(estado, accion)
        valor = min(valor, minimax_max(tateti, estado_siguiente))
    return valor


def estrategia_minimax(tateti: Tateti, estado: List[List[str]]) -> Tuple[int, int]:
    """
    Estrategia minimax: elige la mejor acción usando el algoritmo minimax.
    Esta es la función principal 'MINIMAX' del pseudocódigo.
    
    Args:
        tateti: Instancia de la clase Tateti (el 'problema')
        estado: Estado actual del tablero
        
    Returns:
        Tuple[int, int]: Acción elegida (fila, columna)
    """
    
    #Si el jugador actual es MAX
    if tateti.jugador(estado) == JUGADOR_MAX:
        #Para cada acción posible, calcula el valor que obtendría si MIN juega despues
        estado_siguiente = {accion: minimax_min(tateti, tateti.resultado(estado, accion)) for accion in tateti.acciones(estado)}
        #Devuelve la acción con el valor máximo (la mejor para MAX)
        return max(estado_siguiente, key = estado_siguiente.get)
    
    #Si el jugador actual es MIN
    if tateti.jugador(estado) == JUGADOR_MIN:
        #Para cada acción posible, calcula el valor que obtendría si MAX juega después
        estado_siguiente = {accion: minimax_max(tateti, tateti.resultado(estado, accion)) for accion in tateti.acciones(estado)}
        #Devuelve la acción con el valor mínimo (la mejor para MIN)
        return min(estado_siguiente, key = estado_siguiente.get)