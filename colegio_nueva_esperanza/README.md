# Colegio Nueva Esperanza — Evaluación Sumativa N°3

**Asignatura:** Programación Orientada a Objeto Seguro (TI3V21)  
**Sede:** INACAP Puente Alto  
**Docente:** Michael Arjel  
**Equipo:** Viviana Núñez y Johana Larrondo  
**Sección:** 114-2A-F2

## Instalación y ejecución

Requiere Python 3.9 o superior. Desde la carpeta del proyecto:

```bash
python -m pip install -r requirements.txt
python main.py
```

La base `colegio_nueva_esperanza.db` se crea junto a `main.py`. Al iniciar se crean las tablas y se cargan asignaturas de ejemplo. Las matrículas se guardan con cabecera y detalles dentro de una transacción SQLite.

## Pruebas de la guía

- Estudiantes: crear, listar, modificar curso/apoderado/deuda y eliminar.
- RUT: se valida con módulo 11 y se guarda normalizado.
- Evaluaciones: Prueba 40%, Trabajo 35% y Presentación oral 25%; notas válidas de 1,0 a 7,0.
- Matrículas: la opción 6 registra tres asignaturas; la opción 7 lista cabecera y detalles.
- Deuda: la matrícula se bloquea tanto en el menú como en la transacción DAO.
- Electivos: `ING201` parte con un cupo. Cada inscripción exitosa descuenta uno; al agotarse se rechazan las siguientes.
- UF: se consulta `https://mindicador.cl/api/uf` con timeout. Si falla, el sistema muestra el aviso y utiliza el valor local de respaldo de $39.000.
- Entradas incorrectas y errores de base de datos se informan sin cerrar el menú.

La base contiene datos de prueba locales. Para repetir la prueba de cupos, el cupo de `ING201` debe restaurarse a 1 en la tabla `asignaturas` antes de empezar una nueva corrida.
