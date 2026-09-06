# Prompt de desarrollo — Gestor Académico de Notas

## 1. Rol

Actúa como un desarrollador senior especializado en Python, Streamlit, SQLite, Pandas y Plotly. Debes desarrollar una aplicación web sencilla, clara y funcional, siguiendo estrictamente los requisitos indicados en este documento.

La aplicación será desarrollada con apoyo de inteligencia artificial, por lo que el código debe ser claro, organizado y fácil de comprender y modificar por estudiantes de Ingeniería de Sistemas.

## 2. Objetivo

Crear una aplicación web llamada **Gestor Académico de Notas** que permita a los estudiantes registrar sus asignaturas, configurar sus tres cortes, agregar actividades y notas, y conocer automáticamente su progreso académico.

La aplicación debe permitir consultar la nota acumulada, el porcentaje evaluado y la nota final cuando el 100 % de la asignatura haya sido evaluado.

La información debe almacenarse localmente utilizando SQLite para que los datos permanezcan disponibles al cerrar y volver a abrir la aplicación.

## 3. Tecnologías

* Python 3
* Streamlit
* SQLite mediante el módulo `sqlite3`
* Pandas
* Plotly
* Git y GitHub

No utilizar tecnologías adicionales que no sean necesarias para cumplir los requisitos.

## 4. Requisitos funcionales

### RF01. Crear y seleccionar asignaturas

Permitir crear nuevas asignaturas indicando su nombre y seleccionar una asignatura existente para consultar o modificar su información.

### RF02. Tres cortes por asignatura

Cada asignatura debe manejar exactamente tres cortes: Corte 1, Corte 2 y Corte 3.

### RF03. Configurar porcentajes de los cortes

Permitir definir el porcentaje correspondiente a cada uno de los tres cortes.

La suma de los porcentajes debe ser exactamente 100 %. Si no se cumple, mostrar un mensaje de error y evitar guardar la configuración.

### RF04. Agregar actividades

Permitir agregar una cantidad ilimitada de actividades dentro de cada corte.

### RF05. Porcentaje de actividades

Cada actividad debe tener un porcentaje dentro del corte.

La aplicación debe controlar que la suma de los porcentajes de las actividades de cada corte no supere el 100 % y debe permitir completar el corte hasta llegar al 100 %.

### RF06. Registrar y actualizar notas

Permitir registrar y actualizar la nota de cada actividad en una escala de 0.0 a 5.0.

No se deben permitir notas menores a 0.0 ni mayores a 5.0.

### RF07. Calcular nota del corte

Calcular automáticamente la nota de cada corte utilizando:

**Nota del corte = Σ (nota de actividad × porcentaje de actividad / 100)**

Las actividades que todavía no tengan nota no deben aportar a la nota acumulada.

### RF08. Calcular nota acumulada y final

Calcular automáticamente el aporte de cada corte:

**Aporte del corte = nota del corte × porcentaje del corte / 100**

La nota acumulada será la suma de los aportes correspondientes a las actividades que ya hayan sido calificadas.

Cuando el 100 % de la asignatura esté evaluado, mostrar la nota final.

Cuando todavía falten actividades por evaluar, diferenciar claramente entre nota acumulada/parcial y nota final.

### RF09. Porcentaje evaluado

Mostrar el porcentaje de la asignatura que ya ha sido evaluado.

### RF10. Gráfico de asignaturas

Mostrar un gráfico de barras utilizando Plotly con las asignaturas registradas y su nota acumulada o final.

### RF11. Promedio general

Calcular y mostrar el promedio general de las asignaturas registradas.

Para cada asignatura se debe utilizar su nota acumulada o final disponible.

### RF12. Persistencia de datos

Guardar en SQLite las asignaturas, cortes, actividades, porcentajes y notas.

Los datos deben recuperarse automáticamente al iniciar nuevamente la aplicación.

## 5. Requisitos no funcionales

### RNF01. Interfaz

La interfaz debe ser clara, consistente y fácil de comprender sin necesitar una explicación extensa.

### RNF02. Validaciones

Validar campos obligatorios, porcentajes y notas antes de guardar información.

### RNF03. Organización del código

Organizar el código mediante funciones claras y reutilizables.

### RNF04. SQLite

La base de datos SQLite debe crearse automáticamente si no existe.

Las tablas necesarias también deben crearse automáticamente.

### RNF05. Seguridad

No guardar contraseñas, tokens, claves API ni otros secretos dentro del código o repositorio.

### RNF06. Ejecución y despliegue

La aplicación debe poder ejecutarse utilizando `requirements.txt` y debe ser compatible con Streamlit Community Cloud.

### RNF07. Control de versiones

El proyecto debe poder gestionarse mediante Git y GitHub, realizando commits que representen cambios funcionales comprensibles.

## 6. Modelo de datos

Utilizar SQLite con las siguientes entidades:

### Asignatura

* `id`
* `nombre`

### Corte

* `id`
* `asignatura_id`
* `numero`
* `porcentaje`

Cada asignatura debe tener exactamente tres cortes.

### Actividad

* `id`
* `corte_id`
* `nombre`
* `porcentaje`
* `nota`

La relación debe ser:

**Asignatura → Cortes → Actividades**

Una asignatura tiene tres cortes y cada corte puede tener múltiples actividades.

## 7. Reglas de negocio

