from model.evaluacion import Evaluacion

class Prueba(Evaluacion):
    PONDERACION = 0.40

    def calcular_aporte(self) -> float:
        return self.nota * self.PONDERACION
