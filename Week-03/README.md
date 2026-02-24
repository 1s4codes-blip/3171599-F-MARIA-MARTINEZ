📍 Semana 03 – API Plataforma de Seguros Online
📌 Descripción

API REST desarrollada con FastAPI para la gestión de una Plataforma de Seguros Online (Servicios Financieros y FinTech).

Permite administrar:

Tipos de seguro

Seguros (planes/pólizas)

Filtros

Paginación

Ordenamiento

Incluye validación de parámetros y documentación automática.

🎯 Requisitos Implementados

✔ Rutas RESTful
✔ Path Parameters con validación (gt=0)
✔ Query Parameters con valores por defecto
✔ Filtros dinámicos
✔ Paginación
✔ Ordenamiento
✔ Combinación de parámetros
✔ Swagger funcional

🗂️ Estructura
starter/
├── routers/
│   ├── categories.py
│   └── products.py
├── database.py
├── dependencies.py
├── schemas.py
├── main.py
└── README.md
🏦 Modelo
Tipos de Seguro

id

name

description

created_at

Seguros

id

name

description

price

coverage_amount

category_id

created_at

🚀 Endpoints
📂 Tipos de Seguro

GET /categories

GET /categories/{id}

POST /categories

PUT /categories/{id}

DELETE /categories/{id}

🛡️ Seguros

GET /products

GET /products/{id}

POST /products

PUT /products/{id}

PATCH /products/{id}

DELETE /products/{id}

🔎 Query Parameters

Filtros

search

category_id

min_price

max_price

Paginación

page (default=1)

per_page (default=10)

Ordenamiento

sort_by (name, price, created_at)

order (asc, desc)

📄 Documentación

Swagger:

/docs

Redoc:

/redoc
🧠 Tecnologías

FastAPI

Pydantic v2

Depends()

APIRouter

Base de datos en memoria