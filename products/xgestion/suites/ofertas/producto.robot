*** Settings ***
Documentation    Recorridos de ofertas con datos fijos y validación real pendiente.
Library          products.xgestion.offer_journeys.library.XGestionOfferJourneysLibrary
Test Teardown    Finalizar Recorrido De Ofertas
Test Tags       xgestion    regression    promociones    promociones-alcances    ofertas-producto    escritura


*** Test Cases ***
XG-PRM-008 Aplicar el 10 % desde dos unidades por producto
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-008
    Ejecutar Recorrido De Ofertas    XG-PRM-008

XG-PRM-009 Descontar $150 por unidad desde dos unidades por producto
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-009
    Ejecutar Recorrido De Ofertas    XG-PRM-009

XG-PRM-010 Cobrar a $800 la unidad desde dos unidades por producto
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-010
    Ejecutar Recorrido De Ofertas    XG-PRM-010
