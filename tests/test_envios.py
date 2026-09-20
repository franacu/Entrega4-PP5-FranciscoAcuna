import pytest
from solucion.envios import (
    RetiroSucursal, EnvioUrbano, EnvioInterior, EnvioExpress,
    Pedido, total_envios, SeguroEnvio, DescuentoEnvio,
    Seguro, Descuento, PedidoConModificadores,
)


def test_politicas():
    assert Pedido(1, 0, RetiroSucursal()).costo_envio() == 0
    assert Pedido(2, 8, EnvioUrbano()).costo_envio() == 1500
    assert Pedido(3, 100, EnvioInterior()).costo_envio() == 9500


def test_cambiar_politica():
    pedido = Pedido(2, 8, RetiroSucursal())
    pedido.cambiar_politica(EnvioUrbano())
    assert pedido.costo_envio() == 1500


def test_total_envios():
    pedidos = [Pedido(1, 0, RetiroSucursal()), Pedido(2, 8, EnvioUrbano())]
    assert total_envios(pedidos) == 1500


def test_validaciones_pedido():
    with pytest.raises(ValueError):
        Pedido(0, 5, EnvioUrbano())
    with pytest.raises(ValueError):
        Pedido(2, -1, EnvioUrbano())
    with pytest.raises(TypeError):
        Pedido(2, 8, "no es una politica")


def test_decoradores():
    base = EnvioUrbano()
    a = Pedido(2, 8, DescuentoEnvio(SeguroEnvio(base), 10))
    b = Pedido(2, 8, SeguroEnvio(DescuentoEnvio(base, 10)))
    assert a.costo_envio() == 1530
    assert b.costo_envio() == 1550
    assert base.costo(2, 8) == 1500
    assert Pedido(1, 0, SeguroEnvio(RetiroSucursal())).costo_envio() == 200


def test_descuento_porcentaje_invalido():
    with pytest.raises(ValueError):
        DescuentoEnvio(EnvioUrbano(), 150)


def test_express():
    express = SeguroEnvio(EnvioExpress())
    assert Pedido(2, 8, express).costo_envio() == 4000


def test_pipeline():
    pedido = PedidoConModificadores(2, 8, EnvioUrbano())
    pedido.agregar_modificador(Seguro())
    pedido.agregar_modificador(Descuento(10))
    assert pedido.costo_envio() == 1530

    pedido2 = PedidoConModificadores(2, 8, EnvioUrbano())
    pedido2.agregar_modificador(Descuento(10))
    pedido2.agregar_modificador(Seguro())
    assert pedido2.costo_envio() == 1550


def test_pipeline_rechaza_invalido():
    pedido = PedidoConModificadores(2, 8, EnvioUrbano())
    with pytest.raises(TypeError):
        pedido.agregar_modificador("no es un modificador")


def test_pipeline_coleccion_protegida():
    pedido = PedidoConModificadores(2, 8, EnvioUrbano())
    pedido.agregar_modificador(Seguro())
    copia = pedido.modificadores + (Descuento(50),)
    assert pedido.costo_envio() == 1700