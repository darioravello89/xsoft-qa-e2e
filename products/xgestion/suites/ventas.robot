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

XG-VEN-003 Modificar cantidad de producto cargado
    [Documentation]    Edita la cantidad del renglón existente y verifica precio, cantidad, subtotal y total.
    [Tags]    XG-VEN-003    carga-productos    corregir-venta
    [Setup]    Iniciar XGestion QA    ventas-etapa1
    Ingresar Como QA
    Preparar Venta De Una Unidad
    Modificar Cantidad Del Producto Cargado
    Cancelar Venta Basica
    Verificar Cancelacion Sin Persistencia
    Capturar Evidencia QA

XG-VEN-004 Codigo inexistente conserva la venta
    [Documentation]    Rechaza un código, conserva lo cargado y permite continuar con otro producto válido.
    [Tags]    XG-VEN-004    carga-productos
    [Setup]    Iniciar XGestion QA    ventas-etapa1
    Ingresar Como QA
    Preparar Venta De Una Unidad
    Rechazar Codigo Inexistente Y Continuar
    Cancelar Venta Basica
    Verificar Cancelacion Sin Persistencia
    Capturar Evidencia QA

XG-VEN-005 Efectivo con vuelto
    [Documentation]    Cobra 2000 ARS con 3000 recibidos y 1000 de vuelto, una sola vez.
    [Tags]    XG-VEN-005    efectivo
    [Setup]    Iniciar XGestion QA    ventas-etapa1
    Ingresar Como QA
    Preparar Venta Basica
    Cobrar En Efectivo Con Vuelto
    Verificar Venta Persistida
    Capturar Evidencia QA

XG-VEN-006 Cancelar cobro y retomarlo
    [Documentation]    Cancela el diálogo conservando la venta y luego confirma un único cobro.
    [Tags]    XG-VEN-006    efectivo    cobros
    [Setup]    Iniciar XGestion QA    ventas-etapa1
    Ingresar Como QA
    Preparar Venta Basica
    Cancelar Cobro Conservando La Venta
    Cobrar Venta En Efectivo
    Verificar Venta Persistida
    Capturar Evidencia QA

XG-VEN-007 Rechazar abandono y continuar vendiendo
    [Documentation]    Rechaza abandonar, conserva la venta y permite editar cantidad antes de cobrar una sola vez.
    [Tags]    XG-VEN-007    corregir-venta
    [Setup]    Iniciar XGestion QA    ventas-etapa1
    Ingresar Como QA
    Preparar Venta De Una Unidad
    Rechazar Abandono Conservando La Venta
    Modificar Cantidad Del Producto Cargado
    Cobrar Venta En Efectivo
    Verificar Venta Persistida
    Capturar Evidencia QA

XG-VEN-008 Otra venta despues de cobrar
    [Documentation]    Comprueba el reinicio de la misma ventana y abandona otra venta sin afectar el primer cobro.
    [Tags]    XG-VEN-008
    [Setup]    Iniciar XGestion QA    ventas-etapa1
    Ingresar Como QA
    Preparar Venta Basica
    Cobrar Venta En Efectivo
    Verificar Venta Persistida
    Continuar Con Otra Venta Despues Del Cobro
    Agregar Una Unidad A La Venta
    Cancelar Venta Basica
    Verificar Que Solo Persiste La Primera Venta
    Capturar Evidencia QA

XG-VEN-009 Otra venta despues de abandonar
    [Documentation]    Abandona, abre otra venta en la misma sesión y confirma que no quedan ventas ni movimientos.
    [Tags]    XG-VEN-009
    [Setup]    Iniciar XGestion QA    ventas-etapa1
    Ingresar Como QA
    Preparar Venta Basica
    Cancelar Venta Basica
    Verificar Cancelacion Sin Persistencia
    Continuar Con Otra Venta Despues Del Abandono
    Agregar Una Unidad A La Venta
    Cancelar Venta Basica
    Verificar Cancelacion Sin Persistencia
    Capturar Evidencia QA
