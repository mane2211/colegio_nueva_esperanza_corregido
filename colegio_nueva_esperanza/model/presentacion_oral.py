from model.evaluacion import Evaluacion

class PresentacionOral(Evaluacion):
    PONDERACION = 0.25

    def calcular_aporte(self) -> float:
        return self.nota * self.PONDERACION
