*** Settings ***
Documentation    Atajos de 13 listados con JAB y paquete QA privado verificado.
Library    products.xgestion.keyboard_lists.KeyboardListsLibrary
Test Setup    Iniciar XGestion QA    atajos-listados-v1
Test Teardown    Cerrar XGestion QA
Test Tags    xgestion    regression    atajos-listados    lectura


*** Test Cases ***
XG-KEY-001 Atajos en cuentas corrientes de clientes
    [Documentation]    Foco, filas, Enter, identidad, búsqueda, orden, permisos y filtros según matriz KEY.
    [Tags]    XG-KEY-001    p0    filtros-listados
    Ingresar Como QA
    Ejecutar Atajos Del Listado    XG-KEY-001

XG-KEY-002 Atajos en cuenta corriente de cliente
    [Documentation]    Foco, filas, Enter, identidad, búsqueda, orden, permisos y filtros según matriz KEY.
    [Tags]    XG-KEY-002    p0    filtros-listados
    Ingresar Como QA
    Ejecutar Atajos Del Listado    XG-KEY-002

XG-KEY-003 Atajos en cuentas corrientes de proveedores
    [Documentation]    Foco, filas, Enter, identidad, búsqueda, orden, permisos y filtros según matriz KEY.
    [Tags]    XG-KEY-003    p0    filtros-listados
    Ingresar Como QA
    Ejecutar Atajos Del Listado    XG-KEY-003

XG-KEY-004 Atajos en cuenta corriente de proveedor
    [Documentation]    Foco, filas, Enter, identidad, búsqueda, orden, permisos y filtros según matriz KEY.
    [Tags]    XG-KEY-004    p0    filtros-listados
    Ingresar Como QA
    Ejecutar Atajos Del Listado    XG-KEY-004

XG-KEY-005 Atajos en clientes
    [Documentation]    Foco, filas, Enter, identidad, búsqueda, orden, permisos y filtros según matriz KEY.
    [Tags]    XG-KEY-005    p1
    Ingresar Como QA
    Ejecutar Atajos Del Listado    XG-KEY-005

XG-KEY-006 Atajos en productos
    [Documentation]    Foco, filas, Enter, identidad, búsqueda, orden, permisos y filtros según matriz KEY.
    [Tags]    XG-KEY-006    p1    filtros-listados
    Ingresar Como QA
    Ejecutar Atajos Del Listado    XG-KEY-006

XG-KEY-007 Atajos en mesas
    [Documentation]    Foco, filas, Enter, identidad, búsqueda, orden, permisos y filtros según matriz KEY.
    [Tags]    XG-KEY-007    p1    filtros-listados
    Ingresar Como QA
    Ejecutar Atajos Del Listado    XG-KEY-007

XG-KEY-008 Atajos en usuarios
    [Documentation]    Foco, filas, Enter, identidad, búsqueda, orden, permisos y filtros según matriz KEY.
    [Tags]    XG-KEY-008    p1
    Ingresar Como QA
    Ejecutar Atajos Del Listado    XG-KEY-008

XG-KEY-009 Atajos en turnos
    [Documentation]    Foco, filas, Enter, identidad, búsqueda, orden, permisos y filtros según matriz KEY.
    [Tags]    XG-KEY-009    p1
    Ingresar Como QA
    Ejecutar Atajos Del Listado    XG-KEY-009

XG-KEY-010 Atajos en compras
    [Documentation]    Foco, filas, Enter, identidad, búsqueda, orden, permisos y filtros según matriz KEY.
    [Tags]    XG-KEY-010    p0    filtros-listados
    Ingresar Como QA
    Ejecutar Atajos Del Listado    XG-KEY-010

XG-KEY-011 Atajos en proveedores
    [Documentation]    Foco, filas, Enter, identidad, búsqueda, orden, permisos y filtros según matriz KEY.
    [Tags]    XG-KEY-011    p1
    Ingresar Como QA
    Ejecutar Atajos Del Listado    XG-KEY-011

XG-KEY-012 Atajos en categorías
    [Documentation]    Foco, filas, Enter, identidad, búsqueda, orden, permisos y filtros según matriz KEY.
    [Tags]    XG-KEY-012    p1
    Ingresar Como QA
    Ejecutar Atajos Del Listado    XG-KEY-012

XG-KEY-013 Atajos en subcategorías
    [Documentation]    Foco, filas, Enter, identidad, búsqueda, orden, permisos y filtros según matriz KEY.
    [Tags]    XG-KEY-013    p1    filtros-listados
    Ingresar Como QA
    Ejecutar Atajos Del Listado    XG-KEY-013
