from enum import Enum


class CompraStatus(Enum):
    CRIANDO = 1
    PAGO = 2
    CANCELADO = 3
    CONCLUIDO = 4
    EM_PREPARO = 5
    PRONTO_PARA_ENTREGA = 6
    ENTREGUE = 7
    FINALIZADO = 8
