# 📦 Proyecto Semana 02: API CRUD con FastAPI y Pydantic

## 🏛️ Dominio

**Plataforma de Seguros Online | FinTech**

Esta API permite gestionar pólizas de seguro mediante operaciones CRUD completas, aplicando validaciones con **Pydantic v2**.

---

## 🎯 Objetivo

Desarrollar una API REST para la gestión de pólizas de seguro, incluyendo:

* Creación de pólizas
* Consulta (individual y listada)
* Actualización parcial
* Eliminación
* Validaciones de negocio
* Paginación y filtros

---

## 🧱 Modelo de Datos

Entidad principal: **Policy (Póliza de Seguro)**

| Campo          | Tipo     | Descripción                      |
| -------------- | -------- | -------------------------------- |
| id             | int      | ID autogenerado                  |
| policy_number  | str      | Número único (ej: POL-ABC123456) |
| customer_name  | str      | Nombre del cliente               |
| customer_id    | str      | Documento del cliente            |
| coverage_type  | enum     | vida, salud, auto, hogar, viaje  |
| premium_amount | Decimal  | Valor de la prima                |
| start_date     | date     | Fecha de inicio                  |
| end_date       | date     | Fecha de vencimiento             |
| is_active      | bool     | Estado de la póliza              |
| created_at     | datetime | Fecha de creación                |
| updated_at     | datetime | Fecha de actualización           |

---

## ✅ Validaciones Implementadas

* ✔ Formato de póliza: `POL-XXX######`
* ✔ Nombre capitalizado automáticamente
* ✔ Prima mínima: **50,000 COP**
* ✔ Fecha de fin mayor a fecha de inicio
* ✔ Número de póliza único

---

## 🚀 Endpoints

### 📌 Crear póliza

```
POST /policies
```

### 📌 Listar pólizas (con paginación y filtro)

```
GET /policies?page=1&per_page=10&coverage_type=vida
```

### 📌 Obtener por ID

```
GET /policies/{id}
```

### 📌 Buscar por número de póliza

```
GET /policies/by-policy_number/{value}
```

### 📌 Actualizar parcialmente

```
PATCH /policies/{id}
```

### 📌 Eliminar

```
DELETE /policies/{id}
```

---

## 🗂️ Estructura del Proyecto

```
starter/
├── main.py            # API principal (FastAPI)
├── schemas.py         # Modelos Pydantic
├── database.py        # Base de datos en memoria
├── pyproject.toml     # Dependencias
├── Dockerfile         # Configuración Docker
├── docker-compose.yml # Orquestación
```

---

## 🧠 Base de Datos

Se utiliza una base de datos en memoria con:

```python
policies_db: dict[int, dict] = {}
```

Incluye:

* Generación automática de IDs
* Búsqueda por número de póliza
* Reset para testing

---

## ▶️ Ejecución del Proyecto

### 🔹 Opción 1: Local (sin Docker)

```bash
uvicorn main:app --reload
```

Abrir en navegador:

```
http://127.0.0.1:8000
```

Documentación Swagger:

```
http://127.0.0.1:8000/docs
```

---

### 🔹 Opción 2: Con Docker

```bash
docker compose up --build
```

---

## 🧪 Ejemplo de JSON (POST)

```json
{
  "policy_number": "POL-ABC123456",
  "customer_name": "Juan Perez",
  "customer_id": "123456789",
  "coverage_type": "vida",
  "premium_amount": 100000,
  "start_date": "2025-01-01",
  "end_date": "2025-12-31",
  "is_active": true
}
```

---