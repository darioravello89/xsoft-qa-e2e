*** Settings ***
Documentation    Recorridos de ofertas con datos fijos y validación real pendiente.
Library          products.xgestion.offer_journeys.library.XGestionOfferJourneysLibrary
Test Teardown    Finalizar Recorrido De Ofertas
Test Tags       xgestion    regression    promociones    promociones-condiciones    escritura


*** Test Cases ***
XG-PRM-065 Cobrar fracciones con una oferta sin cantidad mínima
    [Documentation]    3 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-producto    XG-PRM-065
    Ejecutar Recorrido De Ofertas    XG-PRM-065

XG-PRM-066 Aplicar una oferta fraccionable al alcanzar un kilo
    [Documentation]    3 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-producto    XG-PRM-066
    Ejecutar Recorrido De Ofertas    XG-PRM-066

XG-PRM-067 Respetar la prioridad entre ofertas de distintos alcances
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-producto    ofertas-familia    ofertas-subfamilia    ofertas-marca    ofertas-sector    XG-PRM-067
    Ejecutar Recorrido De Ofertas    XG-PRM-067

XG-PRM-068 Elegir la oferta elegible por cantidad y fecha dentro del mismo alcance
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    ofertas-producto    XG-PRM-068
    Ejecutar Recorrido De Ofertas    XG-PRM-068

XG-PRM-069 Aplicar la oferta el primer y el último día de vigencia
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-069
    Ejecutar Recorrido De Ofertas    XG-PRM-069

XG-PRM-070 Revisar una oferta activa y desactivada entre ventas nuevas
    [Documentation]    3 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-070
    Ejecutar Recorrido De Ofertas    XG-PRM-070

XG-PRM-071 Calcular la oferta sobre el precio de la lista seleccionada
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    precios    XG-PRM-071
    Ejecutar Recorrido De Ofertas    XG-PRM-071

XG-PRM-072 Cambiar de lista y recuperar el precio de un producto sin entrada en ella
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    precios    recuperacion    XG-PRM-072
    Ejecutar Recorrido De Ofertas    XG-PRM-072

XG-PRM-079 Permitir o rechazar el descuento manual sobre artículos en oferta
    [Documentation]    4 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    descuentos    permisos    XG-PRM-079
    Ejecutar Recorrido De Ofertas    XG-PRM-079
