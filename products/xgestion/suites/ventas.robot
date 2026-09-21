*** Settings ***
Documentation    Venta persistida no fiscal y cancelación. Sólo instancia QA restaurable, suite serial.
Library          products.xgestion.library.XGestionLibrary
Test Setup       Iniciar XGestion QA
Test Teardown    Cerrar XGestion QA
Test Tags        xgestion    regression    ventas    escritura


*** Test Cases ***
XG-VEN-001 Venta efectivo dos unidades
    [Documentation]    Cobra 2000 ARS no fiscales y comprueba venta, detalle, pago, stock y caja.
    [Tags]    XG-VEN-001    efectivo    cobros
    Ingresar Como QA
    Preparar Venta Basica
    Cobrar Venta En Efectivo
    Verificar Venta Persistida
    Capturar Evidencia QA

XG-VEN-002 Cancelar venta sin persistir
    [Documentation]    Descarta la venta cargada sin crear registros ni modificar stock o caja.
    [Tags]    XG-VEN-002
    Ingresar Como QA
    Preparar Venta Basica
    Cancelar Venta Basica
    Verificar Cancelacion Sin Persistencia
    Capturar Evidencia QA
