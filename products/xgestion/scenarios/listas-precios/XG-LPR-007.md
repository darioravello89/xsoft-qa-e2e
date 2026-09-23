---
{"id":"XG-LPR-007","title":"Recuperar una lista automática cuando la del cliente no es válida","product":"xgestion","module":"listas-precios","tags":["xgestion","regression","precios","listas-precios","listas-cliente","listas-prioridad"],"status":"planned"}
---

# XG-LPR-007 — Recuperar una lista automática cuando la del cliente no es válida

## Objetivo

Seguir vendiendo con el siguiente origen válido si la lista del cliente fue retirada o no pertenece al contexto.

## Estado y alcance

**Pendiente de automatizar (`planned`). Prioridad P1.** Etapa 2: condiciones comerciales; Restobar también depende de etapa 5. Sin Robot ni resultado aprobado. Ver [mapa de listas](../../docs/listas-precios.md).

## Precondiciones y datos

- Windows QA exclusivo y offline, paquete autorizado, JAR/entorno identificados y baseline restaurable.
- Operación local, comprobante interno no fiscal, IVA 0 %, stock suficiente, sin impresión, pagos externos, ofertas ni descuentos adicionales salvo indicación expresa.
- Fixture NUEVO PENDIENTE: C apunta a lista inexistente, inactiva o exclusiva de S2; corrida en S1. T activo A=$850; F activa A=$800; normal A=$1.000.
- Roles, datos adicionales, acceso por teclado/JAB y oráculos de lectura pendientes de preparar/verificar para esta ficha. Un ejemplo seed disponible no acredita esos requisitos.

## Pasos y resultados esperados

| Paso | Acción del usuario | Resultado esperado |
| ---: | --- | --- |
| 1 | Elegir C en S1 con T válido. | La lista inválida no se aplica; selector T. |
| 2 | Cargar A × 2. | Total $1.700; el cliente permanece identificado. |
| 3 | En otro perfil sin turno válido, elegir C. | Selector F; A × 2=$1.600. |
| 4 | Abandonar y abrir una venta. | No conserva una identidad inválida ni registra cobros de los intentos. |

## Variantes y dependencias

Tres variantes independientes: ID inexistente, cabecera inactiva y lista de otra sucursal. No reemplazar cabecera inactiva por lista vacía: son estados diferentes.

## Evidencia y límites

Registrar selector de lista, contexto, productos/cantidades, precio unitario, bruto, descuentos, neto y moneda antes/después. Comprobar por identidad lista de cabecera y renglones, documento y efectos de stock/cobro con lectura acotada; no volcar filas completas. Conservar implementación separada de validación real del JAR. INFO resume; DEBUG muestra pasos; TRACE añade diagnóstico saneado. Todo fallo conserva paso, esperado/observado y evidencia; causa no determinada si no está demostrada.

## Recuperación

Ante una discrepancia, detener la confirmación y conservar el informe privado. Cancelar diálogos y cerrar únicamente procesos propios del runner; una cuenta Restobar puede haber persistido cambios. Restaurar el baseline antes de repetir o cambiar perfil. No corregir precios con SQL durante una venta ni editar el esperado para que coincida con lo observado.

## Anexo técnico y trazabilidad

Fuente ERP inspeccionada en commit `4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a`; estas referencias describen reglas/riesgos, no una ejecución E2E.

- `src/ModuloVentas/Servicios/VentaListaPrecioPrioridadPolicy.java:37-74`.
- `src/ModuloVentas/Vistas/FormVenta.java:3413-3491`.
- `src/ModuloProveedores/Entidades/ListaPrecio.java:240-287`.

Registrar SHA256/build del JAR, paquete, perfil, fecha/horario y responsable en evidencia local. Los nombres QA son públicos; credenciales, nombres privados y capturas de autenticación no se publican.

