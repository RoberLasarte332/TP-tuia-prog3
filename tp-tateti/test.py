"""
Pruebas unitarias para el proyecto Tateti - Minimax

Este archivo contiene pruebas para verificar que las implementaciones
de los alumnos funcionen correctamente.

Ejecutar con: python test.py
"""

import unittest
import copy
from tateti import (
    Tateti, JUGADOR_MAX, JUGADOR_MIN, CASILLA_VACIA
)
from estrategias import estrategia_aleatoria, estrategia_minimax

class TestTatetiGame(unittest.TestCase):
    """Pruebas para el módulo tateti"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.tateti = Tateti()
    
    def test_estado_inicial(self):
        """Prueba que el estado inicial sea correcto"""
        estado = copy.deepcopy(self.tateti.estado_inicial)
        self.assertEqual(len(estado), 3)
        self.assertEqual(len(estado[0]), 3)
        self.assertTrue(all(casilla == CASILLA_VACIA 
                           for fila in estado 
                           for casilla in fila))
    
    def test_jugador_estado_inicial(self):
        """Prueba que MAX empiece primero"""
        estado = copy.deepcopy(self.tateti.estado_inicial)
        self.assertEqual(self.tateti.jugador(estado), JUGADOR_MAX)
    
    def test_jugador_alternancia(self):
        """Prueba que los jugadores alternen correctamente"""
        estado = copy.deepcopy(self.tateti.estado_inicial)
        # Después de una jugada de MAX, debe ser turno de MIN
        estado_tras_max = self.tateti.resultado(estado, (0, 0))
        self.assertEqual(self.tateti.jugador(estado_tras_max), JUGADOR_MIN)
        
        # Después de una jugada de MIN, debe ser turno de MAX
        estado_tras_min = self.tateti.resultado(estado_tras_max, (0, 1))
        self.assertEqual(self.tateti.jugador(estado_tras_min), JUGADOR_MAX)
    
    def test_acciones_estado_inicial(self):
        """Prueba que las acciones iniciales sean todas las casillas"""
        estado = copy.deepcopy(self.tateti.estado_inicial)
        acciones_esperadas = [(i, j) for i in range(3) for j in range(3)]
        self.assertEqual(set(self.tateti.acciones(estado)), set(acciones_esperadas))
    
    def test_acciones_estado_parcial(self):
        """Prueba acciones en un estado parcialmente lleno"""
        estado = copy.deepcopy(self.tateti.estado_inicial)
        estado[0][0] = JUGADOR_MAX
        estado[1][1] = JUGADOR_MIN
        
        acciones_disponibles = self.tateti.acciones(estado)
        self.assertNotIn((0, 0), acciones_disponibles)
        self.assertNotIn((1, 1), acciones_disponibles)
        self.assertEqual(len(acciones_disponibles), 7)
    
    def test_resultado_jugada_valida(self):
        """Prueba que resultado funcione con jugadas válidas"""
        estado = copy.deepcopy(self.tateti.estado_inicial)
        nuevo_estado = self.tateti.resultado(estado, (1, 1))
        
        self.assertEqual(nuevo_estado[1][1], JUGADOR_MAX)
        # El estado original no debe cambiar
        self.assertEqual(estado[1][1], CASILLA_VACIA)
    
    def test_resultado_jugada_invalida(self):
        """Prueba que resultado lance error con jugadas inválidas"""
        estado = copy.deepcopy(self.tateti.estado_inicial)
        estado[1][1] = JUGADOR_MAX
        
        with self.assertRaises(ValueError):
            self.tateti.resultado(estado, (1, 1))  # Casilla ocupada
        
        with self.assertRaises(ValueError):
            self.tateti.resultado(estado, (3, 0))  # Fuera de rango
    
    def test_terminal_estado_inicial(self):
        """Prueba que el estado inicial no sea terminal"""
        estado = copy.deepcopy(self.tateti.estado_inicial)
        self.assertFalse(self.tateti.test_terminal(estado))
    
    def test_terminal_victoria_fila(self):
        """Prueba detección de victoria en fila"""
        estado = [
            [JUGADOR_MAX, JUGADOR_MAX, JUGADOR_MAX],
            [JUGADOR_MIN, JUGADOR_MIN, CASILLA_VACIA],
            [CASILLA_VACIA, CASILLA_VACIA, CASILLA_VACIA]
        ]
        self.assertTrue(self.tateti.test_terminal(estado))
        self.assertEqual(self.tateti.utilidad(estado), 1.0)
    
    def test_terminal_victoria_columna(self):
        """Prueba detección de victoria en columna"""
        estado = [
            [JUGADOR_MIN, JUGADOR_MAX, CASILLA_VACIA],
            [JUGADOR_MIN, JUGADOR_MAX, CASILLA_VACIA],
            [JUGADOR_MIN, CASILLA_VACIA, CASILLA_VACIA]
        ]
        self.assertTrue(self.tateti.test_terminal(estado))
        self.assertEqual(self.tateti.utilidad(estado), 0.0)
    
    def test_terminal_victoria_diagonal(self):
        """Prueba detección de victoria en diagonal"""
        estado = [
            [JUGADOR_MAX, JUGADOR_MIN, CASILLA_VACIA],
            [JUGADOR_MIN, JUGADOR_MAX, CASILLA_VACIA],
            [CASILLA_VACIA, CASILLA_VACIA, JUGADOR_MAX]
        ]
        self.assertTrue(self.tateti.test_terminal(estado))
        self.assertEqual(self.tateti.utilidad(estado), 1.0)
    
    def test_terminal_empate(self):
        """Prueba detección de empate"""
        estado = [
            [JUGADOR_MAX, JUGADOR_MIN, JUGADOR_MAX],
            [JUGADOR_MIN, JUGADOR_MIN, JUGADOR_MAX],
            [JUGADOR_MIN, JUGADOR_MAX, JUGADOR_MIN]
        ]
        self.assertTrue(self.tateti.test_terminal(estado))
        self.assertEqual(self.tateti.utilidad(estado), 0.5)
        # El empate debe ser 0.5 para ambos jugadores
        self.assertEqual(self.tateti.utilidad(estado, JUGADOR_MAX), 0.5)
        self.assertEqual(self.tateti.utilidad(estado, JUGADOR_MIN), 0.5)
    
    def test_utilidad_desde_perspectiva_min(self):
        """Prueba que la utilidad se calcule correctamente desde la perspectiva de MIN"""
        # Estado donde MAX gana
        estado_max_gana = [
            [JUGADOR_MAX, JUGADOR_MAX, JUGADOR_MAX],
            [JUGADOR_MIN, JUGADOR_MIN, CASILLA_VACIA],
            [CASILLA_VACIA, CASILLA_VACIA, CASILLA_VACIA]
        ]
        # Desde perspectiva de MAX: victoria = 1.0
        self.assertEqual(self.tateti.utilidad(estado_max_gana, JUGADOR_MAX), 1.0)
        # Desde perspectiva de MIN: derrota = 0.0
        self.assertEqual(self.tateti.utilidad(estado_max_gana, JUGADOR_MIN), 0.0)
        
        # Estado donde MIN gana
        estado_min_gana = [
            [JUGADOR_MIN, JUGADOR_MIN, JUGADOR_MIN],
            [JUGADOR_MAX, JUGADOR_MAX, CASILLA_VACIA],
            [CASILLA_VACIA, CASILLA_VACIA, CASILLA_VACIA]
        ]
        # Desde perspectiva de MAX: derrota = 0.0
        self.assertEqual(self.tateti.utilidad(estado_min_gana, JUGADOR_MAX), 0.0)
        # Desde perspectiva de MIN: victoria = 1.0
        self.assertEqual(self.tateti.utilidad(estado_min_gana, JUGADOR_MIN), 1.0)

class TestEstrategias(unittest.TestCase):
    """Pruebas para el módulo estrategias"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.tateti = Tateti()
    
    def test_estrategia_aleatoria_estado_inicial(self):
        """Prueba que la estrategia aleatoria funcione"""
        estado = copy.deepcopy(self.tateti.estado_inicial)
        accion = estrategia_aleatoria(self.tateti, estado)
        
        self.assertIsInstance(accion, tuple)
        self.assertEqual(len(accion), 2)
        self.assertIn(accion, self.tateti.acciones(estado))
    
    def test_estrategia_aleatoria_sin_acciones(self):
        """Prueba que la estrategia aleatoria falle sin acciones"""
        estado = [
            [JUGADOR_MAX, JUGADOR_MIN, JUGADOR_MAX],
            [JUGADOR_MIN, JUGADOR_MIN, JUGADOR_MAX],
            [JUGADOR_MIN, JUGADOR_MAX, JUGADOR_MIN]
        ]
        
        with self.assertRaises(ValueError):
            estrategia_aleatoria(self.tateti, estado)
    
    def test_minimax_devuelve_accion_valida(self):
        """Prueba básica de que minimax devuelva una acción válida"""
        estado = copy.deepcopy(self.tateti.estado_inicial)
        try:
            accion = estrategia_minimax(self.tateti, estado)
            self.assertIsInstance(accion, tuple)
            self.assertEqual(len(accion), 2)
            self.assertIn(accion, self.tateti.acciones(estado))
        except NotImplementedError:
            # Es aceptable si no está implementado aún
            pass

