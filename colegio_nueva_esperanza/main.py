from datetime import date
import sqlite3
from model.persona import Persona
from model.estudiante import Estudiante
from model.asignatura import Asignatura
from model.periodo_academico import PeriodoAcademico
from model.profesor import Profesor
from model.prueba import Prueba
from model.trabajo import Trabajo
from model.presentacion_oral import PresentacionOral
from model.matricula import Matricula
from model.arancel import Arancel
from model.excepciones import DeudaMatriculaException, CupoElectivoException
from services.api_service import APIService
from dao.database import init_db
from dao.estudiante_dao import EstudianteDAO
from dao.asignatura_dao import AsignaturaDAO
from dao.matricula_dao import MatriculaDAO


def mostrar_menu():
    print("\n" + "=" * 58)
    print("       COLEGIO NUEVA ESPERANZA — SISTEMA DE GESTIÓN")
    print("=" * 58)
    print(" 1. Crear estudiante (P02, P07, P08)")
    print(" 2. Listar estudiantes (P03, P05)")
    print(" 3. Modificar estudiante (curso, apoderado y deuda)")
    print(" 4. Eliminar estudiante (P06)")
    print(" 5. Probar evaluaciones y notas (P09, P10, P11, P19)")
    print(" 6. Registrar matrícula con tres asignaturas (P12, P16)")
    print(" 7. Ver matrícula y sus líneas de detalle (P13)")
    print(" 8. Probar bloqueo por deuda real (P14)")
    print(" 9. Inscribir en electivo con cupo limitado (P15)")
    print("10. Consultar UF y respaldo sin internet (P16, P17)")
    print(" 0. Salir")
    print("=" * 58)


def mostrar_estudiante(est):
    deuda = "Sí" if est.deuda_matricula_pendiente else "No"
    print(f"RUT: {est.rut} | {est.nombres} {est.apellidos} | Curso: {est.curso} | Apoderado: {est.apoderado} | Deuda: {deuda}")


def obtener_indicador_uf():
    indicador = APIService.obtener_indicador_uf(timeout_seconds=4)
    fuente = "respaldo local" if indicador.es_respaldo else "mindicador.cl"
    print(f"UF aplicada: ${indicador.obtener_valor():,.2f} CLP ({fuente}, fecha {indicador.fecha}).")
    return indicador


def pedir_estudiante():
    rut = input("RUT del estudiante: ").strip()
    estudiante = EstudianteDAO.obtener_por_rut(rut)
    if estudiante is None:
        print("No se encontró al estudiante. Regístrelo primero.")
    return estudiante


