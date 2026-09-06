# 📚 Gestor Académico de Notas

Aplicación web desarrollada con Python y Streamlit para que los estudiantes puedan registrar y consultar sus notas académicas de forma sencilla.

El sistema permite organizar las asignaturas por cortes, registrar actividades y sus respectivas calificaciones, calcular automáticamente las notas y consultar el promedio general.

## 🎯 Objetivo

Facilitar el seguimiento de las calificaciones académicas, permitiendo conocer cuánto se ha evaluado de una asignatura, cuál es la nota acumulada y cuál será la nota final cuando se complete el 100% de la evaluación.

## 🛠️ Tecnologías utilizadas

- Python
- Streamlit
- SQLite
- Pandas
- Plotly
- Git
- GitHub

## ⚙️ Funcionalidades

- Crear y consultar asignaturas.
- Configurar los porcentajes de los tres cortes.
- Registrar actividades por cada corte.
- Registrar calificaciones entre 0.0 y 5.0.
- Modificar actividades y calificaciones.
- Eliminar actividades.
- Dejar actividades pendientes de calificación.
- Calcular automáticamente la nota de cada corte.
- Calcular la nota acumulada de cada asignatura.
- Mostrar el porcentaje de evaluación realizado.
- Calcular el promedio general.
- Visualizar las notas mediante un gráfico.
- Guardar la información localmente utilizando SQLite.

## 📊 Organización de las notas

Cada asignatura cuenta con tres cortes. Por defecto, estos tienen la siguiente distribución:

| Corte | Porcentaje |
|---|---:|
| Corte 1 | 30% |
| Corte 2 | 30% |
| Corte 3 | 40% |

Los porcentajes pueden modificarse siempre que la suma de los tres cortes sea exactamente 100%.

Cada corte puede contener diferentes actividades, y la suma de sus porcentajes no puede superar el 100%.

## 🧮 Cálculo de notas

La nota de un corte se calcula teniendo en cuenta la nota obtenida en cada actividad y el porcentaje asignado a esta.

La nota acumulada de una asignatura se obtiene a partir de la contribución de cada corte.

El sistema también muestra qué porcentaje de la asignatura ya ha sido evaluado.

La nota final se muestra cuando se ha completado el 100% de la evaluación.

## 💾 Persistencia

La aplicación utiliza SQLite para almacenar:

- Asignaturas.
- Cortes.
- Actividades.
- Porcentajes.
- Calificaciones.

La base de datos se crea automáticamente como `notas.db` al ejecutar la aplicación.

El archivo de base de datos no se incluye en el repositorio debido a que se encuentra dentro de las reglas del `.gitignore`.

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/carloszuluaga-20/programacion-web.git