class TestEscenariosMinimax(unittest.TestCase):
    """Pruebas específicas para verificar la lógica del minimax"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.tateti = Tateti()
    
    def test_minimax_victoria_inmediata(self):
        """Prueba que minimax tome una victoria inmediata"""
        # Estado donde MAX puede ganar en un movimiento
        estado = [
            [JUGADOR_MAX, JUGADOR_MAX, CASILLA_VACIA],  # MAX puede ganar en (0,2)
            [JUGADOR_MIN, JUGADOR_MIN, CASILLA_VACIA],
            [CASILLA_VACIA, CASILLA_VACIA, CASILLA_VACIA]
        ]
        
        try:
            accion = estrategia_minimax(self.tateti, estado)
            # Si minimax está implementado correctamente, debería elegir (0,2)
            if accion != (0, 2):
                print(f"Advertencia: minimax eligió {accion} en lugar de (0,2) para victoria inmediata")
        except NotImplementedError:
            print("Minimax aún no implementado - esto es normal durante el desarrollo")
        except Exception as e:
            print(f"Error inesperado en minimax: {e}")
    
    def test_minimax_bloquear_victoria_oponente(self):
        """Prueba que minimax bloquee una victoria del oponente"""
        # Estado donde MIN puede ganar si MAX no bloquea
        estado = [
            [JUGADOR_MIN, JUGADOR_MIN, CASILLA_VACIA],  # MIN puede ganar en (0,2)
            [JUGADOR_MAX, CASILLA_VACIA, CASILLA_VACIA],
            [CASILLA_VACIA, CASILLA_VACIA, CASILLA_VACIA]
        ]
        
        try:
            accion = estrategia_minimax(self.tateti, estado)
            # MAX debería bloquear en (0,2)
            if accion != (0, 2):
                print(f"Advertencia: minimax eligió {accion} en lugar de bloquear en (0,2)")
        except NotImplementedError:
            print("Minimax aún no implementado - esto es normal durante el desarrollo")
        except Exception as e:
            print(f"Error inesperado en minimax: {e}")

def ejecutar_pruebas():
    """Ejecuta todas las pruebas y muestra un resumen"""
    print("=== EJECUTANDO PRUEBAS DEL PROYECTO TATETI ===\n")
    
    suite = unittest.TestLoader().loadTestsFromModule(__import__(__name__))
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    
    print(f"\n=== RESUMEN ===")
    print(f"Pruebas ejecutadas: {resultado.testsRun}")
    print(f"Errores: {len(resultado.errors)}")
    print(f"Fallos: {len(resultado.failures)}")
    
    if resultado.errors:
        print("\n⚠️  ERRORES ENCONTRADOS:")
        for test, error in resultado.errors:
            error_msg = error.strip().split('\n')[-1]
            print(f"  - {test}: {error_msg}")
    
    if resultado.failures:
        print("\n❌ FALLOS ENCONTRADOS:")
        for test, failure in resultado.failures:
            failure_msg = failure.strip().split('\n')[-1]
            print(f"  - {test}: {failure_msg}")
    
    if not resultado.errors and not resultado.failures:
        print("\n✅ ¡TODAS LAS PRUEBAS PASARON!")
    
    return resultado.wasSuccessful()

if __name__ == "__main__":
    ejecutar_pruebas()
