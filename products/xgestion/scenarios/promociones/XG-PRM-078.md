---
{"id":"XG-PRM-078","title":"Mantener las ofertas aisladas entre empresas","product":"xgestion","module":"promociones","tags":["xgestion","regression","promociones","promociones-condiciones"],"status":"planned"}
---

# XG-PRM-078 — Mantener las ofertas aisladas entre empresas

## Objetivo

Mantener las ofertas aisladas entre empresas durante una venta, con importes y efectos observables por el vendedor o cajero.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1, etapa 2.**
Ficha para [el backlog de promociones](../../docs/promociones-pendientes.md).
Validación real pendiente. No tiene suite Robot ni resultado aprobado.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado, escritorio visible.
- ARS, comprobante interno 99, IVA 0%, stock suficiente y sin impresión ni fiscalización.
- Perfil por defecto sin listas, descuentos adicionales, fidelización ni ofertas superpuestas,
  salvo las condiciones expresamente indicadas a continuación.
- Nuevo laboratorio de dos empresas sintéticas A/B, pendiente de preparar y autorizar en el contrato de fixtures. Mismos códigos visibles y mismos IDs numéricos de artículo/oferta en ambas, precio normal $1.000; A tiene 10% y B tiene 20%. Cada empresa mantiene stock y ventas propios.
- Preparar cada variante de perfil desde su baseline antes de abrir XGestión;
  no cambiar datos comerciales con SQL durante el recorrido.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Ingresar al contexto A y cargar una unidad. | Neto $900; encabezado visible corresponde a A. |
| Confirmar $900 y registrar la identidad de la operación. | Pago, oferta y stock pertenecen solamente a A. |
| Desde baseline independiente ingresar a B y cargar el mismo código. | Neto $800; no se reutiliza el descuento de A. |
| Cancelar el cobro de B, retomarlo y confirmar $800. | Una venta en B; las identidades repetidas no mezclan pagos, ofertas ni movimientos. |
| Contrastar ambos contextos dentro de cada corrida. | Los registros ajenos a la empresa operativa conservan su estado inicial. |

## Dependencias para automatizar

Requiere ampliar el paquete y verificadores de aislamiento por empresa; no ampliar los permisos del runner como parte de esta ficha. No ejecutar sobre una base compartida.
El autor del caso debe comprobar datos y selectores en el JAR correspondiente;
si falta una precondición, informar bloqueo sin sustituir el esperado por lo observado.

## Evidencia y límites

Registrar producto, cantidad, precio, descuento y neto visibles en cada transición.
Conservar evidencia de cancelación sin efectos y de confirmación única cuando
corresponda. Contrastar venta, detalle, identidad de oferta, medio, stock y destino
del pago por operación y contexto; no imprimir filas completas. Los importes de
esta ficha son expectativas del perfil, no resultados medidos. El cobro de variantes
con otros medios o empresas requiere un contrato de laboratorio específico.

## Recuperación

Ante una discrepancia, conservar el reporte privado y abandonar por la interfaz
si está disponible. No corregir importes ni movimientos en la base para hacer pasar
el caso. Restaurar el baseline correspondiente antes de repetir o cambiar de perfil.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada: `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`.
Rutas relativas a XGestion2: `src/ModuloFinanzas/Entidades/Oferta.java`; `src/ModuloFinanzas/Entidades/OfertaLineaService.java`; `src/ModuloVentas/Entidades/TicketVenta.java`.
Esta referencia acredita reglas de fuente, no ejecución del artefacto.

Selectores accesibles y oráculos por identidad pendientes de implementar/calibrar;
registrar SHA256 del JAR, paquete, perfil y persona responsable en evidencia privada.
INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Todo fallo
informa paso, esperado, observado, categoría y evidencia; causa no determinada
cuando no existe prueba causal. No incluir credenciales ni configuración privada.

