*** Settings ***
Documentation    Smoke Swing real. Requiere paquete privado y calibración JAB vinculada al SHA256 del JAR.
Library          products.xgestion.library.XGestionLibrary
Test Setup       Iniciar XGestion QA
Test Teardown    Cerrar XGestion QA
Test Tags        xgestion    smoke    regression    lectura


*** Test Cases ***
XG-INI-001 Inicio muestra acceso
    [Documentation]    Verifica los controles de acceso del JAR iniciado por el escenario.
    [Tags]    inicio    XG-INI-001
    Verificar Pantalla De Acceso

XG-AUT-001 Credenciales invalidas
    [Documentation]    Rechaza credenciales inválidas y comprueba la limpieza de ambos campos.
    [Tags]    autenticacion    XG-AUT-001
    Rechazar Credenciales Invalidas

XG-AUT-002 Login y contexto QA
    [Documentation]    Comprueba empresa, sucursal y usuario después del login QA real.
    [Tags]    autenticacion    XG-AUT-002
    Ingresar Como QA
    Verificar Contexto QA
    Capturar Evidencia QA

XG-PRO-001 Buscar producto conocido
    [Documentation]    Busca el código fixture y verifica su nombre en el listado.
    [Tags]    productos    XG-PRO-001
    Ingresar Como QA
    Buscar Producto Conocido
    Capturar Evidencia QA

XG-PRO-002 Buscar producto inexistente
    [Documentation]    Comprueba el indicador vacío después de buscar un código ausente.
    [Tags]    productos    XG-PRO-002
    Ingresar Como QA
    Buscar Producto Inexistente
    Capturar Evidencia QA
