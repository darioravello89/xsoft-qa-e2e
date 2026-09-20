# Incorporar XPORTAL

1. Confirmar URL QA y colocar `XPORTAL_BASE_URL` localmente. Verificar que redirecciones y autenticación permanecen en el entorno autorizado.
2. Recibir cuenta QA y tenant exclusivo por canal privado. Definir permisos y baseline que permita repetir los casos.
3. Incorporar dependencia Browser/Playwright y navegadores mediante setup del producto. No instalar el servidor de XPORTAL automáticamente.
4. Validar un caso real de acceso y uno de lectura con selectores semánticos antes de incorporar mutaciones.
5. Registrar casos Markdown y Robot coherentes, reportes protegidos y evidencia real. Actualizar el estado de `planned` cuando el producto pueda ejecutarse.

La preparación de servidor y cambios de aplicación pertenecen a sus repositorios responsables. El harness no cambia configuración productiva ni obtiene autorización de una sesión ajena.
