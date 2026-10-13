from datetime import date
from model.detalle_matricula import DetalleMatricula
from model.excepciones import CupoElectivoException

class Matricula:
    def __init__(self, folio: int, fecha_matricula: date):
        self.folio = folio
        self.fecha_matricula = fecha_matricula
        self.__detalles = []

    @property
    def detalles(self):
        return self.__detalles

    def agregar_detalle(self, asignatura, arancel, indicador_uf):
        if asignatura.es_electivo and not asignatura.tiene_cupo():
            raise CupoElectivoException(f"El electivo {asignatura.nombre} no tiene cupos disponibles.")
        detalle = DetalleMatricula(asignatura, arancel, indicador_uf)
        self.__detalles.append(detalle)
        return detalle

    def calcular_monto_total(self) -> float:
        return sum(d.calcular_subtotal() for d in self.__detalles)
