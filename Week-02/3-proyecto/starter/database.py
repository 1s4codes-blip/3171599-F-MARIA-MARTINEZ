"""
Simulación de Base de Datos
===========================

Base de datos en memoria para pólizas de seguro.
"""

# "Base de datos" en memoria (diccionario con ID como clave)
policies_db: dict[int, dict] = {}

# Contador para generar IDs automáticos
_id_counter = 0


def get_next_id() -> int:
    """Obtiene el siguiente ID disponible."""
    global _id_counter
    _id_counter += 1
    return _id_counter


def find_by_policy_number(policy_number: str) -> dict | None:
    """Busca una póliza por su número único (insensible a mayúsculas)."""
    policy_number_upper = policy_number.upper()
    for policy in policies_db.values():
        if policy["policy_number"].upper() == policy_number_upper:
            return policy
    return None


def reset_db() -> None:
    """Resetea completamente la base de datos (útil para pruebas)."""
    global _id_counter
    policies_db.clear()
    _id_counter = 0