def main():
    init_db()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()
        try:
            if opcion == "1":
                nombres = input("Nombres: ").strip()
                apellidos = input("Apellidos: ").strip()
                rut = input("RUT (Ej: 12.345.678-5): ").strip()
                curso = input("Curso: ").strip() or "Sin asignar"
                apoderado = input("Nombre del apoderado: ").strip() or "Sin asignar"
                estudiante = Estudiante(rut, nombres, apellidos, curso=curso, apoderado=apoderado)
                if EstudianteDAO.crear(estudiante):
                    print("Estudiante guardado correctamente.")
                else:
                    print("Ya existe un estudiante con ese RUT.")

            elif opcion == "2":
                estudiantes = EstudianteDAO.listar_todos()
                if not estudiantes:
                    print("No hay estudiantes registrados.")
                for estudiante in estudiantes:
                    mostrar_estudiante(estudiante)

            elif opcion == "3":
                estudiante = pedir_estudiante()
                if estudiante:
                    estudiante.nombres = input(f"Nombres [{estudiante.nombres}]: ").strip() or estudiante.nombres
                    estudiante.apellidos = input(f"Apellidos [{estudiante.apellidos}]: ").strip() or estudiante.apellidos
                    estudiante.curso = input(f"Curso [{estudiante.curso}]: ").strip() or estudiante.curso
                    estudiante.apoderado = input(f"Apoderado [{estudiante.apoderado}]: ").strip() or estudiante.apoderado
                    deuda = input("¿Tiene deuda pendiente? (s/n, Enter conserva): ").strip().lower()
                    if deuda in ("s", "n"):
                        estudiante.deuda_matricula_pendiente = deuda == "s"
                    if EstudianteDAO.actualizar(estudiante):
                        print("Estudiante actualizado.")
                        mostrar_estudiante(estudiante)
                    else:
                        print("No se pudo actualizar el estudiante.")

            elif opcion == "4":
                rut = input("RUT del estudiante a eliminar: ").strip()
                if EstudianteDAO.eliminar(rut):
                    print("Estudiante eliminado.")
                else:
                    print("No se encontró al estudiante.")

            elif opcion == "5":
                nota_texto = input("Nota (1.0 a 7.0; puede escribir 8,5 o letras para probar validación): ").strip().replace(",", ".")
                periodo = PeriodoAcademico(2026, 2, "abierto", date(2026, 12, 31))
                asignatura = Asignatura("MAT101", "Matemática", 30, False)
                profesor = Profesor("12345678-5", "Ana", "Pérez")
                prueba = Prueba(date.today(), nota_texto, "Prueba 1", asignatura, profesor, periodo)
                trabajo = Trabajo(date.today(), nota_texto, "Trabajo 1", asignatura, profesor, periodo)
                oral = PresentacionOral(date.today(), nota_texto, "Presentación 1", asignatura, profesor, periodo)
                print(f"Prueba (40%): aporte {prueba.calcular_aporte():.2f}")
                print(f"Trabajo (35%): aporte {trabajo.calcular_aporte():.2f}")
                print(f"Presentación oral (25%): aporte {oral.calcular_aporte():.2f}")

            elif opcion == "6":
                folio = int(input("Folio de matrícula: ").strip())
                estudiante = pedir_estudiante()
                if estudiante:
                    if estudiante.deuda_matricula_pendiente:
                        raise DeudaMatriculaException("La matrícula se impidió: el estudiante tiene deuda pendiente.")
                    codigos_texto = input("Tres códigos de asignatura separados por coma [MAT101,HIS101,CIE101]: ").strip()
                    codigos = [c.strip().upper() for c in (codigos_texto or "MAT101,HIS101,CIE101").split(",") if c.strip()]
                    if len(codigos) != 3:
                        raise ValueError("Para esta prueba debe ingresar exactamente tres asignaturas.")
                    indicador = obtener_indicador_uf()
                    matricula = Matricula(folio, date.today())
                    arancel = Arancel(3.0)
                    for codigo in codigos:
                        asignatura = AsignaturaDAO.obtener_por_codigo(codigo)
                        if not asignatura:
                            raise ValueError(f"No existe la asignatura {codigo}.")
                        matricula.agregar_detalle(asignatura, arancel, indicador)
                    MatriculaDAO.guardar_transaccion(matricula, estudiante.rut)
                    print(f"Matrícula {folio} guardada con 3 asignaturas. Total: ${matricula.calcular_monto_total():,.2f} CLP.")

            elif opcion == "7":
                matriculas = MatriculaDAO.listar_todas()
                if not matriculas:
                    print("No hay matrículas registradas.")
                for mat in matriculas:
                    print(f"\nFolio: {mat[0]} | Fecha: {mat[1]} | RUT: {mat[2]} | Total: ${mat[3]:,.2f} CLP")
                    for detalle in MatriculaDAO.listar_detalles(mat[0]):
                        print(f"  - {detalle[0]} {detalle[1]} | UF aplicada: ${detalle[2]:,.2f} | Subtotal: ${detalle[3]:,.2f} CLP")

            elif opcion == "8":
                estudiante = pedir_estudiante()
                if estudiante:
                    prueba = Matricula(-1, date.today())
                    estudiante.solicitar_matricula(prueba)
                    if estudiante.deuda_matricula_pendiente:
                        raise DeudaMatriculaException("La matrícula se impidió: el estudiante tiene deuda pendiente.")
                    print("El estudiante no tiene deuda. Para registrarlo use la opción 6.")

            elif opcion == "9":
                estudiante = pedir_estudiante()
                if estudiante:
                    folio = int(input("Folio nuevo para esta matrícula de prueba: ").strip())
                    indicador = obtener_indicador_uf()
                    matricula = Matricula(folio, date.today())
                    electivo = AsignaturaDAO.obtener_por_codigo("ING201")
                    if electivo is None:
                        raise ValueError("No está configurado el electivo ING201.")
                    matricula.agregar_detalle(electivo, Arancel(2.5), indicador)
                    MatriculaDAO.guardar_transaccion(matricula, estudiante.rut)
                    print("Inscripción al electivo ING201 guardada. El cupo disponible se descontó.")

            elif opcion == "10":
                obtener_indicador_uf()
                print("Si la API no está disponible, se informa el uso del valor de respaldo y la aplicación continúa.")

            elif opcion == "0":
                print("Gracias por usar el sistema.")
                break
            else:
                print(f"Opción '{opcion}' no válida. Ingrese un número del 0 al 10.")
        except (ValueError, DeudaMatriculaException, CupoElectivoException, sqlite3.Error) as exc:
            print(f"No se pudo completar la operación: {exc}")
        except Exception as exc:
            print(f"Ocurrió un error al procesar la operación: {exc}")


if __name__ == "__main__":
    main()

