# Agregar un escenario con ayuda de IA

1. Leer [roadmap](roadmap.md) y [cobertura](cobertura.md). Describir en `../scenarios/` objetivo de usuario, perfil, datos, pasos con resultado, recuperación y evidencia. Elegir ID estable (`XG-MOD-NNN`) y tags del registro de grupos. Una ficha `planned` no necesita ni debe simular un `.robot`.
2. Reutilizar keywords públicos de `library.py`; agregar uno cuando represente una acción del usuario o un resultado. No pasar credenciales como argumentos y no llamar SQL de escritura desde un keyword.
3. Agregar `.robot` en `suites/`. Cada prueba debe ejecutarse sola después de restaurar el fixture. Nunca depender de que otra haya creado la venta o iniciado sesión.
4. Añadir aliases semánticos nuevos a `contracts.py`, al ejemplo y al mapa privado. Calibrarlos con el JAR exacto, sin inventar propiedades accesibles a partir del nombre de un campo Java.
5. Si se requiere persistencia, agregar oráculos de lectura por PK completa. `ventas_cuerpo.vecCodigo` guarda el ID de artículo, distinto del `artCodigo` introducido en pantalla. No usar `MAX(venId)` como identidad única: el oráculo calcula diferencia de IDs bajo empresa/sucursal/computadora y exige una sola venta nueva.
6. Probar unidades de lógica del harness y `qa.cmd run --product xgestion --group regression --dry-run`; después ejecutar la GUI real en laboratorio. Documentar por separado qué evidencia se obtuvo y qué quedó pendiente. Al implementar una ficha, cambiar su estado y añadir su archivo de test; escribir la ficha sola no la hace ejecutable.

Las etiquetas `lectura` describen las acciones de negocio del escenario: el inicio del ERP puede actualizar configuración/estado local. Todo escenario se ejecuta dentro del laboratorio restaurable.

Para v1 quedan fuera facturación ARCA, impresora fiscal, impresión física, pagos electrónicos, sincronización cloud, cierre de caja y multiusuario concurrente. Se incorporan como suites separadas con fixtures y aceptación propios.

Mantener las comprobaciones de negocio en lenguaje QA y trasladar SQL y selectores al anexo. Los logs INFO cuentan resultado y resumen; DEBUG, acciones y comprobaciones; TRACE, diagnóstico saneado. Ningún nivel registra credenciales ni contenido de campos de autenticación. Un fallo debe informar esperado/observado y evidencia sin inventar una causa.
