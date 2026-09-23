*** Settings ***
Documentation    Recorridos de ofertas con datos fijos y validación real pendiente.
Library          products.xgestion.offer_journeys.library.XGestionOfferJourneysLibrary
Test Teardown    Finalizar Recorrido De Ofertas
Test Tags       xgestion    regression    promociones    promociones-alcances    ofertas-familia    escritura


*** Test Cases ***
XG-PRM-011 Aplicar el 10 % por familia
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-011
    Ejecutar Recorrido De Ofertas    XG-PRM-011

XG-PRM-012 Descontar $150 por unidad por familia
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-012
    Ejecutar Recorrido De Ofertas    XG-PRM-012

XG-PRM-013 Aplicar un 2x1 por familia
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-013
    Ejecutar Recorrido De Ofertas    XG-PRM-013

XG-PRM-014 Aplicar la segunda unidad al 50 % por familia
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-014
    Ejecutar Recorrido De Ofertas    XG-PRM-014

XG-PRM-015 Aplicar el 10 % desde dos unidades por familia
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-015
    Ejecutar Recorrido De Ofertas    XG-PRM-015

XG-PRM-016 Descontar $150 por unidad desde dos unidades por familia
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-016
    Ejecutar Recorrido De Ofertas    XG-PRM-016

XG-PRM-017 Cobrar a $800 la unidad desde dos unidades por familia
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-017
    Ejecutar Recorrido De Ofertas    XG-PRM-017
