*** Settings ***
Documentation    Circuitos P0 de venta USD, recepción y cierre. Validación real pendiente.
Library          products.xgestion.circuits.library.XGestionCircuitsLibrary
Test Teardown    Finalizar Circuito Comercial
Test Tags        xgestion    regression    circuitos-completos    conciliacion    stock    p0    escritura


*** Test Cases ***
XG-FIN-011 Vender productos USD y conciliar stock y Libro Diario
    [Documentation]    Cancelar y retomar cobro ARS con vuelto; comprobar una sola venta.
    [Tags]    libro-diario    caja    XG-FIN-011
    Ejecutar Circuito Comercial    XG-FIN-011

XG-FIN-013 Recibir remito mixto actualizar costos y vender
    [Documentation]    Cuatro productos ARS/USD fijos/calculados; deuda y recepción única.
    [Tags]    remitos    XG-FIN-013
    Ejecutar Circuito Comercial    XG-FIN-013

XG-FIN-014 Cerrar turno con venta USD cobrada en ARS
    [Documentation]    Apertura sin fondo, venta, cierre y consulta histórica sin duplicaciones.
    [Tags]    caja    libro-diario    XG-FIN-014
    Ejecutar Circuito Comercial    XG-FIN-014
