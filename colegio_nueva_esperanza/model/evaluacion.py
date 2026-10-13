from datetime import date
from abc import ABC, abstractmethod

class Evaluacion(ABC):
    def __init__(self, fecha: date, nota: float, observacion: str, asignatura, profesor, periodo_academico):
        self.fecha = fecha
        self.nota = nota
        self.observacion = observacion
        self.asignatura = asignatura
        self.profesor = profesor
        self.periodo_academico = periodo_academico

    @property
    def nota(self) -> float:
        return self.__nota

    @nota.setter
    def nota(self, valor: float):
        try:
            val_float = float(valor)
        except (ValueError, TypeError):
            raise ValueError("La nota debe ser un número numérico válido entre 1.0 y 7.0.")
        if not (1.0 <= val_float <= 7.0):
            raise ValueError("La nota debe estar entre 1.0 y 7.0.")
        self.__nota = round(val_float, 2)

    @abstractmethod
    def calcular_aporte(self) -> float:
        pass
