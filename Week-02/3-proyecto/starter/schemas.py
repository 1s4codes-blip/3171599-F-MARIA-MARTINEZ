"""
Schemas Pydantic para la API de Gestión de Pólizas de Seguro
===========================================================
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import date, datetime
from decimal import Decimal
from typing import Literal
import re


# ============================================
# 1. PolicyBase - Campos comunes a varios schemas
# ============================================

class PolicyBase(BaseModel):
    """
    Campos comunes para las pólizas.
    """
    policy_number: str = Field(..., min_length=8, max_length=20, description="Número único de póliza (ej: POL-ABC123456)")
    customer_name: str = Field(..., min_length=3, max_length=100, description="Nombre completo del asegurado")
    customer_id: str = Field(..., min_length=6, max_length=20, description="Número de documento (cédula, NIT, etc.)")
    coverage_type: Literal["vida", "salud", "auto", "hogar", "viaje"] = Field(..., description="Tipo de cobertura")
    premium_amount: Decimal = Field(..., gt=0, decimal_places=2, description="Valor de la prima en COP")
    start_date: date = Field(..., description="Fecha de inicio de la póliza")
    end_date: date = Field(..., description="Fecha de vencimiento de la póliza")
    is_active: bool = Field(default=True, description="Indica si la póliza está activa")


# ============================================
# 2. PolicyCreate - Para crear pólizas (POST)
# ============================================

class PolicyCreate(PolicyBase):
    """
    Schema para crear una nueva póliza.
    Incluye validadores específicos del negocio de seguros.
    """

    @field_validator("policy_number", mode="before")
    @classmethod
    def validate_and_normalize_policy_number(cls, v: str) -> str:
        """Valida y normaliza el número de póliza."""
        v = v.strip().upper()
        if not re.match(r"^POL-[A-Z]{3}\d{6,8}$", v):
            raise ValueError("El número de póliza debe tener formato POL-XXX###### (ej: POL-ABC123456)")
        return v

    @field_validator("customer_name", mode="before")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        """Normaliza el nombre: quita espacios extras y pone en formato título."""
        return v.strip().title()

    @field_validator("end_date")
    @classmethod
    def end_after_start(cls, v: date, values) -> date:
        """Asegura que la fecha de fin sea posterior a la de inicio."""
        if "start_date" in values and v <= values["start_date"]:
            raise ValueError("La fecha de vencimiento debe ser posterior a la fecha de inicio")
        return v

    @field_validator("premium_amount", mode="before")
    @classmethod
    def minimum_premium(cls, v) -> Decimal:
        """Valida que la prima cumpla con el mínimo establecido."""
        if Decimal(v) < Decimal("50000"):
            raise ValueError("La prima mínima es 50.000 COP")
        return Decimal(v)


# ============================================
# 3. PolicyUpdate - Para actualizaciones parciales (PATCH)
# ============================================

class PolicyUpdate(BaseModel):
    """
    Schema para actualizar póliza de forma parcial.
    Todos los campos son opcionales.
    """
    policy_number: str | None = None
    customer_name: str | None = None
    customer_id: str | None = None
    coverage_type: Literal["vida", "salud", "auto", "hogar", "viaje"] | None = None
    premium_amount: Decimal | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool | None = None


# ============================================
# 4. PolicyResponse - Lo que se devuelve en las respuestas
# ============================================

class PolicyResponse(PolicyBase):
    """
    Schema para respuestas de póliza (incluye ID y timestamps).
    """
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


# ============================================
# 5. PolicyList - Para la lista paginada
# ============================================

class PolicyList(BaseModel):
    """
    Schema para la lista paginada de pólizas.
    """
    items: list[PolicyResponse]
    total: int
    page: int
    per_page: int