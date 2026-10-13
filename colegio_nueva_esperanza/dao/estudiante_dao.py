import sqlite3
from contextlib import closing
from dao.database import get_connection
from model.estudiante import Estudiante
from model.persona import Persona


class EstudianteDAO:
    @staticmethod
    def crear(estudiante: Estudiante) -> bool:
        try:
            with closing(get_connection()) as conn, conn:
                conn.execute(
                    "INSERT INTO estudiantes (rut, nombres, apellidos, deuda_matricula_pendiente, curso, apoderado) VALUES (?, ?, ?, ?, ?, ?)",
                    (estudiante.rut, estudiante.nombres, estudiante.apellidos,
                     int(estudiante.deuda_matricula_pendiente), estudiante.curso, estudiante.apoderado),
                )
            return True
        except sqlite3.IntegrityError:
            return False

    @staticmethod
    def obtener_por_rut(rut: str):
        if not Persona.validar_rut(rut):
            raise ValueError(f"RUT inválido: '{rut}'")
        rut = Persona.normalizar_rut(rut)
        with closing(get_connection()) as conn, conn:
            row = conn.execute(
                "SELECT rut, nombres, apellidos, deuda_matricula_pendiente, curso, apoderado FROM estudiantes "
                "WHERE REPLACE(REPLACE(UPPER(rut), '.', ''), '-', '') = ?",
                (rut.replace("-", ""),),
            ).fetchone()
        return Estudiante(*row[:3], deuda_matricula_pendiente=bool(row[3]), curso=row[4], apoderado=row[5]) if row else None

    @staticmethod
    def listar_todos():
        with closing(get_connection()) as conn, conn:
            rows = conn.execute(
                "SELECT rut, nombres, apellidos, deuda_matricula_pendiente, curso, apoderado FROM estudiantes ORDER BY apellidos, nombres"
            ).fetchall()
        return [Estudiante(*row[:3], deuda_matricula_pendiente=bool(row[3]), curso=row[4], apoderado=row[5]) for row in rows]

    @staticmethod
    def actualizar(estudiante: Estudiante) -> bool:
        with closing(get_connection()) as conn, conn:
            cursor = conn.execute(
                "UPDATE estudiantes SET nombres=?, apellidos=?, deuda_matricula_pendiente=?, curso=?, apoderado=? "
                "WHERE REPLACE(REPLACE(UPPER(rut), '.', ''), '-', '') = ?",
                (estudiante.nombres, estudiante.apellidos, int(estudiante.deuda_matricula_pendiente),
                 estudiante.curso, estudiante.apoderado, estudiante.rut.replace("-", "")),
            )
            return cursor.rowcount > 0

    @staticmethod
    def eliminar(rut: str) -> bool:
        if not Persona.validar_rut(rut):
            raise ValueError(f"RUT inválido: '{rut}'")
        try:
            with closing(get_connection()) as conn, conn:
                cursor = conn.execute(
                    "DELETE FROM estudiantes WHERE REPLACE(REPLACE(UPPER(rut), '.', ''), '-', '') = ?",
                    (Persona.normalizar_rut(rut).replace("-", ""),),
                )
                return cursor.rowcount > 0
        except sqlite3.IntegrityError as exc:
            raise ValueError("No se puede eliminar: el estudiante tiene matrículas asociadas.") from exc
