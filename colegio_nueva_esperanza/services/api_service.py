import requests
from datetime import date
from model.indicador_uf import IndicadorUF


class APIService:
    URL = "https://mindicador.cl/api/uf"
    VALOR_RESPALDO = 39000.0

    @staticmethod
    def obtener_indicador_uf(timeout_seconds: int = 5) -> IndicadorUF:
        try:
            response = requests.get(APIService.URL, timeout=timeout_seconds)
            response.raise_for_status()
            serie = response.json().get("serie", [])
            if not serie or "valor" not in serie[0]:
                raise ValueError("La respuesta no contiene el valor de la UF.")
            return IndicadorUF(date.today(), float(serie[0]["valor"]), es_respaldo=False)
        except (requests.RequestException, ValueError, TypeError, KeyError) as exc:
            print(f"[API] No se pudo obtener la UF ({exc}). Se utilizará el respaldo local de ${APIService.VALOR_RESPALDO:,.0f}.")
            return IndicadorUF(date.today(), APIService.VALOR_RESPALDO, es_respaldo=True)
