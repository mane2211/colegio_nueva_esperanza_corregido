from model.persona import Persona
from model.excepciones import DeudaMatriculaException


class Estudiante(Persona):
    def __init__(self, rut: str, nombres: str, apellidos: str,
                 deuda_matricula_pendiente: bool = False,
                 curso: str = "Sin asignar", apoderado: str = "Sin asignar"):
        super().__init__(rut, nombres, apellidos)
        self.deuda_matricula_pendiente = deuda_matricula_pendiente
        self.curso = curso
        self.apoderado = apoderado
        self.matriculas = []

    @property
    def curso(self):
        return self.__curso

    @curso.setter
    def curso(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El curso no puede estar vacío.")
        self.__curso = valor.strip()

    @property
    def apoderado(self):
        return self.__apoderado

    @apoderado.setter
    def apoderado(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El apoderado no puede estar vacío.")
        self.__apoderado = valor.strip()

    @property
    def deuda_matricula_pendiente(self) -> bool:
        return self.__deuda_matricula_pendiente

    @deuda_matricula_pendiente.setter
    def deuda_matricula_pendiente(self, valor: bool):
        self.__deuda_matricula_pendiente = bool(valor)

    def tiene_deuda_pendiente(self) -> bool:
        return self.__deuda_matricula_pendiente

    def solicitar_matricula(self, matricula):
        if self.__deuda_matricula_pendiente:
            raise DeudaMatriculaException("El estudiante mantiene una deuda de matrícula pendiente.")
        self.matriculas.append(matricula)
        return True
