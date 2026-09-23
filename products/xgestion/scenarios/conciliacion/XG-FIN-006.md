---
{"id":"XG-FIN-006","title":"Conservar la venta ante rechazo y registrar la autorización de abandono","product":"xgestion","module":"conciliacion","tags":["xgestion","regression","conciliacion","integridad-operaciones","permisos","recuperacion"],"status":"planned"}
---

# XG-FIN-006 — Conservar la venta ante rechazo y registrar la autorización de abandono

## Objetivo

Probar rechazo, autorización y trazabilidad de una acción sensible sin perder una venta por un intento rechazado.

## Estado y alcance

**Pendiente de automatizar (`planned`), prioridad P0.** Etapas 3–4, integridad entre circuitos.
Ver [roadmap de circuitos críticos](../../docs/circuitos-criticos.md). No tiene Robot, seed propio ni evidencia del JAR.

## Precondiciones y datos

- Windows QA aislado, JAR identificado, baseline recuperable y paquete autorizado. Sin fiscal, correo, servicios externos ni impresoras salvo laboratorio expresamente preparado.
- Venta abierta de una unidad ARS 1.000 sin cerrar; stock persistido 10 y caja ARS 5.000. Perfil con autorización de supervisor para abandonar, vendedor restringido y supervisor QA. Datos y controles del diálogo pendientes; no usar credenciales reales ni registrar sus valores.
- Nombres QA e importes son requisitos públicos de fixtures futuros; no están creados por esta ficha ni garantizados por el seed comercial. Calibración de controles y lecturas por identidad pendientes.
- Definir moneda, concepto, medio, empresa, sucursal, puesto, operador y período antes de ejecutar. No cambiar datos mediante SQL para corregir una operación en curso.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Solicitar abandono, aceptar la confirmación de salida y cancelar la autorización de supervisor o ingresar una autorización inválida. | La venta conserva producto, cantidad e importe; no cambian stock persistido, deuda ni caja. |
| 2 | Repetir, aceptar la confirmación de salida y autorizar con supervisor habilitado. | La venta se abandona una vez, sin cobrar ni descontar stock. La auditoría identifica acción, vendedor y autorizante según el perfil. |
| 3 | Consultar auditoría con un usuario habilitado. | Se reconoce la operación y el motivo; la autorización no contiene contraseña. El tiempo de espera admite el guardado asíncrono, con límite y evidencia. |
| 4 | Iniciar una nueva venta. | No arrastra autorización, productos ni condiciones sensibles de la venta abandonada. |

## Variantes y dependencias

Perfil sin supervisor separa autorización no requerida de autorización aprobada. Auditoría deshabilitada/habilitada se declara antes de probar. Cambios de precio/descuentos usan sus propios permisos; no asumir que el permiso de abandono los controla. El recorrido VEN-007 de rechazar abandono no sustituye este perfil con supervisor.

Las dependencias sin procedimiento reproducible bloquean la variante. Un resultado observado no se convierte automáticamente en el resultado esperado. La aprobación exige todos los pasos y variantes habilitadas del perfil, identificando cuáles siguen pendientes.

## Evidencia y límites

Registrar importes antes/después, identidad de documentos y deltas de deuda, caja, stock y movimientos relevantes. Cada dominio tiene su alcance: dos representaciones técnicas no acreditan dos movimientos de dinero. Conservar lectura acotada y saneada, sin filas completas, credenciales ni datos privados en el repositorio.

INFO muestra caso y resultado; DEBUG acciones de negocio; TRACE controles, esperas y diagnóstico saneado. Todo fallo incluye paso, esperado, observado y evidencia; causa no determinada si no está demostrada. Un dry-run no acredita estos resultados.

## Recuperación

Cancelar las acciones no confirmadas. Ante persistencia incierta, consultar antes de reintentar y no ejecutar compensaciones improvisadas. Conservar evidencia privada, cerrar sólo procesos propios y restaurar el baseline mediante el procedimiento del laboratorio. La anulación de negocio no reemplaza la restauración técnica de datos.

## Anexo técnico y trazabilidad

Fuente inspeccionada: XGestion2 `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.
Los tests fuente son insumos de reglas/riesgos, no evidencia de ejecución del JAR.

- `src/ModuloVentas/Vistas/FormVenta.java:681-709`.
- `src/ModuloVentas/Servicios/AuditoriaVentasService.java`.
- `test/ModuloVentas/Servicios/AuditoriaVentasContratoTest.java`.

Registrar build/SHA256 del JAR, perfil, paquete, fecha, responsable, IDs y reporte privado al validar. Cambios posteriores de fuente obligan a revisar el contrato antes de ejecutar.
