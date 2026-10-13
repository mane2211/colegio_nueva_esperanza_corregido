class Arancel:
    def __init__(self, valor_uf: float):
        self.valor_uf = valor_uf

    def calcular_valor_pesos(self, valor_uf_dia: float) -> float:
        return round(self.valor_uf * valor_uf_dia, 2)
