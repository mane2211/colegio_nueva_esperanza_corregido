from model.persona import Persona

class Empleado(Persona):
    def __init__(self, rut: str, nombres: str, apellidos: str, cargo: str):
        super().__init__(rut, nombres, apellidos)
        self.cargo = cargo

    @property
    def cargo(self) -> str:
        return self.__cargo

    @cargo.setter
    def cargo(self, valor: str):
        if not valor or not isinstance(valor, str):
            raise ValueError("El cargo no puede estar vacío.")
        self.__cargo = valor.strip()
