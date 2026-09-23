*** Settings ***
Documentation    Recorridos de ofertas con datos fijos y validación real pendiente.
Library          products.xgestion.offer_journeys.library.XGestionOfferJourneysLibrary
Test Teardown    Finalizar Recorrido De Ofertas
Test Tags       xgestion    regression    promociones    promociones-combos    escritura


*** Test Cases ***
XG-PRM-060 Completar un combo, quitar un componente y recuperar el beneficio
    [Documentation]    3 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-060
    Ejecutar Recorrido De Ofertas    XG-PRM-060

XG-PRM-061 Repetir combos y descontar solo los productos sobrantes
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-061
    Ejecutar Recorrido De Ofertas    XG-PRM-061

XG-PRM-062 Elegir entre combos que comparten productos y resolver un empate
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-062
    Ejecutar Recorrido De Ofertas    XG-PRM-062

XG-PRM-063 Conservar los centavos al distribuir el descuento de un combo
    [Documentation]    2 variantes; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-063
    Ejecutar Recorrido De Ofertas    XG-PRM-063

XG-PRM-064 Completar y repetir un combo con cantidades fraccionarias
    [Documentation]    1 variante; ver ficha y pasos exactos del catálogo.
    [Tags]    XG-PRM-064
    Ejecutar Recorrido De Ofertas    XG-PRM-064
