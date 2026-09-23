# Beneficios, impuestos y centavos

Seis fichas pendientes de automatización. Grupos `beneficios`, `descuentos`,
`impuestos` y `fidelizacion`; los tags se superponen y no agregan escenarios.
Este mapa complementa PRM-079 (descuento por artículo sobre oferta), REM y RES;
no considera esas pruebas como cobertura de puntos o desglose de Venta.

| Ficha | Recorrido | Prioridad |
| --- | --- | --- |
| [XG-BEN-001](../scenarios/beneficios/XG-BEN-001.md) | Combinar descuento por artículo y descuento global sin repetirlos | P0 |
| [XG-BEN-002](../scenarios/beneficios/XG-BEN-002.md) | Conservar centavos al editar cantidades fraccionadas y cobrar | P0 |
| [XG-BEN-003](../scenarios/beneficios/XG-BEN-003.md) | Consultar impuestos y conservar el total entre presentación e histórico | P0 |
| [XG-BEN-004](../scenarios/beneficios/XG-BEN-004.md) | Canjear puntos, cancelar y cobrar una sola vez | P0 |
| [XG-BEN-005](../scenarios/beneficios/XG-BEN-005.md) | Limitar puntos por vigencia, saldo y elegibilidad | P0 |
| [XG-BEN-006](../scenarios/beneficios/XG-BEN-006.md) | Cambiar de cliente o condición sin trasladar puntos ajenos | P0 |

## Preparación y orden

1. Fijar descuentos por renglón/global, cantidades fraccionadas y el cálculo
   de importes independiente del resultado del ERP (BEN-001/002).
2. Preparar tasas/precios netos o finales, tipo de comprobante local y
   desglose soportado por el JAR (BEN-003). No emite factura electrónica.
3. Preparar clientes, saldo/origen/fecha de puntos, vigencia y valor del canje
   (BEN-004..006). La fuente diferencia crédito y contado; no generalizarlos.

El perfil define reglas esperadas antes de ejecutar; diferencias de precisión,
elegibilidad mixta, exención o redondeo todavía sin contrato bloquean su variante.
Prioridad P0 indica riesgo monetario; no confirma un defecto del producto.

## Datos y aceptación futura

El seed comercial no prepara estos seis perfiles. Son necesarios puntos
ganados/usados/vencidos con fecha fija, dos clientes y consumidor final,
artículos elegibles/excluidos, stock, importes e impuestos conocidos. Nunca
alterar el reloj del host cotidiano para simular vencimientos.

Aceptar sólo con controles accesibles calibrados, comprobación de importes
visibles/persistidos, deltas por identidad y evidencia del JAR exacto.
Cancelar no consume puntos; una confirmación no debe repetir descuentos ni
consumos. Si una regla no coincide, conservar evidencia, no corregir la base.

```text
qa.cmd list --product xgestion --group beneficios
qa.cmd list --product xgestion --group fidelizacion
qa.cmd list --product xgestion --group impuestos
```

No usar `run` hasta implementar las fichas. INFO resume, DEBUG explica acciones
y TRACE añade diagnóstico saneado; ningún nivel publica credenciales o filas.

## Trazabilidad

Fuente ERP: `daa002d597d0fa7380ace204d3727085c52d1415`; referencias precisas en cada ficha.
La inspección de fuente/tests no acredita un JAR ni ejecución de usuario.
Ver [complemento de circuitos críticos](complementos-criticos.md),
[roadmap](roadmap.md) y [cobertura](cobertura.md).
