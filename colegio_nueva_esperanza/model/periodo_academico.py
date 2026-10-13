from datetime import date

class PeriodoAcademico:
    def __init__(self, anio: int, semestre: int, estado: str, fecha_cierre: date):
        self.anio = anio
        self.semestre = semestre
        self.estado = estado
        self.fecha_cierre = fecha_cierre

    @property
    def estado(self) -> str:
        return self.__estado

    @estado.setter
    def estado(self, valor: str):
        if valor.lower() not in ["abierto", "cerrado"]:
            raise ValueError("El estado del periodo debe ser 'abierto' o 'cerrado'.")
        self.__estado = valor.lower()

    def esta_abierto(self) -> bool:
        return self.__estado == "abierto"
