import re


class Persona:
    def __init__(self, rut: str, nombres: str, apellidos: str):
        self.rut = rut
        self.nombres = nombres
        self.apellidos = apellidos

    @property
    def rut(self) -> str:
        return self.__rut

    @rut.setter
    def rut(self, valor: str):
        if not self.validar_rut(valor):
            raise ValueError(f"RUT inválido: '{valor}'")
        self.__rut = self.normalizar_rut(valor)

    @property
    def nombres(self) -> str:
        return self.__nombres

    @nombres.setter
    def nombres(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres.")
        self.__nombres = valor.strip()

    @property
    def apellidos(self) -> str:
        return self.__apellidos

    @apellidos.setter
    def apellidos(self, valor: str):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ValueError("El apellido debe tener al menos 2 caracteres.")
        self.__apellidos = valor.strip()

    @staticmethod
    def normalizar_rut(rut: str) -> str:
        return rut.replace(".", "").replace("-", "").strip().upper()[:-1] + "-" + rut.replace(".", "").replace("-", "").strip().upper()[-1:]

    @staticmethod
    def validar_rut(rut: str) -> bool:
        if not isinstance(rut, str):
            return False
        rut_limpio = rut.replace(".", "").replace("-", "").strip().upper()
        if len(rut_limpio) < 8 or len(rut_limpio) > 9:
            return False
        cuerpo, dv = rut_limpio[:-1], rut_limpio[-1]
        if not cuerpo.isdigit() or not (dv.isdigit() or dv == "K"):
            return False
        suma, multiplicador = 0, 2
        for digito in reversed(cuerpo):
            suma += int(digito) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1
        resto = 11 - (suma % 11)
        esperado = "0" if resto == 11 else "K" if resto == 10 else str(resto)
        return dv == esperado
