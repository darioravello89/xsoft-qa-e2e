# Incorporar la app Flutter de mozos

1. Identificar repositorio, APK QA, versión, hash y application ID reales. Confirmar endpoints y credenciales QA mediante canal privado.
2. Reservar emulador/dispositivo Android y datos de mesas/pedidos aislados. Documentar permisos y condición inicial.
3. Instalar Maestro y Android tools únicamente al activar el producto. Fijar versiones y repetir instalación en una estación QA limpia.
4. Inspeccionar Semantics del APK. Los `Key` internos de Flutter no sustituyen identificadores expuestos al sistema. Si faltan controles, registrar el requisito para el equipo de la app.
5. Implementar acceso y consulta antes de crear pedidos. Definir recuperación de pedidos y efectos en cocina/ERP antes de activar escenarios mutantes.
6. Incorporar flujos, casos Markdown, evidencia y comandos del runner; acreditar una ejecución real antes de quitar `planned`.

La desconexión total de red es una condición de XGestion v1, no una receta universal para esta app. Al incorporar Mozos se deberá especificar su conectividad al backend QA sin habilitar sistemas productivos. iOS queda fuera de la primera incorporación Android.
