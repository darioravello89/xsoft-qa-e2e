# Agregar un escenario con ayuda de IA

1. Describir precondiciones, pasos visibles y resultado en esta carpeta. Elegir ID estable (`XG-MOD-NNN`) y tags: producto, módulo, `smoke` o `regression`, lectura/escritura.
2. Reutilizar keywords públicos de `library.py`; agregar uno cuando represente una acción del usuario o un resultado. No pasar credenciales como argumentos y no llamar SQL de escritura desde un keyword.
3. Agregar `.robot` en `suites/`. Cada prueba debe ejecutarse sola después de restaurar el fixture. Nunca depender de que otra haya creado la venta o iniciado sesión.
4. Añadir aliases semánticos nuevos a `contracts.py`, al ejemplo y al mapa privado. Calibrarlos con el JAR exacto, sin inventar propiedades accesibles a partir del nombre de un campo Java.
5. Si se requiere persistencia, agregar oráculos de lectura por PK completa. `ventas_cuerpo.vecCodigo` guarda el ID de artículo, distinto del `artCodigo` introducido en pantalla. No usar `MAX(venId)` como identidad única: el oráculo calcula diferencia de IDs bajo empresa/sucursal/computadora y exige una sola venta nueva.
6. Probar unidades de lógica del harness y `robot --dryrun`; después ejecutar la GUI real en laboratorio. Documentar por separado qué evidencia se obtuvo y qué quedó pendiente.

Las etiquetas `lectura` describen las acciones de negocio del escenario: el inicio del ERP puede actualizar configuración/estado local. Todo escenario se ejecuta dentro del laboratorio restaurable.

Para v1 quedan fuera facturación ARCA, impresora fiscal, impresión física, pagos electrónicos, sincronización cloud, cierre de caja y multiusuario concurrente. Se incorporan como suites separadas con fixtures y aceptación propios.
