# Incorporar Consultador web

1. Confirmar producto/versionado servido en la URL QA y definir `CONSULTADOR_BASE_URL` localmente, sin datos sensibles en query strings.
2. Definir si requiere autenticación y los identificadores de empresa/sucursal que condicionan precios y disponibilidad.
3. Preparar artículos conocidos, código inexistente y reglas de precio del entorno. Precisar si el caso usa ingreso manual de código o un dispositivo físico.
4. Incorporar Browser/Playwright al setup web y comprobar consulta válida e inexistente con selectores reales.
5. Agregar casos Markdown y automatización, declarar los límites de cámaras/lectores físicos y registrar ejecución real antes de activar el producto.

Simular teclado o entrada de código no acredita QA física de un lector de barras o cámara. Esas pruebas se incorporan con hardware y criterios explícitos cuando formen parte del alcance.
