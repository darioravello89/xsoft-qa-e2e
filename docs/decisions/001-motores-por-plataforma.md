# ADR-001 — Runner común y motores por plataforma

Estado: aceptado para implementación; compatibilidad real del JAR pendiente de calibración.

Fecha: 2026-09-19.

## Contexto

XGestion es una aplicación Java Swing de escritorio. XPORTAL y Consultador son aplicaciones web; Mozos será una app Flutter independiente. QA necesita comandos simples y escenarios legibles, mientras la IA requiere estructura y contratos claros para mantenerlos.

## Decisión

Usar Robot Framework con Python 3.12 como base de automatización de XGestion y [`RPA.JavaAccessBridge`](https://rpaframework.org/libraries/javaaccessbridge/index.html) para controles Swing accesibles. PowerShell prepara el Windows QA y `qa.cmd` ofrece el punto único de entrada. Los selectores se calibran contra el hash de un JAR específico.

Reservar Robot Framework Browser —Playwright— para los productos web. La documentación de Browser concentra instalación y uso en [su repositorio oficial](https://github.com/MarketSquare/robotframework-browser); se incorporará al activar un producto web, sin obligar al QA de escritorio a instalar navegadores ahora.

Reservar Maestro para Mozos Android: sus flujos YAML se ejecutan sobre APK y utilizan el árbol Semantics de Flutter. Requiere identificadores accesibles y la verificación del APK real. Sus [reglas para Flutter](https://docs.maestro.dev/get-started/supported-platform/flutter) y [requisitos de instalación](https://docs.maestro.dev/maestro-cli/how-to-install-maestro-cli) son la referencia al incorporar ese producto.

## Alternativas y motivo

- Playwright directo para todo: resuelve aplicaciones web, pero no aporta acceso a controles Swing de XGestion.
- Automatización por coordenadas o imágenes como base: depende de resolución, foco y apariencia; se priorizan controles accesibles con cardinalidad y estado verificables.
- `integration_test` para Flutter: es útil dentro del proyecto de la app, pero la plataforma QA debe poder operar desde un repositorio separado con un APK. Se reconsiderará si el APK no expone controles suficientes.
- Un único motor para todas las plataformas: impone compromisos innecesarios. Unificar catálogo, comandos y documentación permite conservar motores adecuados para cada aplicación.

## Consecuencias

La prueba técnica de Java Access Bridge es un requisito de aceptación: no se declara compatible un JAR hasta verificar login, ventanas, grilla y venta. Los controles ausentes se informan como bloqueos, sin reemplazarlos silenciosamente por coordenadas.

Los E2E de XGestion requieren escritorio interactivo y datos privados; el CI público verifica infraestructura y parsing. La red desconectada limita llamadas involuntarias del ERP. MySQL 5.7 se conserva por compatibilidad del producto y se limita a la instancia local de QA; una actualización requiere validar el contrato del ERP.
