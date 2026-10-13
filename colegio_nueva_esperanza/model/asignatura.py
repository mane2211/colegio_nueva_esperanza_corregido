class Asignatura:
    def __init__(self, codigo: str, nombre: str, cupo: int, es_electivo: bool):
        self.codigo = codigo
        self.nombre = nombre
        self.cupo = cupo
        self.es_electivo = es_electivo

    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El código de asignatura es obligatorio.")
        self.__codigo = valor.strip().upper()

    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre de la asignatura no puede estar vacío.")
        self.__nombre = valor.strip()

    @property
    def cupo(self) -> int:
        return self.__cupo

    @cupo.setter
    def cupo(self, valor: int):
        if not isinstance(valor, int) or valor < 0:
            raise ValueError("El cupo debe ser un número entero no negativo.")
        self.__cupo = valor

    @property
    def es_electivo(self) -> bool:
        return self.__es_electivo

    @es_electivo.setter
    def es_electivo(self, valor: bool):
        self.__es_electivo = bool(valor)

    def tiene_cupo(self) -> bool:
        return self.__cupo > 0
