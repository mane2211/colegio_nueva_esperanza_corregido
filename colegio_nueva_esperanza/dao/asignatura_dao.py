from contextlib import closing
from dao.database import get_connection
from model.asignatura import Asignatura


class AsignaturaDAO:
    @staticmethod
    def obtener_por_codigo(codigo: str):
        with closing(get_connection()) as conn:
            row = conn.execute(
                "SELECT codigo, nombre, cupo, es_electivo FROM asignaturas WHERE codigo = ?",
                (codigo.strip().upper(),),
            ).fetchone()
        return Asignatura(row[0], row[1], row[2], bool(row[3])) if row else None

    @staticmethod
    def listar_todas():
        with closing(get_connection()) as conn:
            rows = conn.execute(
                "SELECT codigo, nombre, cupo, es_electivo FROM asignaturas ORDER BY codigo"
            ).fetchall()
        return [Asignatura(r[0], r[1], r[2], bool(r[3])) for r in rows]
