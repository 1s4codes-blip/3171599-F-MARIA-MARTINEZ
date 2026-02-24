"""
API de Plataforma de Seguros Online - Main
===================================
"""

from fastapi import FastAPI
from routers import categories, products

app = FastAPI(
    title="API de Catálogo de Productos",
    description="API completa con CRUD, filtrado, paginación y ordenamiento",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Incluir routers
app.include_router(categories.router)
app.include_router(products.router)


@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz"""
    return {
        "message": "API Plataforma de Seguros Online",
        "docs": "/docs",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Root"])
async def health_check():
    """Health check"""
    return {"status": "healthy"}
