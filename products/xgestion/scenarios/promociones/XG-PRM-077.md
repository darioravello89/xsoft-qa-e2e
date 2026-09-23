---
{"id":"XG-PRM-077","title":"Limitar las ofertas a las sucursales configuradas","product":"xgestion","module":"promociones","tags":["xgestion","regression","promociones","promociones-condiciones"],"status":"planned"}
---

# XG-PRM-077 — Limitar las ofertas a las sucursales configuradas

## Objetivo

Limitar las ofertas a las sucursales configuradas durante una venta, con importes y efectos observables por el vendedor o cajero.

## Estado y alcance

**Pendiente de automatizar — `planned`. Prioridad P1, etapa 2.**
Ficha para [el backlog de promociones](../../docs/promociones-pendientes.md).
Validación real pendiente. No tiene suite Robot ni resultado aprobado.

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete privado autorizado, escritorio visible.
- ARS, comprobante interno 99, IVA 0%, stock suficiente y sin impresión ni fiscalización.
- Perfil por defecto sin listas, descuentos adicionales, fidelización ni ofertas superpuestas,
  salvo las condiciones expresamente indicadas a continuación.
- Nuevo paquete multi-sucursal QA aislado y pendiente de preparar. A y B son sucursales de una empresa sintética; producto $1.000 con 10% solo A. Otro producto CONTROL tiene 10% para Todas. Identidades verificadas por contexto, sin conectar instalaciones de sucursales reales.
- Preparar cada variante de perfil desde su baseline antes de abrir XGestión;
  no cambiar datos comerciales con SQL durante el recorrido.

## Pasos y resultados esperados

| Paso del usuario | Resultado esperado |
| --- | --- |
| Iniciar la corrida de A y cargar una unidad del producto y otra de CONTROL. | Ambas cuestan $900; total $1.800. |
| Restaurar y ejecutar la misma carga en el perfil B. | Producto $1.000 y CONTROL $900; total $1.900. |
| En B cancelar el cobro y retomarlo por $1.900. | No se habilita el beneficio exclusivo de A al reabrir el cobro. |
| Confirmar cada corrida y revisar el contexto del comprobante. | Una venta y movimientos solo en la sucursal seleccionada; ninguna modificación en la otra. |

## Dependencias para automatizar

El runner actual no habilita este laboratorio por existir la ficha. Ampliar baseline/contrato y oráculos de aislamiento antes de automatizar; nunca quitar los guards del seed para admitir contextos desconocidos.
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
Rutas relativas a XGestion2: `src/ModuloFinanzas/Entidades/OfertaLineaService.java`; `src/ModuloFinanzas/Entidades/Oferta.java`; `test/ModuloFinanzas/Entidades/OfertaAplicabilidadTest.java`.
Esta referencia acredita reglas de fuente, no ejecución del artefacto.

Selectores accesibles y oráculos por identidad pendientes de implementar/calibrar;
registrar SHA256 del JAR, paquete, perfil y persona responsable en evidencia privada.
INFO resume; DEBUG muestra pasos; TRACE aporta diagnóstico saneado. Todo fallo
informa paso, esperado, observado, categoría y evidencia; causa no determinada
cuando no existe prueba causal. No incluir credenciales ni configuración privada.

