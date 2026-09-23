*** Settings ***
Documentation    Recorridos de ofertas con datos fijos y validación real pendiente.
Library          products.xgestion.offer_journeys.library.XGestionOfferJourneysLibrary
Test Teardown    Finalizar Recorrido De Ofertas
Test Tags       xgestion    regression    promociones    promociones-condiciones    cobros    escritura


*** Test Cases ***
XG-PRM-073 Aplicar una oferta configurada para todas las formas de pago
    [Documentation]    3 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-073
    Ejecutar Recorrido De Ofertas    XG-PRM-073

XG-PRM-074 Aplicar una oferta exclusiva de efectivo y rechazar otros medios
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-074
    Ejecutar Recorrido De Ofertas    XG-PRM-074

XG-PRM-075 Aplicar una oferta a varios medios seleccionados y excluir otro
    [Documentation]    3 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-075
    Ejecutar Recorrido De Ofertas    XG-PRM-075

XG-PRM-076 Recalcular la promoción al cambiar de medio y retomar el cobro
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    recuperacion    XG-PRM-076
    Ejecutar Recorrido De Ofertas    XG-PRM-076
