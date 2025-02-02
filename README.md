# Documentación de la API

## Descripción General
Esta API permite gestionar reservas para un sistema de mesas en un restaurante. Proporciona endpoints para crear, consultar, actualizar y eliminar reservas.

## Autenticación
La API no requiere autenticación.

## Varibles de entorno
```
#Application Config
SECRET_KEY = ""

#Database Confguration
HOST_DB = ""
USER_DB = ""
PASS_DB = ""
DB = ""
```

## Levantar DB
Inicializar el sistema de migraciones.

- flask db init (inicializar el sistema de migraciones)
- flask db migrate (inicializar la migracion)
- flask db upgrade

## Levantar API

instalar dependencias.

Es necesario tener instalado poetry
```shell
pip install poetry
```

- poetry install

correr API.
- python run.py


## Endpoints

## **Reservations**
### 1. Crear una Reserva
Crea una nueva reserva.

- **URL:** `/reservation`
- **Método:** `POST`
- **Body (JSON):**
  ```json
  {
    "customer_id": 1,
    "table_id": 2,
    "reservation_date": "2025-01-27T20:00:00",
    "duration_hours": 2,
    "status": "confirmed" #default: pending
  }
  ```

### 2. Confirmar una reserva
Confirmar reserva

- **URL:** `/reservation/{id}`
- **Método:** `PUT`
- **Body (JSON):**
  ```json
  {
    "status": "confirmed"
  }
  ```

### 3. Obtener todas las reservas
Obtener todas las reservas.

- **URL:** `/reservations`
- **Método:** `GET`
```json
[
    {
        "customer": {
            "email": "jd@example.com",
            "id": 1,
            "name": "Juan Delgado",
            "phone": "9999-4444-2222"
        },
        "id": 1,
        "reservation_date": "2025-01-30T16:00:00",
        "status": "confirmed",
        "table": {
            "id": 1,
            "number": 1,
            "seats": 2
        }
    },
    {
        "customer": {
            "email": "jd@example.com",
            "id": 1,
            "name": "Juan Delgado",
            "phone": "1111-7777-6666"
        },
        "id": 2,
        "reservation_date": "2025-01-30T18:00:00",
        "status": "confirmed",
        "table": {
            "id": 1,
            "number": 1,
            "seats": 2
        }
    }
]
```
### 4. Obtener reserva por ID
Confirmar reserva

- **URL:** `/reservation/{id}`
- **Método:** `GET`
- **Body (JSON):**
  ```json
    {
        "customer": {
            "email": "jd@example.com",
            "id": 1,
            "name": "Juan Delgado",
            "phone": "9999-4444-2222"
        },
        "id": 3,
        "reservation_date": "2025-01-30T16:00:00",
        "status": "confirmed",
        "table": {
            "id": 1,
            "number": 1,
            "seats": 2
        }
    }
  ```