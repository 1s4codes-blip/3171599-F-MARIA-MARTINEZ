"""
Proyecto Semana 02: API de Gestión de Pólizas de Seguro
=======================================================

Aplicación principal con FastAPI.
"""

from fastapi import FastAPI, HTTPException, status, Query
from datetime import datetime

from schemas import (
    PolicyCreate,
    PolicyUpdate,
    PolicyResponse,
    PolicyList,
)
from database import policies_db, get_next_id, find_by_policy_number

app = FastAPI(
    title="API de Gestión de Pólizas de Seguro",
    description="Proyecto Semana 02 - Plataforma de Seguros Online (FinTech)",
    version="1.0.0",
)


# ============================================
# ENDPOINTS CRUD
# ============================================

@app.post(
    "/policies",
    response_model=PolicyResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Policies"],
)
async def create_policy(policy: PolicyCreate) -> PolicyResponse:
    """
    Crea una nueva póliza.
    Valida que el número de póliza sea único.
    """
    if find_by_policy_number(policy.policy_number):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe una póliza con el número {policy.policy_number}"
        )
    
    policy_id = get_next_id()
    new_policy = {
        "id": policy_id,
        **policy.model_dump(),
        "created_at": datetime.now(),
        "updated_at": None,
    }
    policies_db[policy_id] = new_policy
    
    return new_policy


@app.get(
    "/policies",
    response_model=PolicyList,
    tags=["Policies"],
)
async def list_policies(
    page: int = Query(ge=1, default=1),
    per_page: int = Query(ge=1, le=100, default=10),
    coverage_type: str | None = None,
) -> PolicyList:
    """
    Lista las pólizas con paginación.
    Permite filtro opcional por tipo de cobertura.
    """
    policies = list(policies_db.values())
    
    if coverage_type:
        policies = [p for p in policies if p["coverage_type"] == coverage_type]
    
    total = len(policies)
    start = (page - 1) * per_page
    end = start + per_page
    items = policies[start:end]
    
    return PolicyList(
        items=items,
        total=total,
        page=page,
        per_page=per_page,
    )


@app.get(
    "/policies/{policy_id}",
    response_model=PolicyResponse,
    tags=["Policies"],
)
async def get_policy(policy_id: int) -> PolicyResponse:
    """Obtiene una póliza por su ID."""
    if policy_id not in policies_db:
        raise HTTPException(status_code=404, detail="Póliza no encontrada")
    return policies_db[policy_id]


@app.get(
    "/policies/by-policy_number/{value}",
    response_model=PolicyResponse,
    tags=["Policies"],
)
async def get_policy_by_number(value: str) -> PolicyResponse:
    """Busca una póliza por su número único."""
    policy = find_by_policy_number(value)
    if not policy:
        raise HTTPException(status_code=404, detail="Póliza no encontrada")
    return policy


@app.patch(
    "/policies/{policy_id}",
    response_model=PolicyResponse,
    tags=["Policies"],
)
async def update_policy(
    policy_id: int,
    policy: PolicyUpdate,
) -> PolicyResponse:
    """
    Actualiza una póliza de forma parcial.
    Solo modifica los campos enviados.
    """
    if policy_id not in policies_db:
        raise HTTPException(status_code=404, detail="Póliza no encontrada")
    
    update_data = policy.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    
    # Validar unicidad si se cambia el número de póliza
    if "policy_number" in update_data:
        existing = find_by_policy_number(update_data["policy_number"])
        if existing and existing["id"] != policy_id:
            raise HTTPException(
                status_code=409,
                detail=f"El número {update_data['policy_number']} ya está en uso"
            )
    
    stored = policies_db[policy_id]
    for key, value in update_data.items():
        stored[key] = value
    stored["updated_at"] = datetime.now()
    
    return stored


@app.delete(
    "/policies/{policy_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Policies"],
)
async def delete_policy(policy_id: int) -> None:
    """Elimina una póliza por su ID."""
    if policy_id not in policies_db:
        raise HTTPException(status_code=404, detail="Póliza no encontrada")
    del policies_db[policy_id]


# ============================================
# HEALTH CHECK (opcional pero recomendado)
# ============================================

@app.get("/", tags=["Health"])
async def root():
    """Health check simple de la API."""
    return {
        "status": "ok",
        "message": "API de Pólizas de Seguro corriendo correctamente",
        "total_policies": len(policies_db),
    }