import sys
from pathlib import Path

from solucion.empleados import (
    Contratado,
    Empleado,
    Planta,
    mejor_sueldo,
    optimizar_sueldos,
    total_sueldos_a_pagar,
)

def test_incorporar_empleado():
    e = Empleado("Pepe", 33888999, "Argento", Contratado(6, 500))
    assert e.nombre == "Pepe"


def test_sueldo_contratado():
    e = Empleado("Ana", 1, "Lopez", Contratado(6, 500))
    e.registrar_dia(6)
    e.registrar_dia(3)
    assert e.sueldo() == 6 * 500


def test_sueldo_planta_sin_extra():
    e = Empleado("Juan", 2, "Diaz", Planta(nivel=1))
    e.registrar_dia(100)
    e.registrar_dia(100)
    assert e.sueldo() == 200 * 160


def test_sueldo_planta_con_extra():
    e = Empleado("Juan", 2, "Diaz", Planta(nivel=1))
    e.registrar_dia(150)
    e.registrar_dia(150)
    assert e.sueldo() == 200 * 160 + 100 * 160 * 2


def test_total_sueldos_a_pagar():
    e1 = Empleado("A", 1, "B", Contratado(6, 500))
    e1.registrar_dia(6)
    e2 = Empleado("C", 2, "D", Planta(nivel=1))
    e2.registrar_dia(100)
    assert total_sueldos_a_pagar([e1, e2]) == 3000 + 16000


def test_mejor_sueldo():
    e1 = Empleado("A", 1, "B", Planta(nivel=1))
    e1.registrar_dia(100)
    e2 = Empleado("C", 2, "D", Planta(nivel=3))
    e2.registrar_dia(100)
    assert mejor_sueldo([e1, e2]) == 100 * 160


def test_efectivizar_conserva_datos_y_horas():
    e = Empleado("Pepe", 33888999, "Argento", Contratado(6, 500))
    e.registrar_dia(8)
    e.efectivizar(nivel=1)
    assert e.nombre == "Pepe"
    assert e._registro_horas_deDia == [8]


def test_precarizar_solo_afecta_a_los_de_planta():
    contratado_original = Contratado(4, 800)
    e1 = Empleado("A", 1, "B", contratado_original)
    e2 = Empleado("C", 2, "D", Planta(nivel=1))

    optimizar_sueldos([e1, e2], 8, 600)

    assert e1._relacion_laboral is contratado_original   # no cambió
    e2.registrar_dia(8)
    assert e2.sueldo() == 8 * 600   # ahora sí es Contratado con el contrato nuevo