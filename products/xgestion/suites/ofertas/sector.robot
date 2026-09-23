*** Settings ***
Documentation    Recorridos de ofertas con datos fijos y validación real pendiente.
Library          products.xgestion.offer_journeys.library.XGestionOfferJourneysLibrary
Test Teardown    Finalizar Recorrido De Ofertas
Test Tags       xgestion    regression    promociones    promociones-alcances    ofertas-sector    escritura


*** Test Cases ***
XG-PRM-032 Aplicar el 10 % por sector
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-032
    Ejecutar Recorrido De Ofertas    XG-PRM-032

XG-PRM-033 Descontar $150 por unidad por sector
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-033
    Ejecutar Recorrido De Ofertas    XG-PRM-033

XG-PRM-034 Aplicar un 2x1 por sector
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-034
    Ejecutar Recorrido De Ofertas    XG-PRM-034

XG-PRM-035 Aplicar la segunda unidad al 50 % por sector
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-035
    Ejecutar Recorrido De Ofertas    XG-PRM-035

XG-PRM-036 Aplicar el 10 % desde dos unidades por sector
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-036
    Ejecutar Recorrido De Ofertas    XG-PRM-036

XG-PRM-037 Descontar $150 por unidad desde dos unidades por sector
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-037
    Ejecutar Recorrido De Ofertas    XG-PRM-037

XG-PRM-038 Cobrar a $800 la unidad desde dos unidades por sector
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-038
    Ejecutar Recorrido De Ofertas    XG-PRM-038
