"""Registro de recorridos; 077/078 requieren otro laboratorio."""

from framework.errors import QAError

from . import combos, conditions, currencies, grouped, payments, price_lists, profiled, scopes
from .contracts import validate_journey

CASES = {}
for _module in (scopes, grouped, combos, conditions, profiled, price_lists, payments, currencies):
    for _identifier, _journey in _module.CASES.items():
        if _identifier in CASES or _journey.id != _identifier:
            raise QAError("El catálogo de recorridos tiene identidades repetidas o inconsistentes.")
        validate_journey(_journey)
        CASES[_identifier] = _journey

if set(CASES) != {f"XG-PRM-{number:03}" for number in (*range(8, 77), *range(79, 85))}:
    raise QAError("El catálogo de recorridos no contiene los 75 escenarios acordados.")


def get_journey(identifier):
    try:
        return CASES[identifier]
    except (KeyError, TypeError):
        raise QAError("Recorrido desconocido o pendiente de laboratorio; no se ejecuta.") from None


def get_journeys():
    return tuple(CASES[identifier] for identifier in sorted(CASES))
