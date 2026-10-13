from datetime import date


class IndicadorUF:
    def __init__(self, fecha: date, valor: float, es_respaldo: bool = False):
        self.fecha = fecha
        self.valor = float(valor)
        self.es_respaldo = es_respaldo

    def obtener_valor(self) -> float:
        return self.valor
