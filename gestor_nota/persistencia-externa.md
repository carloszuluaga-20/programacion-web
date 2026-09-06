# Comparación de alternativas de persistencia externa

Actualmente, la aplicación utiliza SQLite para almacenar la información de forma local. Esta opción funciona correctamente durante el desarrollo, pero para una aplicación desplegada en Internet sería conveniente utilizar una base de datos externa que permita mantener la información disponible de forma persistente.

## 1. Supabase

Supabase es una plataforma que proporciona una base de datos PostgreSQL administrada, además de otros servicios para aplicaciones web. Su plan gratuito permite crear hasta dos proyectos activos y cada proyecto cuenta con una instancia PostgreSQL. El plan gratuito incluye hasta 500 MB de almacenamiento de base de datos por proyecto. [1]

### Ventajas

* Utiliza PostgreSQL, por lo que permite trabajar con un modelo relacional similar al utilizado actualmente.
* Permite almacenar la información en la nube y acceder a ella desde la aplicación desplegada.
* Cuenta con herramientas para administrar la base de datos desde una interfaz web.
* Su plan gratuito es suficiente para una aplicación académica pequeña.

### Desventajas

* Requiere configurar una base de datos externa y modificar la aplicación para conectarse a ella.
* El plan gratuito tiene límites de almacenamiento y uso.
* Se deben proteger correctamente las credenciales de conexión.

## 2. MongoDB Atlas

MongoDB Atlas es un servicio administrado para utilizar MongoDB en la nube. Su clúster gratuito está orientado a proyectos pequeños y de desarrollo. Actualmente permite hasta 0,5 GB de almacenamiento y hasta 500 conexiones, además de otras limitaciones propias del nivel gratuito. [2]

### Ventajas

* Permite almacenar información en la nube sin administrar directamente un servidor.
* Su modelo documental puede ser flexible para aplicaciones cuyos datos cambien con frecuencia.
* Cuenta con un nivel gratuito para proyectos pequeños.
* Proporciona herramientas para administrar y supervisar la base de datos.

### Desventajas

* Utiliza un modelo NoSQL, por lo que sería necesario adaptar el modelo relacional utilizado actualmente.
* El nivel gratuito tiene límites de almacenamiento, operaciones y conexiones.
* Para este proyecto implicaría una migración mayor que utilizar una solución basada en PostgreSQL.

## 3. Comparación

| Característica                | Supabase              | MongoDB Atlas            |
| ----------------------------- | --------------------- | ------------------------ |
| Tipo de base de datos         | PostgreSQL relacional | MongoDB documental       |
| Modelo                        | Tablas y relaciones   | Documentos y colecciones |
| Plan gratuito                 | Sí                    | Sí                       |
| Almacenamiento gratuito       | 500 MB por proyecto   | 0,5 GB                   |
| Adaptación al proyecto actual | Alta                  | Media                    |
| Facilidad para este proyecto  | Alta                  | Media                    |

## 4. Recomendación

Para el Gestor Académico de Notas se recomienda **Supabase**, principalmente porque utiliza PostgreSQL y el modelo de datos actual de la aplicación ya está diseñado de forma relacional mediante asignaturas, cortes y actividades.

La migración desde SQLite hacia PostgreSQL sería más sencilla que adaptar toda la estructura a un modelo documental. Además, el plan gratuito de Supabase ofrece suficiente capacidad para una aplicación académica pequeña.

Por esta razón, si en una siguiente versión se necesitara que los datos fueran persistentes en Internet, Supabase sería la alternativa recomendada.

## Fuentes

[1] Supabase, “About billing on Supabase,” documentación oficial. [Supabase – Billing](https://supabase.com/docs/guides/platform/billing-on-supabase?utm_source=chatgpt.com)

[2] MongoDB, “Límites del clúster gratuito de Atlas,” documentación oficial. [MongoDB Atlas – Límites del clúster gratuito](https://www.mongodb.com/es/docs/atlas/reference/free-shared-limitations/?utm_source=chatgpt.com)
