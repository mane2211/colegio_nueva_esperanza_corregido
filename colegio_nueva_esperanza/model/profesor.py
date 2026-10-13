from model.empleado import Empleado
from model.excepciones import PeriodoCerradoException

class Profesor(Empleado):
    def __init__(self, rut: str, nombres: str, apellidos: str):
        super().__init__(rut, nombres, apellidos, cargo="Profesor")

    def ingresar_nota(self, evaluacion, nota: float):
        if evaluacion.periodo_academico.estado.lower() == "cerrado":
            raise PeriodoCerradoException("No se puede ingresar la nota porque el período académico está cerrado.")
        evaluacion.nota = nota

    def modificar_nota(self, evaluacion, nueva_nota: float):
        if evaluacion.periodo_academico.estado.lower() == "cerrado":
            raise PeriodoCerradoException("No se puede modificar la nota porque el período académico está cerrado.")
        evaluacion.nota = nueva_nota
