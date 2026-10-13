import sqlite3
from contextlib import closing
from dao.database import get_connection
from model.excepciones import CupoElectivoException, DeudaMatriculaException
from model.persona import Persona


class MatriculaDAO:
    @staticmethod
    def guardar_transaccion(matricula, rut_estudiante: str) -> bool:
        if not Persona.validar_rut(rut_estudiante):
            raise ValueError(f"RUT inválido: '{rut_estudiante}'")
        rut_estudiante = Persona.normalizar_rut(rut_estudiante)
        if not matricula.detalles:
            raise ValueError("La matrícula debe incluir al menos una asignatura.")
        codigos = [d.asignatura.codigo for d in matricula.detalles]
        if len(codigos) != len(set(codigos)):
            raise ValueError("No se puede inscribir dos veces la misma asignatura en una matrícula.")

        conn = get_connection()
        try:
            cursor = conn.cursor()
            estudiante = cursor.execute(
                "SELECT rut, deuda_matricula_pendiente FROM estudiantes "
                "WHERE REPLACE(REPLACE(UPPER(rut), '.', ''), '-', '') = ?",
                (rut_estudiante.replace("-", ""),)
            ).fetchone()
            if not estudiante:
                raise ValueError("El estudiante no existe en la base de datos.")
            if estudiante[1]:
                raise DeudaMatriculaException("La matrícula se impidió: el estudiante tiene deuda pendiente.")

            rut_estudiante = estudiante[0]  # Conserva la clave original de bases anteriores.

            for detalle in matricula.detalles:
                asignatura = cursor.execute(
                    "SELECT es_electivo FROM asignaturas WHERE codigo = ?", (detalle.asignatura.codigo,)
                ).fetchone()
                if not asignatura:
                    raise ValueError(f"La asignatura {detalle.asignatura.codigo} no está registrada.")
                if asignatura[0]:
                    cursor.execute(
                        "UPDATE asignaturas SET cupo = cupo - 1 WHERE codigo = ? AND es_electivo = 1 AND cupo > 0",
                        (detalle.asignatura.codigo,),
                    )
                    if cursor.rowcount != 1:
                        raise CupoElectivoException(
                            f"La inscripción se impidió: el electivo {detalle.asignatura.nombre} no tiene cupos disponibles."
                        )

            cursor.execute(
                "INSERT INTO matriculas (folio, fecha_matricula, rut_estudiante, monto_total) VALUES (?, ?, ?, ?)",
                (matricula.folio, str(matricula.fecha_matricula), rut_estudiante, matricula.calcular_monto_total()),
            )
            cursor.executemany(
                "INSERT INTO detalles_matricula (folio_matricula, codigo_asignatura, valor_uf_aplicado, subtotal) VALUES (?, ?, ?, ?)",
                [(matricula.folio, d.asignatura.codigo, d.valor_uf_aplicado, d.calcular_subtotal()) for d in matricula.detalles],
            )
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    @staticmethod
    def listar_todas():
        with closing(get_connection()) as conn:
            return conn.execute(
                "SELECT folio, fecha_matricula, rut_estudiante, monto_total FROM matriculas ORDER BY folio"
            ).fetchall()

    @staticmethod
    def listar_detalles(folio: int):
        with closing(get_connection()) as conn:
            return conn.execute(
                "SELECT d.codigo_asignatura, a.nombre, d.valor_uf_aplicado, d.subtotal "
                "FROM detalles_matricula d JOIN asignaturas a ON a.codigo=d.codigo_asignatura "
                "WHERE d.folio_matricula=? ORDER BY d.id",
                (folio,),
            ).fetchall()
