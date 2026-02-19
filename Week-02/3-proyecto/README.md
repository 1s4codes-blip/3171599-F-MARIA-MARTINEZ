📄 README   

# 🛡️ Plataforma de Seguros Online – API CRUD

Proyecto académico – Semana 02  
Implementación de API REST utilizando **FastAPI** y **Pydantic v2**.

---

## 🎯 Objetivo

Desarrollar un CRUD completo para la gestión de **titulares de pólizas** aplicando validaciones de datos, normalización y tipado fuerte mediante Pydantic.

---

## 🧠 Adaptación al Dominio FinTech

Aunque el proyecto base parte de contactos, el modelo fue adaptado a clientes de una aseguradora.

Se añadieron campos del negocio como:

- `document_id` → identificación del cliente  
- `monthly_premium` → valor mensual a pagar por la póliza  

---

## 📦 Modelo de Datos

Cada titular de seguro contiene:

| Campo | Tipo | Regla |
|------|------|------|
| first_name | str | 2–50 caracteres |
| last_name | str | 2–50 caracteres |
| email | EmailStr | formato válido |
| phone | str | mínimo 7 dígitos |
| document_id | str | identificación del cliente |
| monthly_premium | float | debe ser mayor a 0 |
| company | str \| None | opcional |
| tags | list[str] | máximo 5, sin duplicados |
| is_favorite | bool | default False |
| created_at | datetime | automático |
| updated_at | datetime \| None | automático |

---

## ✅ Validaciones Implementadas

- Capitalización automática de nombres.
- Limpieza del teléfono dejando solo números.
- Conversión de tags a minúsculas.
- Eliminación de duplicados en tags.
- Límite máximo de 5 etiquetas.
- Prima mensual mayor a cero.

---

## 🚀 Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/contacts` | Crear cliente |
| GET | `/contacts` | Listar (paginado) |
| GET | `/contacts/{id}` | Obtener por ID |
| GET | `/contacts/email/{email}` | Buscar por email |
| PATCH | `/contacts/{id}` | Actualizar parcialmente |
| DELETE | `/contacts/{id}` | Eliminar |
| POST | `/contacts/{id}/favorite` | Alternar favorito |

---

## ▶️ Ejecución

```bash
docker compose up --build

Documentación automática disponible en:

http://localhost:8000/docs
🧩 Tecnologías

FastAPI

Pydantic v2

Docker

Base de datos en memoria