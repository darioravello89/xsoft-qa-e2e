---
{"id":"XG-FIN-005","title":"Conservar saldos ajenos al consultar y corregir otro contexto","product":"xgestion","module":"conciliacion","tags":["xgestion","regression","conciliacion","integridad-operaciones","varios-puestos","permisos","cuenta-corriente"],"status":"planned"}
---

# XG-FIN-005 — Conservar saldos ajenos al consultar y corregir otro contexto

## Objetivo

Evitar que identificar sólo un número local mezcle dinero o documentos de distintos contextos.

## Estado y alcance

**Pendiente de automatizar (`planned`), prioridad P0.** Etapas 3–4, integridad entre circuitos.
Ver [roadmap de circuitos críticos](../../docs/circuitos-criticos.md). No tiene Robot, seed propio ni evidencia del JAR.

## Precondiciones y datos

- Windows QA aislado, JAR identificado, baseline recuperable y paquete autorizado. Sin fiscal, correo, servicios externos ni impresoras salvo laboratorio expresamente preparado.
- Paquete multicontexto todavía inexistente: empresa A sucursal S1 puestos P1/P2 y empresa B; mismo número local de venta/movimiento en cada contexto, importes ARS 1.000/2.000/3.000. Clientes/proveedores identificados por empresa. Roles con alcance definido; no inventar acceso a otra empresa.
- Nombres QA e importes son requisitos públicos de fixtures futuros; no están creados por esta ficha ni garantizados por el seed comercial. Calibración de controles y lecturas por identidad pendientes.
- Definir moneda, concepto, medio, empresa, sucursal, puesto, operador y período antes de ejecutar. No cambiar datos mediante SQL para corregir una operación en curso.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Consultar desde A/S1/P1 el documento de ARS 1.000 y sus movimientos relacionados. | Origen, empresa, sucursal, puesto y persona corresponden a P1; ningún enlace abre el documento homónimo de P2 o B. |
| 2 | Realizar una corrección permitida sobre el documento de P1, registrando su delta esperado antes de confirmar. | Sólo cambia la operación elegida y sus efectos legítimos. Las operaciones de P2 y B conservan importes y estados. |
| 3 | Ingresar con el rol restringido y repetir consulta y acceso a la corrección. | Se respeta el alcance configurado sin mutaciones no autorizadas; registrar si el permiso real opera por menú o por acción. |
| 4 | Revisar agregados por cliente/proveedor dentro de A. | Una cuenta empresarial puede incluir legítimamente varios puestos: no exigir una deuda independiente por caja. La corrección cambia el agregado de A por el delta previsto y nunca el de B. |

## Variantes y dependencias

Sucursal diferente, número local repetido y mismo nombre de persona con identidades distintas. El caso específico de baja de Libro Diario se enlaza desde su mapa: el UPDATE sin Computadora es riesgo de fuente a reproducir, no evidencia de defecto ya probado. No ejecutar hasta recibir el paquete multicontexto.

Las dependencias sin procedimiento reproducible bloquean la variante. Un resultado observado no se convierte automáticamente en el resultado esperado. La aprobación exige todos los pasos y variantes habilitadas del perfil, identificando cuáles siguen pendientes.

## Evidencia y límites

Registrar importes antes/después, identidad de documentos y deltas de deuda, caja, stock y movimientos relevantes. Cada dominio tiene su alcance: dos representaciones técnicas no acreditan dos movimientos de dinero. Conservar lectura acotada y saneada, sin filas completas, credenciales ni datos privados en el repositorio.

INFO muestra caso y resultado; DEBUG acciones de negocio; TRACE controles, esperas y diagnóstico saneado. Todo fallo incluye paso, esperado, observado y evidencia; causa no determinada si no está demostrada. Un dry-run no acredita estos resultados.

## Recuperación

Cancelar las acciones no confirmadas. Ante persistencia incierta, consultar antes de reintentar y no ejecutar compensaciones improvisadas. Conservar evidencia privada, cerrar sólo procesos propios y restaurar el baseline mediante el procedimiento del laboratorio. La anulación de negocio no reemplaza la restauración técnica de datos.

## Anexo técnico y trazabilidad

Fuente inspeccionada: XGestion2 `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.
Los tests fuente son insumos de reglas/riesgos, no evidencia de ejecución del JAR.

- `src/ModuloFinanzas/Entidades/MovimientoFinanzas.java:382-395`.
- `src/ModuloFinanzas/Entidades/CuentaCorrienteSaldoService.java:42-92`.
- `src/ModuloVentas/Servicios/AuditoriaVentasService.java:491-556`.
- `test/ModuloVentas/Entidades/TurnoCajaSqlBuilderTest.java`.

Registrar build/SHA256 del JAR, perfil, paquete, fecha, responsable, IDs y reporte privado al validar. Cambios posteriores de fuente obligan a revisar el contrato antes de ejecutar.
