from abc import ABC, abstractmethod


class PoliticaEnvio(ABC):
    @abstractmethod
    def costo(self, peso_kg, distancia_km) -> float:
        """Devuelve el costo de envío."""


class RetiroSucursal(PoliticaEnvio):
    def costo(self, peso_kg, distancia_km):
        return 0


class EnvioUrbano(PoliticaEnvio):
    def costo(self, peso_kg, distancia_km):
        return 1500


class EnvioInterior(PoliticaEnvio):
    def costo(self, peso_kg, distancia_km):
        return 1500 + 80 * distancia_km


class EnvioExpress(PoliticaEnvio):
    def costo(self, peso_kg, distancia_km):
        return 3000 + 100 * distancia_km


class Pedido:
    def __init__(self, peso_kg, distancia_km, politica_envio):
        if peso_kg <= 0:
            raise ValueError("El peso debe ser mayor que cero")
        if distancia_km < 0:
            raise ValueError("La distancia no puede ser negativa")
        if not isinstance(politica_envio, PoliticaEnvio):
            raise TypeError("La política no cumple el contrato")

        self._peso_kg = peso_kg
        self._distancia_km = distancia_km
        self._politica = politica_envio

    @property
    def peso_kg(self):
        return self._peso_kg

    @property
    def distancia_km(self):
        return self._distancia_km

    def cambiar_politica(self, politica_envio):
        if not isinstance(politica_envio, PoliticaEnvio):
            raise TypeError("La política no cumple el contrato")
        self._politica = politica_envio

    def costo_envio(self):
        return self._politica.costo(self._peso_kg, self._distancia_km)


def total_envios(pedidos):
    total = 0
    for pedido in pedidos:
        total += pedido.costo_envio()
    return total


class DecoradorEnvio(PoliticaEnvio):
    def __init__(self, politica_envio):
        if not isinstance(politica_envio, PoliticaEnvio):
            raise TypeError("La política no cumple el contrato")
        self._politica = politica_envio

    def costo(self, peso_kg, distancia_km):
        return self._politica.costo(peso_kg, distancia_km)

class SeguroEnvio(DecoradorEnvio):
    def costo(self, peso_kg, distancia_km):
        return self._politica.costo(peso_kg, distancia_km) + 200


class DescuentoEnvio(DecoradorEnvio):
    def __init__(self, politica_envio, porcentaje):
        super().__init__(politica_envio)
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        self._porcentaje = porcentaje

    def costo(self, peso_kg, distancia_km):
        costo_base = self._politica.costo(peso_kg, distancia_km)
        return round(costo_base * (1 - self._porcentaje / 100), 2)


class ModificadorCosto(ABC):
    @abstractmethod
    def aplicar(self, costo):
        """Devuelve el nuevo costo."""


class Seguro(ModificadorCosto):
    def aplicar(self, costo):
        return costo + 200


class Descuento(ModificadorCosto):
    def __init__(self, porcentaje):
        if porcentaje < 0 or porcentaje > 100:
            raise ValueError("El porcentaje debe estar entre 0 y 100")
        self._porcentaje = porcentaje

    def aplicar(self, costo):
        return round(costo * (1 - self._porcentaje / 100), 2)


class PedidoConModificadores:
    def __init__(self, peso_kg, distancia_km, politica_envio):
        if peso_kg <= 0:
            raise ValueError("El peso debe ser mayor que cero")
        if distancia_km < 0:
            raise ValueError("La distancia no puede ser negativa")
        if not isinstance(politica_envio, PoliticaEnvio):
            raise TypeError("La política no cumple el contrato")

        self._peso_kg = peso_kg
        self._distancia_km = distancia_km
        self._politica = politica_envio
        self._modificadores = []

    def agregar_modificador(self, modificador):
        if not isinstance(modificador, ModificadorCosto):
            raise TypeError("El modificador no cumple el contrato")
        self._modificadores.append(modificador)

    @property
    def modificadores(self):
        return tuple(self._modificadores)

    def costo_envio(self):
        costo = self._politica.costo(self._peso_kg, self._distancia_km)
        for modificador in self._modificadores:
            costo = modificador.aplicar(costo)
        return costo


    