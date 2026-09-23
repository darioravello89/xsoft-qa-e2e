*** Settings ***
Documentation    Recorridos de ofertas con datos fijos y validación real pendiente.
Library          products.xgestion.offer_journeys.library.XGestionOfferJourneysLibrary
Test Teardown    Finalizar Recorrido De Ofertas
Test Tags       xgestion    regression    promociones    promociones-alcances    ofertas-marca    escritura


*** Test Cases ***
XG-PRM-025 Aplicar el 10 % por marca
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-025
    Ejecutar Recorrido De Ofertas    XG-PRM-025

XG-PRM-026 Descontar $150 por unidad por marca
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-026
    Ejecutar Recorrido De Ofertas    XG-PRM-026

XG-PRM-027 Aplicar un 2x1 por marca
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-027
    Ejecutar Recorrido De Ofertas    XG-PRM-027

XG-PRM-028 Aplicar la segunda unidad al 50 % por marca
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-028
    Ejecutar Recorrido De Ofertas    XG-PRM-028

XG-PRM-029 Aplicar el 10 % desde dos unidades por marca
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-029
    Ejecutar Recorrido De Ofertas    XG-PRM-029

XG-PRM-030 Descontar $150 por unidad desde dos unidades por marca
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-030
    Ejecutar Recorrido De Ofertas    XG-PRM-030

XG-PRM-031 Cobrar a $800 la unidad desde dos unidades por marca
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-031
    Ejecutar Recorrido De Ofertas    XG-PRM-031
