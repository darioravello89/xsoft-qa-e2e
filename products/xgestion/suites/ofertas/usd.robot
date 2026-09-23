*** Settings ***
Documentation    Recorridos de ofertas con datos fijos y validación real pendiente.
Library          products.xgestion.offer_journeys.library.XGestionOfferJourneysLibrary
Test Teardown    Finalizar Recorrido De Ofertas
Test Tags       xgestion    regression    promociones    promociones-alcances    ofertas-usd    p0    escritura


*** Test Cases ***
XG-PRM-080 Cobrar precio final USD 50 por producto
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-producto    XG-PRM-080
    Ejecutar Recorrido De Ofertas    XG-PRM-080

XG-PRM-081 Cobrar precio final USD 50 por familia
    [Documentation]    3 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-familia    XG-PRM-081
    Ejecutar Recorrido De Ofertas    XG-PRM-081

XG-PRM-082 Cobrar precio final USD 50 por subfamilia
    [Documentation]    3 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-subfamilia    XG-PRM-082
    Ejecutar Recorrido De Ofertas    XG-PRM-082

XG-PRM-083 Cobrar precio final USD 50 por marca
    [Documentation]    3 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-marca    XG-PRM-083
    Ejecutar Recorrido De Ofertas    XG-PRM-083

XG-PRM-084 Cobrar precio final USD 50 por sector
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-sector    XG-PRM-084
    Ejecutar Recorrido De Ofertas    XG-PRM-084
