*** Settings ***
Documentation    Recorridos de ofertas con datos fijos y validación real pendiente.
Library          products.xgestion.offer_journeys.library.XGestionOfferJourneysLibrary
Test Teardown    Finalizar Recorrido De Ofertas
Test Tags       xgestion    regression    promociones    promociones-agrupadas    escritura


*** Test Cases ***
XG-PRM-039 Agrupar por familia: 10 % entre productos
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-familia    XG-PRM-039
    Ejecutar Recorrido De Ofertas    XG-PRM-039

XG-PRM-040 Agrupar por familia: descuento de $150 por unidad entre productos
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-familia    XG-PRM-040
    Ejecutar Recorrido De Ofertas    XG-PRM-040

XG-PRM-041 Agrupar por familia: 3x2 entre productos
    [Documentation]    3 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-familia    XG-PRM-041
    Ejecutar Recorrido De Ofertas    XG-PRM-041

XG-PRM-042 Agrupar por familia: segunda unidad al 50 % entre productos
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-familia    XG-PRM-042
    Ejecutar Recorrido De Ofertas    XG-PRM-042

XG-PRM-043 Agrupar por familia: 10 % desde dos unidades combinadas
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-familia    XG-PRM-043
    Ejecutar Recorrido De Ofertas    XG-PRM-043

XG-PRM-044 Agrupar por familia: $150 por unidad desde dos unidades combinadas
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-familia    XG-PRM-044
    Ejecutar Recorrido De Ofertas    XG-PRM-044

XG-PRM-045 Agrupar por familia: precio de $800 desde dos unidades combinadas
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-familia    XG-PRM-045
    Ejecutar Recorrido De Ofertas    XG-PRM-045

XG-PRM-046 Agrupar por subfamilia: 10 % entre productos
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-subfamilia    XG-PRM-046
    Ejecutar Recorrido De Ofertas    XG-PRM-046

XG-PRM-047 Agrupar por subfamilia: descuento de $150 por unidad entre productos
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-subfamilia    XG-PRM-047
    Ejecutar Recorrido De Ofertas    XG-PRM-047

XG-PRM-048 Agrupar por subfamilia: 3x2 entre productos
    [Documentation]    3 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-subfamilia    XG-PRM-048
    Ejecutar Recorrido De Ofertas    XG-PRM-048

XG-PRM-049 Agrupar por subfamilia: segunda unidad al 50 % entre productos
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-subfamilia    XG-PRM-049
    Ejecutar Recorrido De Ofertas    XG-PRM-049

XG-PRM-050 Agrupar por subfamilia: 10 % desde dos unidades combinadas
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-subfamilia    XG-PRM-050
    Ejecutar Recorrido De Ofertas    XG-PRM-050

XG-PRM-051 Agrupar por subfamilia: $150 por unidad desde dos unidades combinadas
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-subfamilia    XG-PRM-051
    Ejecutar Recorrido De Ofertas    XG-PRM-051

XG-PRM-052 Agrupar por subfamilia: precio de $800 desde dos unidades combinadas
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-subfamilia    XG-PRM-052
    Ejecutar Recorrido De Ofertas    XG-PRM-052

XG-PRM-053 Agrupar por marca: 10 % entre productos
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-marca    XG-PRM-053
    Ejecutar Recorrido De Ofertas    XG-PRM-053

XG-PRM-054 Agrupar por marca: descuento de $150 por unidad entre productos
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-marca    XG-PRM-054
    Ejecutar Recorrido De Ofertas    XG-PRM-054

XG-PRM-055 Agrupar por marca: 3x2 entre productos
    [Documentation]    3 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-marca    XG-PRM-055
    Ejecutar Recorrido De Ofertas    XG-PRM-055

XG-PRM-056 Agrupar por marca: segunda unidad al 50 % entre productos
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-marca    XG-PRM-056
    Ejecutar Recorrido De Ofertas    XG-PRM-056

XG-PRM-057 Agrupar por marca: 10 % desde dos unidades combinadas
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-marca    XG-PRM-057
    Ejecutar Recorrido De Ofertas    XG-PRM-057

XG-PRM-058 Agrupar por marca: $150 por unidad desde dos unidades combinadas
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-marca    XG-PRM-058
    Ejecutar Recorrido De Ofertas    XG-PRM-058

XG-PRM-059 Agrupar por marca: precio de $800 desde dos unidades combinadas
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-marca    XG-PRM-059
    Ejecutar Recorrido De Ofertas    XG-PRM-059
