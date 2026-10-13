class DetalleMatricula:
    def __init__(self, asignatura, arancel, indicador_uf):
        self.asignatura = asignatura
        self.arancel = arancel
        self.indicador_uf = indicador_uf
        self.valor_uf_aplicado = indicador_uf.obtener_valor()

    def calcular_subtotal(self) -> float:
        return self.arancel.calcular_valor_pesos(self.valor_uf_aplicado)
