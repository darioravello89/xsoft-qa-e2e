# Fuentes del adaptador

- API primaria: [RPA.JavaAccessBridge Python](https://rpaframework.org/libraries/javaaccessbridge/python.html): selección por PID/título, búsqueda estricta, acciones accesibles, texto y refresco del árbol.
- [Implementación de JavaAccessBridge](https://github.com/robocorp/rpaframework/blob/master/packages/main/src/RPA/JavaAccessBridge.py): API consultada al construir adaptador lazy. No se copia el cierre global por `taskkill`; se administra únicamente `subprocess.Popen` propio.
- Fuente local XGestion `release/189-lts`, commit inspeccionado `f34238183d494259bed1279dd7d9aac0ce16a3ae`: `AppXGestion.java`, `Login.java`, `FormVenta.java`, `formTicketCierre.java`, `TicketVenta.java`, `Constantes.java`, `DATABASE_SCHEMA.sql`. Sustentan flujos, claves y SQL; no demuestran localizadores JAB.
- Pipeline privado de tutoriales XSoft: `XGVideoBase.java` y `TutorialRealizarVenta.java` sirvieron para identificar orden de pantallas/controles. No se reutiliza su bypass de soporte, invocación directa de negocio, supresión de diálogos ni limpieza de ventas.

La prueba funcional del JAR distribuido y sus selectores queda pendiente hasta ejecutar el paquete QA privado en el laboratorio. Lint, unittest y dry-run no son QA GUI.
