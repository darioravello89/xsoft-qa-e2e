*** Settings ***
Documentation    Promociones ARS: recálculo, cancelación de cobro y una venta no fiscal persistida.
Library          products.xgestion.promotions_library.XGestionPromotionsLibrary
Test Teardown    Cerrar XGestion QA
Test Tags        xgestion    regression    promociones    escritura


*** Test Cases ***
XG-PRM-001 Aplicar una promoción porcentual y recalcular la cantidad
    [Documentation]    PCT-Q3: cantidad 1 a 3, neto 900 a 2.700 ARS y un único cobro.
    [Tags]    XG-PRM-001
    [Setup]    Iniciar Promociones QA    PCT-Q3
    Ingresar Como QA
    Preparar Venta Con Promocion
    Modificar Cantidad Con Promocion
    Cancelar Cobro De Promocion
    Cobrar Promocion En Efectivo
    Verificar Venta Persistida
    Capturar Evidencia QA

XG-PRM-002 Aplicar un descuento de importe fijo y recalcular la cantidad
    [Documentation]    IMP-Q3: cantidad 1 a 3, neto 850 a 2.550 ARS y un único cobro.
    [Tags]    XG-PRM-002
    [Setup]    Iniciar Promociones QA    IMP-Q3
    Ingresar Como QA
    Preparar Venta Con Promocion
    Modificar Cantidad Con Promocion
    Cancelar Cobro De Promocion
    Cobrar Promocion En Efectivo
    Verificar Venta Persistida
    Capturar Evidencia QA

XG-PRM-003 Recalcular una promoción 2x1 al pasar de una a tres unidades
    [Documentation]    2X1-Q3: cantidad 1 a 3, neto 1.000 a 2.000 ARS y un único cobro.
    [Tags]    XG-PRM-003
    [Setup]    Iniciar Promociones QA    2X1-Q3
    Ingresar Como QA
    Preparar Venta Con Promocion
    Modificar Cantidad Con Promocion
    Cancelar Cobro De Promocion
    Cobrar Promocion En Efectivo
    Verificar Venta Persistida
    Capturar Evidencia QA

XG-PRM-004 Recalcular el descuento del 50 % en la segunda unidad
    [Documentation]    2DA50-Q3: cantidad 1 a 3, neto 1.000 a 2.500 ARS y un único cobro.
    [Tags]    XG-PRM-004
    [Setup]    Iniciar Promociones QA    2DA50-Q3
    Ingresar Como QA
    Preparar Venta Con Promocion
    Modificar Cantidad Con Promocion
    Cancelar Cobro De Promocion
    Cobrar Promocion En Efectivo
    Verificar Venta Persistida
    Capturar Evidencia QA

XG-PRM-005 Conservar el precio normal cuando la promoción está vencida
    [Documentation]    EXPIRADA: cantidad 2 a 1, neto 2.000 a 1.000 ARS y un único cobro.
    [Tags]    XG-PRM-005
    [Setup]    Iniciar Promociones QA    EXPIRADA
    Ingresar Como QA
    Preparar Venta Con Promocion
    Modificar Cantidad Con Promocion
    Cancelar Cobro De Promocion
    Cobrar Promocion En Efectivo
    Verificar Venta Persistida
    Capturar Evidencia QA

XG-PRM-006 Conservar el precio normal antes del inicio de una promoción
    [Documentation]    FUTURA: cantidad 2 a 1, neto 2.000 a 1.000 ARS y un único cobro.
    [Tags]    XG-PRM-006
    [Setup]    Iniciar Promociones QA    FUTURA
    Ingresar Como QA
    Preparar Venta Con Promocion
    Modificar Cantidad Con Promocion
    Cancelar Cobro De Promocion
    Cobrar Promocion En Efectivo
    Verificar Venta Persistida
    Capturar Evidencia QA

XG-PRM-007 Conservar el precio normal cuando la promoción está desactivada
    [Documentation]    INACTIVA: cantidad 2 a 1, neto 2.000 a 1.000 ARS y un único cobro.
    [Tags]    XG-PRM-007
    [Setup]    Iniciar Promociones QA    INACTIVA
    Ingresar Como QA
    Preparar Venta Con Promocion
    Modificar Cantidad Con Promocion
    Cancelar Cobro De Promocion
    Cobrar Promocion En Efectivo
    Verificar Venta Persistida
    Capturar Evidencia QA
