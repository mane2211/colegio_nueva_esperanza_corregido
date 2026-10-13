from model.evaluacion import Evaluacion

class Trabajo(Evaluacion):
    PONDERACION = 0.35

    def calcular_aporte(self) -> float:
        return self.nota * self.PONDERACION
