"""Contrato pequeño para datos públicos y valores exactos del seed."""

import re
from dataclasses import dataclass, field
from datetime import date
from decimal import Decimal

from framework.errors import QAError

NAME = "catalogo-comercial-v1"
SOURCE_COMMIT = "f34238183d494259bed1279dd7d9aac0ce16a3ae"
IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,63}\Z")


@dataclass(frozen=True)
class SeedContext:
    empresa: int
    sucursal: int
    computadora: int
    usuario_id: int
    reference_date: date

    def __post_init__(self):
        if any(type(value) is not int or not 0 < value <= 2147483647
               for value in (self.empresa, self.sucursal, self.computadora, self.usuario_id)):
            raise QAError("El contexto del seed requiere IDs positivos de empresa, sucursal, puesto y usuario.")
        if type(self.reference_date) is not date:
            raise QAError("La fecha de referencia del seed debe ser una fecha de calendario.")


@dataclass
class SeedTable:
    name: str
    keys: tuple[str, ...]
    identity: tuple[str, ...]
    rows: list[dict]
    natural_keys: tuple[tuple[str, ...], ...] = field(default_factory=tuple)

    def __post_init__(self):
        names = [self.name, *self.keys, *self.identity, *(key for row in self.rows for key in row),
                 *(key for fields in self.natural_keys for key in fields)]
        if not self.keys or not self.identity or any(not isinstance(name, str) or not IDENTIFIER.fullmatch(name)
                                                   for name in names):
            raise QAError("El catálogo seed contiene identificadores SQL o identidades inválidos.")
        required = set(self.keys + self.identity).union(*(set(fields) for fields in self.natural_keys))
        if any(not required.issubset(row) or any(row[key] is None for key in self.keys)
               for row in self.rows):
            raise QAError("Una fila del seed no declara su clave e identidad completas.")
        if any(not (value is None or type(value) in (str, int) or
                    isinstance(value, Decimal) and value.is_finite())
               for row in self.rows for value in row.values()):
            raise QAError("El seed solo admite valores escalares exactos; no usar float ni objetos.")


def merge_tables(tables: list[SeedTable]) -> list[SeedTable]:
    result = {}
    for table in tables:
        if table.name not in result:
            result[table.name] = SeedTable(table.name, table.keys, table.identity, [], table.natural_keys)
        target = result[table.name]
        if (target.keys, target.identity, target.natural_keys) != (table.keys, table.identity, table.natural_keys):
            raise QAError(f"Contratos distintos para la misma tabla seed: {table.name}.")
        target.rows.extend(dict(row) for row in table.rows)
    for table in result.values():
        for fields in (table.keys, *table.natural_keys):
            identities = [tuple(row[key] for key in fields) for row in table.rows]
            if len(set(identities)) != len(identities):
                raise QAError(f"Clave duplicada dentro del seed: {table.name}.")
    return list(result.values())
