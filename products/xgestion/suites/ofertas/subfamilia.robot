*** Settings ***
Documentation    Recorridos de ofertas con datos fijos y validación real pendiente.
Library          products.xgestion.offer_journeys.library.XGestionOfferJourneysLibrary
Test Teardown    Finalizar Recorrido De Ofertas
Test Tags       xgestion    regression    promociones    promociones-alcances    ofertas-subfamilia    escritura


*** Test Cases ***
XG-PRM-018 Aplicar el 10 % por subfamilia
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-018
    Ejecutar Recorrido De Ofertas    XG-PRM-018

XG-PRM-019 Descontar $150 por unidad por subfamilia
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-019
    Ejecutar Recorrido De Ofertas    XG-PRM-019

XG-PRM-020 Aplicar un 2x1 por subfamilia
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-020
    Ejecutar Recorrido De Ofertas    XG-PRM-020

XG-PRM-021 Aplicar la segunda unidad al 50 % por subfamilia
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-021
    Ejecutar Recorrido De Ofertas    XG-PRM-021

XG-PRM-022 Aplicar el 10 % desde dos unidades por subfamilia
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-022
    Ejecutar Recorrido De Ofertas    XG-PRM-022

XG-PRM-023 Descontar $150 por unidad desde dos unidades por subfamilia
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-023
    Ejecutar Recorrido De Ofertas    XG-PRM-023

XG-PRM-024 Cobrar a $800 la unidad desde dos unidades por subfamilia
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-024
    Ejecutar Recorrido De Ofertas    XG-PRM-024