* Las notas deben estar entre 0.0 y 5.0.
* Los cortes deben ser exactamente 3 por asignatura.
* Los porcentajes de los cortes deben sumar 100 %.
* Los porcentajes de las actividades de un corte no pueden superar el 100 %.
* Una actividad puede existir sin nota mientras todavía no haya sido evaluada.
* Una actividad sin nota no debe aportar a la nota acumulada.
* El porcentaje evaluado debe representar únicamente el peso de las actividades que ya tienen una nota.
* La nota acumulada debe mostrar únicamente los puntos obtenidos sobre el 100 % total de la asignatura.
* La nota final solamente debe mostrarse cuando el 100 % de la asignatura esté evaluado.

## 8. Cálculos

Para cada corte:

**Nota del corte = Σ (nota × porcentaje de actividad / 100)**

Para cada corte:

**Aporte del corte = nota del corte × porcentaje del corte / 100**

Para la asignatura:

**Nota acumulada = suma de los aportes correspondientes a las actividades evaluadas**

El porcentaje evaluado debe calcularse según el peso de las actividades que ya tienen nota.

Si el porcentaje evaluado es 100 %, la nota acumulada corresponde a la nota final.

## 9. Interfaz

La aplicación tendrá una navegación principal mediante una barra lateral.

### Dashboard

Mostrar:

* Promedio general.
* Número de asignaturas.
* Porcentaje evaluado.
* Resumen de cada asignatura.
* Nota acumulada o final.
* Gráfico de barras de las asignaturas.

### Asignaturas

Permitir:

* Crear una asignatura.
* Seleccionar una asignatura existente.
* Consultar información de la asignatura.

### Configuración de cortes

Mostrar los tres cortes de la asignatura seleccionada y permitir configurar:

* Porcentaje del Corte 1.
* Porcentaje del Corte 2.
* Porcentaje del Corte 3.

Mostrar validación de la suma total.

### Actividades y notas

Permitir seleccionar un corte y:

* Agregar actividades.
* Definir nombre.
* Definir porcentaje.
* Registrar nota.
* Actualizar nota.
* Consultar actividades existentes.

Mostrar la nota calculada del corte y su aporte a la asignatura.

## 10. Diseño visual

Utilizar inicialmente un diseño sencillo, limpio y académico.

* Fondo claro.
* Barra lateral para navegación.
* Tarjetas para mostrar estadísticas.
* Componentes de Streamlit para formularios, botones, selectores y mensajes.
* Verde para mensajes de éxito.
* Rojo para errores y validaciones.
* Gráfico de barras mediante Plotly.
* Mantener una distribución ordenada y fácil de leer.
* Evitar elementos visuales innecesarios que dificulten el uso de la aplicación.

El diseño podrá modificarse posteriormente sin afectar la lógica de la aplicación.

## 11. Persistencia

Crear automáticamente una base de datos llamada:

`notas.db`

Crear las tablas necesarias al iniciar la aplicación si todavía no existen.

La aplicación debe realizar operaciones para:

* Crear asignaturas.
* Consultar asignaturas.
* Crear cortes.
* Consultar cortes.
* Actualizar porcentajes de cortes.
* Crear actividades.
* Consultar actividades.
* Actualizar notas.
* Recuperar toda la información almacenada.

El archivo `notas.db` no debe incluirse en GitHub.

## 12. Archivos esperados

Generar y mantener como mínimo:

```text
gestor_notas_2026/
├── app.py
├── prompt.md
├── README.md
├── requirements.txt
└── .gitignore
```

La aplicación principal debe estar en `app.py`.

## 13. Criterios de aceptación

La aplicación se considera funcional cuando:

1. Puede iniciarse mediante Streamlit sin errores.
2. Permite crear asignaturas.
3. Cada asignatura tiene exactamente tres cortes.
4. Los porcentajes de los cortes deben sumar 100 %.
5. Permite agregar múltiples actividades.
6. Valida los porcentajes de las actividades.
7. Permite registrar notas entre 0.0 y 5.0.
8. Calcula correctamente la nota de cada corte.
9. Calcula correctamente la nota acumulada.
10. Muestra el porcentaje evaluado.
11. Muestra la nota final cuando el 100 % esté evaluado.
12. Muestra un gráfico de barras por asignatura.
13. Calcula el promedio general.
14. Guarda los datos en SQLite.
15. Los datos permanecen disponibles después de cerrar y volver a abrir la aplicación.

## 14. Forma de trabajo con IA

Antes de generar el código completo:

1. Proponer la estructura del proyecto.
2. Explicar el modelo de datos y las relaciones.
3. Esperar revisión de la estructura antes de generar el código.
4. Generar el código completo por archivo.
5. Explicar brevemente la función de las partes principales.
6. Probar la aplicación localmente.
7. Corregir únicamente los errores encontrados.
8. No regenerar todo el proyecto innecesariamente.
9. Mantener el código sencillo y comprensible.
10. No implementar funcionalidades que no estén relacionadas con los requisitos.

## 15. Entregables

El proyecto debe permitir obtener:

* `prompt.md` como especificación técnica.
* Código fuente de la aplicación.
* `requirements.txt`.
* `README.md`.
* `.gitignore`.
* Repositorio GitHub con commits comprensibles.
* Aplicación desplegada en Streamlit Community Cloud.
* Evidencia de pruebas de los requisitos.
