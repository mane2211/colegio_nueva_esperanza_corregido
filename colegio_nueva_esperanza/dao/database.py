import os
import sqlite3
from contextlib import closing

DB_NAME = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "colegio_nueva_esperanza.db")


def get_connection():
    conn = sqlite3.connect(DB_NAME, timeout=10)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _agregar_columna_si_falta(cursor, tabla, columna, definicion):
    columnas = {fila[1] for fila in cursor.execute(f"PRAGMA table_info({tabla})")}
    if columna not in columnas:
        cursor.execute(f"ALTER TABLE {tabla} ADD COLUMN {columna} {definicion}")


def init_db():
    with closing(get_connection()) as conn, conn:
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS estudiantes (
            rut TEXT PRIMARY KEY, nombres TEXT NOT NULL, apellidos TEXT NOT NULL,
            deuda_matricula_pendiente INTEGER NOT NULL DEFAULT 0,
            curso TEXT NOT NULL DEFAULT 'Sin asignar',
            apoderado TEXT NOT NULL DEFAULT 'Sin asignar'
        )""")
        _agregar_columna_si_falta(cursor, "estudiantes", "curso", "TEXT NOT NULL DEFAULT 'Sin asignar'")
        _agregar_columna_si_falta(cursor, "estudiantes", "apoderado", "TEXT NOT NULL DEFAULT 'Sin asignar'")
        cursor.execute("""CREATE TABLE IF NOT EXISTS asignaturas (
            codigo TEXT PRIMARY KEY, nombre TEXT NOT NULL, cupo INTEGER NOT NULL,
            es_electivo INTEGER NOT NULL
        )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS matriculas (
            folio INTEGER PRIMARY KEY, fecha_matricula TEXT NOT NULL,
            rut_estudiante TEXT NOT NULL, monto_total REAL NOT NULL,
            FOREIGN KEY (rut_estudiante) REFERENCES estudiantes(rut)
        )""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS detalles_matricula (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            folio_matricula INTEGER NOT NULL, codigo_asignatura TEXT NOT NULL,
            valor_uf_aplicado REAL NOT NULL, subtotal REAL NOT NULL,
            FOREIGN KEY (folio_matricula) REFERENCES matriculas(folio),
            FOREIGN KEY (codigo_asignatura) REFERENCES asignaturas(codigo)
        )""")
        cursor.executemany(
            "INSERT OR IGNORE INTO asignaturas (codigo, nombre, cupo, es_electivo) VALUES (?, ?, ?, ?)",
            [
                ("MAT101", "Matemática", 30, 0),
                ("HIS101", "Historia", 25, 0),
                ("CIE101", "Ciencias", 20, 0),
                ("ING201", "Inglés Avanzado", 1, 1),
            ],
        )
