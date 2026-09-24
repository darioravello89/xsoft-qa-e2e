# Evidencia de atajos — JAR 6085b7f3d

Preparado el 2026-09-24 desde `release/189-lts`, commit
`6085b7f3dae892b23ff9efd602b1b2416e60d741`. Incluye los atajos de
`3f8648035`, la cabecera de `2ecd5f3b4` y los ajustes visuales del commit
identificado. El checkout ERP tenía cambios concurrentes; el build usó
`git archive` del commit, **sin worktree ni cambios no confirmados**.

| Dato | Evidencia |
| --- | --- |
| FAT JAR privado | `.local/artifacts/6085b7f3d/dist/XGestion-6085b7f3d.jar` |
| SHA-256 JAR | `b749df85294c91b27bdfb0bd5a7b6792e35f5f00215fe5b647dc29803dc18997` |
| Tamaño | 175.495.761 bytes |
| SHA-256 archivo fuente | `7890746d843745ad2b91919ee57d767f55e525085e68ee0bf2d70a0e87c36f9b` |
| Compilación | Ant `jar`: `BUILD SUCCESSFUL`; verificador FAT de classloading y dependencias pasó |
| Registro privado | `.local/artifacts/6085b7f3d/artifact.json` y `build.log` |
| JAB / perfil / paquete | **NO EJECUTADO**: no hay VM exclusiva ni paquete privado |

Los 13 casos tienen suite Robot y dry-run; ningún caso tiene validación real.
El `qa.cmd doctor --product xgestion` sigue informando que falta el paquete.
No se inició el JAR contra la instalación habitual.

| Casos | Pantallas | Automatización | JAB real | Defecto reproducible |
| --- | --- | --- | --- | --- |
| KEY-001/002 | Cuentas corrientes clientes, general e individual | Codificada | No ejecutado | No determinado |
| KEY-003/004 | Cuentas corrientes proveedores, general e individual | Codificada | No ejecutado | No determinado |
| KEY-005/006/007 | Clientes, Productos, Mesas | Codificada | No ejecutado | No determinado |
| KEY-008/009/010 | Usuarios, Turnos, Compras | Codificada | No ejecutado | No determinado |
| KEY-011/012/013 | Proveedores, Categorías, Subcategorías | Codificada | No ejecutado | No determinado |

ACC-011 (orden), ACC-012 (contador de recarga lógica) y ACC-013 (X nativa)
siguen siendo requisitos de observabilidad por verificar en este JAR. Su
ausencia en la calibración debe clasificarse BLOQUEADO, no como PASS ni como
defecto funcional confirmado. El seed público no prepara los datos de las
trece pantallas. La [guía de automatización](atajos-automatizacion.md)
describe los aliases y fixtures privados necesarios para la primera corrida.
