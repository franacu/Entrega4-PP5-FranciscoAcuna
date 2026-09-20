from abc import ABC, abstractmethod

class RelacionLaboral(ABC):
    @abstractmethod
    def calcular_sueldo(self, registro_horas_deDia):
        """Cada tipo de relación implementa su propia forma de calcular."""

    @abstractmethod
    def resultado_precarizar(self, horas_minimas_diarias, costo_de_cada_hora):
        """Decide si cambia o no a Contratado."""

class Empleado:
    def __init__(self,nombre,dni,apellido,relacion_laboral) :
        self.nombre=nombre
        self.dni=dni
        self.apellido=apellido
        self._relacion_laboral = relacion_laboral
        self._registro_horas_deDia = []  

    def registrar_dia(self, horas):
        self._registro_horas_deDia.append(horas)

    def sueldo(self):
        return self._relacion_laboral.calcular_sueldo(self._registro_horas_deDia)

#  Sistema de Empleados:
    # efectivizar: de ser contratado a a ser empleado de planta - tipo de nivel
    # precarizar: empleado de planta pasa a ser contratado - tipo de nivel

    def efectivizar(self, nivel):
            self._relacion_laboral = Planta(nivel)

    def precarizar(self, horas_minimas_diarias, costo_de_cada_hora):
        self._relacion_laboral = self._relacion_laboral.resultado_precarizar(
            horas_minimas_diarias, costo_de_cada_hora)

    

class Contratado(RelacionLaboral):
    def __init__(self, horas_minimas_diarias, costo_de_cada_hora):
        if horas_minimas_diarias <= 0:
            raise ValueError("Las horas mínimas deben ser positivas")
        if costo_de_cada_hora <= 0:
            raise ValueError("El costo por hora debe ser positivo")
        self.horas_minimas_diarias = horas_minimas_diarias
        self.costo_de_cada_hora = costo_de_cada_hora

    def calcular_sueldo(self, registro_horas_deDia):
        contador_dias= 0
        for horas in registro_horas_deDia:
            if horas >= self.horas_minimas_diarias:
                contador_dias += 1
        return contador_dias * self.horas_minimas_diarias * self.costo_de_cada_hora

    def resultado_precarizar(self, horas_minimas_diarias, costo_de_cada_hora):
        return self
    
class Planta(RelacionLaboral):
    def __init__(self, nivel):
       
        if nivel <= 0 or nivel >= 4:
            raise ValueError("Niveles existentes del 1 al 3")
        self.nivel=nivel

# Suponiendo que:  nivel 1 = $160 la hora / nivel 2 = $100 la hora / nivel 3 = $50 la hora

    def calcular_sueldo(self, registro_horas_deDia):
        total_horas = 0

        for horas in registro_horas_deDia:
            total_horas += horas 

        minimo_mensual = 200
        tarifas = {1: 160, 2: 100, 3: 50}

        if  total_horas <= minimo_mensual:
            return total_horas * tarifas[self.nivel] 
        else:
            horas_extra = total_horas - minimo_mensual
            horas_sin_extra =total_horas - horas_extra
            return horas_extra * 2 * tarifas[self.nivel] + horas_sin_extra * tarifas[self.nivel]

    def resultado_precarizar(self, horas_minimas_diarias, costo_de_cada_hora):
        return Contratado(horas_minimas_diarias, costo_de_cada_hora)


def total_sueldos_a_pagar(empleados):
    total = 0
    for empleado in empleados:
        total += empleado.sueldo()
    return total


def mejor_sueldo(empleados):
    mejor = empleados[0].sueldo()
    for empleado in empleados:
        if empleado.sueldo() > mejor:
            mejor = empleado.sueldo()
    return mejor


def optimizar_sueldos(empleados, horas_minimas_diarias, costo_de_cada_hora):
    for empleado in empleados:
        empleado.precarizar(horas_minimas_diarias, costo_de_cada_hora)


if __name__ == "__main__":
    pepe = Empleado("Pepe", 33888999, "Argento", Contratado(6, 500))
    pepe.registrar_dia(6)
    pepe.registrar_dia(8)
    print("Sueldo como contratado:", pepe.sueldo())

    pepe.efectivizar(nivel=1)
    pepe.registrar_dia(60)
    print("Sueldo como planta:", pepe.sueldo())
    print("Datos conservados:", pepe.nombre, pepe.dni, pepe.apellido)

