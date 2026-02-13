# ============================================
# PROYECTO: API DE SEGUROS ONLINE / FINTECH
# ============================================
# Semana 01 - Bootcamp FastAPI Zero to Hero
#
# En este proyecto implementarás una API del dominio
# de seguros que demuestra el uso de:
# - FastAPI
# - Type hints
# - Path parameters
# - Query parameters
# - Documentación automática
# ============================================

from fastapi import FastAPI

# ============================================
# DATOS DE CONFIGURACIÓN
# ============================================

# Mensajes de bienvenida por idioma
WELCOME_MESSAGES: dict[str, str] = {
    "es": "¡Bienvenido a la aseguradora digital, {name}!",
    "en": "Welcome to the digital insurance company, {name}!",
    "fr": "Bienvenue dans l'assurance numérique, {name}!",
}

# Idiomas soportados
SUPPORTED_LANGUAGES = list(WELCOME_MESSAGES.keys())


# ============================================
# TODO 1: CREAR LA INSTANCIA DE FASTAPI
# ============================================

app = FastAPI(
    title="Insurance & FinTech API",
    description="API for policy, claims and payment management",
    version="1.0.0",
)


# ============================================
# TODO 2: ENDPOINT RAÍZ
# ============================================

@app.get("/")
async def root() -> dict[str, str]:
    """Información principal de la API."""
    return {
        "name": "Insurance & FinTech API",
        "version": "1.0.0",
        "domain": "insurance",
    }


# ============================================
# TODO 3: BIENVENIDA PERSONALIZADA
# ============================================

@app.get("/{actor}/{name}")
async def welcome_actor(
    actor: str,
    name: str,
    language: str = "es",
) -> dict[str, str]:
    """
    Mensaje de bienvenida según el tipo de actor.
    """

    template = WELCOME_MESSAGES.get(language, WELCOME_MESSAGES["es"])
    message = template.format(name=name)

    return {
        "actor": actor,
        "message": message,
        "language": language,
        "available_roles": ["client", "agent", "admin"],
    }


# ============================================
# TODO 4: INFORMACIÓN DE ENTIDAD
# ============================================

@app.get("/{entity}/{identifier}/info")
async def entity_info(
    entity: str,
    identifier: str,
    detail_level: str = "basic",
) -> dict[str, str]:
    """
    Información de una entidad del dominio.
    """

    data = {
        "entity": entity,
        "id": identifier,
        "status": "active",
        "company": "SecureLife",
    }

    if detail_level == "full":
        data.update(
            {
                "coverage": "premium",
                "monthly_payment": "120 USD",
                "risk_level": "low",
                "valid_until": "2026-12-31",
            }
        )

    return data


# ============================================
# TODO 5: SERVICIO SEGÚN HORARIO
# ============================================

@app.get("/service/schedule")
async def service_schedule(hour: int) -> dict[str, str | list[str] | int]:
    """
    Disponibilidad de servicios según la hora.
    """

    if 6 <= hour <= 11:
        return {
            "message": "Morning operations",
            "available": ["policy creation", "claims assistance"],
            "hour": hour,
        }
    elif 12 <= hour <= 17:
        return {
            "message": "Afternoon operations",
            "available": ["payments", "policy updates"],
            "hour": hour,
        }
    else:
        return {
            "message": "Night support",
            "available": ["emergency claims"],
            "hour": hour,
        }


# ============================================
# TODO 6: HEALTH CHECK
# ============================================

@app.get("/health")
async def health_check() -> dict[str, str]:
    """Estado de la API."""
    return {
        "status": "healthy",
        "domain": "insurance",
    }


# ============================================
# VERIFICACIÓN
# ============================================
# Ejecutar:
# docker compose up --build
#
# Probar:
# http://localhost:8000/docs
# ============================================
