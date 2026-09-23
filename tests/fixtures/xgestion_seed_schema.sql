-- Esquema de referencia sintetico sin triggers/integraciones ni credenciales.
-- Version: xgestion-seed-schema-v1, objetivo MySQL 5.7.44 / InnoDB.
-- Fuente: XGestion2 release/189-lts, f34238183d494259bed1279dd7d9aac0ce16a3ae.
-- Tablas copiadas de DATABASE_SCHEMA.sql; ajustes al final respaldados por
-- src/ModuloPrincipal/Entidades/VerificadorDeBaseDeDatos.java y
-- src/Utilidades/Constantes.java del mismo commit.
-- Solo estructura: sin INSERT, datos privados, triggers, funciones, vistas,
-- eventos, usuarios SQL, privilegios ni instrucciones CREATE/DROP DATABASE.
-- Se carga exclusivamente en un esquema EFIMERO creado por tests; no es una
-- migracion del ERP ni el dump privado del paquete QA. No usar en una base real.
-- Las pruebas agregan por separado sus datos sinteticos de contexto/globales.
-- Normalizacion lexical: utf8mb3 -> utf8 y utf8mb3_general_ci -> utf8_general_ci
-- (mismo repertorio de tres bytes; alias documentado por MySQL 5.7):
-- https://dev.mysql.com/doc/refman/5.7/en/charset-unicode-utf8.html
-- Las demas definiciones y restricciones del snapshot se conservan.


-- Fuente: DATABASE_SCHEMA.sql:147
CREATE TABLE `_empresa` (
  `idEmp` int(11) NOT NULL,
  `empNombreLegal` varchar(255) NOT NULL,
  `empNombreFantasia` varchar(255) DEFAULT '',
  `empDireccion` varchar(255) DEFAULT '',
  `empCuit` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT '',
  `empTelefono` varchar(255) DEFAULT '',
  `empEmail` varchar(255) DEFAULT '',
  `empCodPostal` varchar(255) DEFAULT '',
  `empCiudad` varchar(255) DEFAULT '',
  `empProvincia` varchar(255) DEFAULT '',
  `empLogoS` blob DEFAULT NULL COMMENT '25x25',
  `empLogoM` blob DEFAULT NULL COMMENT '100x100',
  `empLogoL` longblob DEFAULT NULL COMMENT '200x200',
  `empLogoXL` longblob DEFAULT NULL COMMENT '250x250',
  `empFechaValidez` varchar(255) DEFAULT NULL,
  `empFechaBackup` date DEFAULT NULL,
  `Fecha_Vencimiento_Soporte` date DEFAULT NULL,
  `Fecha_Vencimiento_Licencia` date DEFAULT NULL,
  `Fecha_Vencimiento_Servidor` date DEFAULT NULL,
  `activo` bit(1) DEFAULT b'1',
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(45) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(45) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  `Modulo_Ventas` bit(1) DEFAULT b'1',
  `Modulo_Productos` bit(1) DEFAULT b'1',
  `Modulo_Stocks` bit(1) DEFAULT b'1',
  `Modulo_Proveedores` bit(1) DEFAULT b'1',
  `Modulo_Finanzas` bit(1) DEFAULT b'1',
  `Modulo_Configuracion` bit(1) DEFAULT b'1',
  `Modulo_FacturaElectronica` bit(1) DEFAULT b'1',
  `Modulo_ImpresoraFiscal` bit(1) DEFAULT b'1',
  `Modulo_Servicios` bit(1) DEFAULT b'1',
  `Modulo_Sincronizacion` bit(1) DEFAULT b'1',
  `Modulo_Turnify` bit(1) DEFAULT b'0',
  `ID_TipoEmpresa` int(11) DEFAULT NULL,
  `IngresosBrutos` varchar(145) DEFAULT NULL,
  `FechaInicioActividades` date DEFAULT NULL,
  `Porcentaje_IngresosBrutos` decimal(10,2) DEFAULT NULL,
  `CotizacionDolar` decimal(10,2) DEFAULT NULL,
  `Modulo_Restobar` bit(1) NOT NULL DEFAULT b'0',
  `Empresa` varchar(255) DEFAULT NULL,
  `backgroundImage` varchar(500) DEFAULT NULL,
  `primaryColor` varchar(7) DEFAULT '',
  `secondaryColor` varchar(7) DEFAULT '',
  `minutosPorTurno` int(11) DEFAULT 0,
  `redondeo` decimal(10,2) DEFAULT 0.00,
  `Configuracion` varchar(5000) DEFAULT '',
  PRIMARY KEY (`idEmp`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:318
CREATE TABLE `_sucursales` (
  `Empresa` int(11) NOT NULL,
  `Empresa_Nombre` varchar(250) DEFAULT NULL,
  `sucId` int(11) NOT NULL,
  `sucNombre` varchar(255) DEFAULT '',
  `sucDireccion` varchar(255) DEFAULT '',
  `sucTelefono` varchar(255) DEFAULT '',
  `sucUbicacion` varchar(255) DEFAULT '',
  `activo` bit(1) DEFAULT b'1',
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(50) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(50) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  `mp_store_id` int(11) DEFAULT 0,
  `mp_external_id` varchar(255) DEFAULT NULL,
  `mp_name` varchar(255) DEFAULT NULL,
  `mp_location_street_number` varchar(255) DEFAULT NULL,
  `mp_location_street_name` varchar(255) DEFAULT NULL,
  `mp_location_city_name` varchar(255) DEFAULT NULL,
  `mp_location_state_name` varchar(255) DEFAULT NULL,
  `mp_location_latitude` varchar(255) DEFAULT NULL,
  `mp_location_longitude` varchar(255) DEFAULT NULL,
  `mp_reference` varchar(255) DEFAULT NULL,
  `ID_Provincia` int(11) DEFAULT 1,
  PRIMARY KEY (`Empresa`,`sucId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:99
CREATE TABLE `_computadoras` (
  `Empresa` int(11) NOT NULL,
  `Empresa_Nombre` varchar(250) DEFAULT NULL,
  `Sucursal` int(11) NOT NULL,
  `Sucursal_Nombre` varchar(45) DEFAULT NULL,
  `cpuId` int(11) NOT NULL,
  `cpuNombre` varchar(255) DEFAULT '',
  `cpuConfig` varchar(2000) DEFAULT '',
  `activo` bit(1) DEFAULT b'1',
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(50) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(50) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  `mp_pos_id` int(11) DEFAULT 0,
  `mp_external_id` varchar(255) DEFAULT NULL,
  `mp_fixed_amount` bit(1) DEFAULT b'0',
  `mp_name` varchar(255) DEFAULT NULL,
  `qr_url` varchar(500) DEFAULT NULL,
  `version` varchar(255) DEFAULT NULL,
  `intro_version` varchar(255) DEFAULT NULL,
  `licencia_utilizada` varchar(50) DEFAULT '',
  `Configuracion` varchar(5000) DEFAULT '',
  `ID_TipoAbono_Override` int(11) DEFAULT NULL,
  PRIMARY KEY (`Empresa`,`Sucursal`,`cpuId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:366
CREATE TABLE `_usuarios` (
  `Empresa` int(11) NOT NULL,
  `Empresa_Nombre` varchar(250) DEFAULT NULL,
  `usuId` int(11) NOT NULL DEFAULT 0,
  `usuUsuario` varchar(255) NOT NULL DEFAULT '',
  `usuPassword` varchar(255) NOT NULL DEFAULT '',
  `usuNombreCompleto` varchar(255) DEFAULT '',
  `usuTipo` int(11) DEFAULT 1,
  `usuTipoNombre` varchar(255) DEFAULT '',
  `activo` bit(1) NOT NULL DEFAULT b'1',
  `usuVentas` bit(1) DEFAULT b'0',
  `usuMercaderia` bit(1) DEFAULT b'0',
  `usuFinanzas` bit(1) DEFAULT b'0',
  `usuInformes` bit(1) DEFAULT b'0',
  `usuConfiguracion` bit(1) DEFAULT b'0',
  `usuVentasVentas` bit(1) DEFAULT b'0',
  `usuVentasCaja` bit(1) DEFAULT b'0',
  `usuMercaderiaCompras` bit(1) DEFAULT b'0',
  `usuMercaderiaAjustesStock` bit(1) DEFAULT b'0',
  `usuMercaderiaListadoStocks` bit(1) DEFAULT b'0',
  `usuMercaderiaCierreAnual` bit(1) DEFAULT b'0',
  `usuFinanzasLibroDiario` bit(1) DEFAULT b'0',
  `usuFinanzasCtaCteProveedores` bit(1) DEFAULT b'0',
  `usuFinanzasCtaCteClientes` bit(1) DEFAULT b'0',
  `usuFinanzasOfertas` bit(1) DEFAULT b'0',
  `usuFinanzasFormasDePago` bit(1) DEFAULT b'0',
  `usuFinanzasListaPrecios` bit(1) DEFAULT b'0',
  `usuFinanzasPreciosEnMasa` bit(1) DEFAULT b'0',
  `usuInformesMercaderia` bit(1) DEFAULT b'0',
  `usuInformesVentas` bit(1) DEFAULT b'0',
  `usuInformesFinanzas` bit(1) DEFAULT b'0',
  `usuInformesOtros` bit(1) DEFAULT b'0',
  `usuConfiguracionClientes` bit(1) DEFAULT b'0',
  `usuConfiguracionProductos` bit(1) DEFAULT b'0',
  `usuConfiguracionUsuarios` bit(1) DEFAULT b'0',
  `usuConfiguracionTurnos` bit(1) DEFAULT b'0',
  `usuConfiguracionBackup` bit(1) DEFAULT b'0',
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(50) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(50) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  `usuModuloProveedores` bit(1) DEFAULT b'1',
  `usuModuloStocks` bit(1) DEFAULT b'1',
  `usuListadoDeVentas` bit(1) DEFAULT b'1',
  `usuConfiguracionOpciones` bit(1) DEFAULT b'1',
  `usuConfiguracionSincronizar` bit(1) DEFAULT b'1',
  `usuConfiguracionMisDatos` bit(1) DEFAULT b'1',
  `usuPorcentajeComisionVentas` decimal(10,2) DEFAULT NULL,
  `ID_ListaPrecio` int(11) DEFAULT NULL,
  `MSCargarPedido` bit(1) DEFAULT b'1',
  `MSInformesStocks` bit(1) DEFAULT b'1',
  `MPvCrearPedido` bit(1) DEFAULT b'1',
  `MPvAgregarProveedor` bit(1) DEFAULT b'1',
  `MPvListadoDeProveedores` bit(1) DEFAULT b'1',
  `MPvCuentasCorrientesProveedores` bit(1) DEFAULT b'1',
  `MPvVencimientosDePagos` bit(1) DEFAULT b'1',
  `MPvVencimientosDeGastos` bit(1) DEFAULT b'1',
  `MPCategorias` bit(1) DEFAULT b'1',
  `MPAgregarProductoEnMasa` bit(1) DEFAULT b'1',
  `MPListadoDeProductos` bit(1) DEFAULT b'1',
  `usuProveedores` bit(1) DEFAULT b'1',
  `TarifaPorHora` decimal(10,3) DEFAULT 0.000,
  `ID_Turno` int(11) DEFAULT 0,
  `usuInformesProveedores` bit(1) DEFAULT b'1',
  `Permisos` varchar(2500) DEFAULT '',
  `ID_TipoUsuario` int(11) DEFAULT 1,
  `ID_Google` varchar(255) DEFAULT NULL,
  `Celular` varchar(255) DEFAULT NULL,
  `Ciudad` varchar(255) DEFAULT NULL,
  `Codigo_Postal` varchar(255) DEFAULT NULL,
  `Provincia` varchar(255) DEFAULT NULL,
  `idToken` varchar(255) DEFAULT NULL,
  `usuFoto` blob DEFAULT NULL,
  `ID_Xsoft` int(11) DEFAULT NULL,
  `ID_TipoUsuarioCliente` int(11) DEFAULT 1,
  PRIMARY KEY (`Empresa`,`usuId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:585
CREATE TABLE `articulos_ume` (
  `umeId` int(11) NOT NULL AUTO_INCREMENT,
  `umeNombre` varchar(2) DEFAULT '',
  `umeDescripcion` varchar(20) DEFAULT NULL,
  `umeDecimal` bit(1) DEFAULT b'0',
  PRIMARY KEY (`umeId`),
  UNIQUE KEY `mpUMEId` (`umeId`) USING BTREE,
  KEY `idx_articulos_ume_id` (`umeId`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:1649
CREATE TABLE `t_sis_moneda` (
  `ID_Moneda` int(11) NOT NULL AUTO_INCREMENT,
  `Nombre_Moneda` varchar(255) DEFAULT NULL,
  `Codigo_Afip` varchar(255) DEFAULT NULL,
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(255) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(255) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  PRIMARY KEY (`ID_Moneda`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:1634
CREATE TABLE `t_sis_iva` (
  `ID_Iva` int(11) NOT NULL,
  `Nombre_Iva` varchar(45) DEFAULT NULL,
  `PorcentajeIva` decimal(10,2) DEFAULT NULL,
  `fecha_insert` date DEFAULT NULL,
  `usuario_insert` varchar(45) DEFAULT NULL,
  `fecha_update` date DEFAULT NULL,
  `usuario_update` varchar(45) DEFAULT NULL,
  `fecha_sync` date DEFAULT NULL,
  PRIMARY KEY (`ID_Iva`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:203
CREATE TABLE `_familias` (
  `Empresa` int(11) NOT NULL,
  `Empresa_Nombre` varchar(250) DEFAULT NULL,
  `famId` int(11) NOT NULL,
  `famNombre` varchar(255) DEFAULT '',
  `activo` bit(1) NOT NULL DEFAULT b'1',
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(50) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(50) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  `famFoto` mediumblob DEFAULT NULL,
  `orden` int(11) DEFAULT 1,
  `EsParaCocina` bit(1) DEFAULT b'0',
  `ID_TiendaNube` varchar(255) DEFAULT '',
  `ID_PedidosYa` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Empresa`,`famId`),
  KEY `buscar_por_id_tiendanube` (`ID_TiendaNube`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:295
CREATE TABLE `_subfamilias` (
  `Empresa` int(11) NOT NULL,
  `Empresa_Nombre` varchar(250) DEFAULT NULL,
  `subId` int(11) NOT NULL,
  `subNombre` varchar(255) DEFAULT '',
  `famId` int(11) DEFAULT 1,
  `activo` bit(1) NOT NULL DEFAULT b'1',
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(50) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(50) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  `subFoto` mediumblob DEFAULT NULL,
  `orden` int(11) DEFAULT 1,
  `ID_TiendaNube` varchar(255) DEFAULT '',
  `ID_PedidosYa` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Empresa`,`subId`),
  KEY `buscar_por_id_tiendanube` (`ID_TiendaNube`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:349
CREATE TABLE `_ubicaciones` (
  `Empresa` int(11) NOT NULL,
  `Empresa_Nombre` varchar(250) DEFAULT NULL,
  `ubiId` int(11) NOT NULL,
  `ubiNombre` varchar(255) DEFAULT '',
  `activo` bit(1) NOT NULL DEFAULT b'1',
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(50) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(50) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  PRIMARY KEY (`Empresa`,`ubiId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:250
CREATE TABLE `_proveedores` (
  `Empresa` int(11) NOT NULL,
  `Empresa_Nombre` varchar(250) DEFAULT NULL,
  `proId` int(11) NOT NULL,
  `proCuit` varchar(255) DEFAULT '',
  `proNombre` varchar(255) DEFAULT '',
  `proContacto` varchar(255) DEFAULT '',
  `proTelefono` varchar(255) DEFAULT '',
  `proCelular` varchar(255) DEFAULT '',
  `proEmail` varchar(255) DEFAULT '',
  `proDireccion` varchar(255) DEFAULT '',
  `proFoto` longblob DEFAULT NULL,
  `activo` bit(1) DEFAULT b'1',
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(50) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(50) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  `ID_TipoResponsable` int(11) DEFAULT 1,
  `ID_TipoDocumento` int(11) DEFAULT 80,
  `ID_TipoEmpresa` int(11) DEFAULT 6,
  `ID_Provincia` int(11) DEFAULT 1,
  PRIMARY KEY (`Empresa`,`proId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:1896
CREATE TABLE `variantes` (
  `Empresa` int(11) NOT NULL DEFAULT 0,
  `ID_Variante` int(11) NOT NULL DEFAULT 0,
  `Nombre_Variante` varchar(55) DEFAULT '',
  `ID_TipoVariante` int(11) DEFAULT 0,
  `activo` bit(1) DEFAULT b'1',
  `fecha_insert` datetime DEFAULT '1990-01-01 00:00:00',
  `usuario_insert` varchar(55) DEFAULT '',
  `fecha_update` datetime DEFAULT '1990-01-01 00:00:00',
  `usuario_update` varchar(55) DEFAULT '',
  `fecha_sync` datetime DEFAULT '1990-01-01 00:00:00',
  PRIMARY KEY (`Empresa`,`ID_Variante`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Fuente: DATABASE_SCHEMA.sql:494
CREATE TABLE `articulos` (
  `Empresa` int(11) NOT NULL,
  `Empresa_Nombre` varchar(250) DEFAULT NULL,
  `artId` int(11) NOT NULL,
  `artCodigo` varchar(255) DEFAULT '',
  `artCodigoProveedor` varchar(255) DEFAULT '',
  `artNombre` varchar(255) DEFAULT NULL,
  `artDescripcion` varchar(2500) DEFAULT '',
  `artMarca` varchar(255) DEFAULT '',
  `artFamilia` int(11) DEFAULT 1,
  `artFamiliaNombre` varchar(255) DEFAULT '',
  `artSubfamilia` int(11) DEFAULT 1,
  `artSubfamiliaNombre` varchar(255) DEFAULT '',
  `artUbicacion` int(11) DEFAULT 1,
  `artUbicacionNombre` varchar(255) DEFAULT '',
  `artProveedor` int(11) DEFAULT 1,
  `artProveedorNombre` varchar(255) DEFAULT '',
  `artPrecioCosto` decimal(10,2) DEFAULT 0.00,
  `artPrecioVenta` decimal(10,2) DEFAULT 0.00,
  `artPrecioPorcentaje` decimal(10,2) DEFAULT 0.00,
  `artStock` decimal(10,3) DEFAULT 0.000,
  `artStockMinimo` decimal(10,3) DEFAULT 0.000,
  `artLoteHabitual` decimal(10,3) DEFAULT 0.000,
  `artEstado` int(11) DEFAULT 1,
  `artEstadoNombre` varchar(255) DEFAULT '',
  `artFoto` mediumblob DEFAULT NULL,
  `artUme` int(11) DEFAULT 1,
  `artStockeable` bit(1) DEFAULT b'1',
  `artContabilizable` bit(1) DEFAULT b'1',
  `artNumeroSerie` varchar(255) DEFAULT NULL,
  `artIngresoManual` bit(1) DEFAULT b'0',
  `artPrecioPorcentaje2` decimal(10,2) DEFAULT 0.00,
  `artPrecioVenta2` double(10,2) DEFAULT 0.00,
  `artNombreManual` bit(1) DEFAULT b'0',
  `activo` bit(1) NOT NULL DEFAULT b'1',
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(50) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(50) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  `ID_Iva` int(11) DEFAULT NULL,
  `ID_Moneda` int(11) DEFAULT NULL,
  `ImpuestoITC` decimal(10,2) DEFAULT NULL,
  `Ganancia` decimal(10,2) DEFAULT 0.00,
  `PrecioNeto` decimal(10,2) DEFAULT 0.00,
  `CantidadItc` decimal(10,2) DEFAULT 0.00,
  `CantidadImpuestos` decimal(10,2) DEFAULT 0.00,
  `CantidadIva` decimal(10,2) DEFAULT 0.00,
  `esPrecioCalculado` bit(1) DEFAULT b'1',
  `esPrecioCostoUniversal` bit(1) DEFAULT b'0',
  `Costo_Flete` decimal(14,2) DEFAULT 0.00,
  `orden` int(11) DEFAULT 0,
  `esProductoConOpciones` bit(1) DEFAULT b'0',
  `esMateriaPrima` bit(1) DEFAULT b'0',
  `balanza` varchar(255) DEFAULT '',
  `esOtrosImpuestosPorcentaje` bit(1) DEFAULT b'0',
  `ID_TipoTributoOtrosImpuestos` int(11) DEFAULT NULL,
  `Es_A_Cta_Orden_Proveedor` bit(1) DEFAULT b'0',
  `ID_Externo` varchar(255) DEFAULT '',
  `EsPrecioCostoCalculado` bit(1) DEFAULT b'0',
  `ID_TipoProducto` int(11) DEFAULT 1,
  `EsProductoConVariantes` bit(1) DEFAULT b'0',
  `ID_ProductoPadre` int(11) DEFAULT 0,
  `ID_Variante1` int(11) DEFAULT 0,
  `ID_Variante2` int(11) DEFAULT 0,
  `Configuracion` varchar(5000) DEFAULT '',
  `EsProductoConSubproductos` bit(1) DEFAULT b'0',
  `porcentaje` decimal(10,2) DEFAULT 0.00,
  `ImpuestoITC2` decimal(10,2) DEFAULT 0.00,
  `esOtrosImpuestosPorcentaje2` bit(1) DEFAULT b'0',
  `ID_TipoTributoOtrosImpuestos2` int(11) DEFAULT 0,
  `ID_TiendaNube` varchar(255) DEFAULT '',
  `ID_PedidosYa` varchar(255) DEFAULT '',
  `ID_Sucursales` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Empresa`,`artId`),
  KEY `BUSQUEDA` (`artCodigo`,`artProveedor`,`artUbicacion`,`artSubfamilia`,`artFamilia`,`artNombre`,`artDescripcion`(767),`artId`,`Empresa`) USING BTREE,
  KEY `idx_articulos_nombre` (`artNombre`),
  KEY `idx_articulos_id` (`artId`),
  KEY `idx_articulos_empresa_activo_nombre` (`Empresa`,`activo`,`artNombre`),
  KEY `idx_articulos_familia` (`artFamilia`),
  KEY `idx_articulos_subfamilia` (`artSubfamilia`),
  KEY `idx_articulos_proveedor` (`artProveedor`),
  KEY `idx_articulos_materiaprima` (`esMateriaPrima`),
  KEY `idx_articulos_ume` (`artUme`),
  KEY `buscar_por_id_tiendanube` (`ID_TiendaNube`) USING BTREE,
  KEY `buscar_por_id_pedidosya` (`ID_PedidosYa`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:1176
CREATE TABLE `productos_hijos` (
  `Empresa` int(11) NOT NULL,
  `Empresa_Nombre` varchar(250) DEFAULT NULL,
  `prhId` int(11) NOT NULL,
  `prhProducto` int(11) DEFAULT NULL,
  `prhProductoHijo` int(11) DEFAULT NULL,
  `prhCantidad` decimal(10,3) DEFAULT 10.000,
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(50) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(50) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  `activo` bit(1) DEFAULT b'1',
  PRIMARY KEY (`Empresa`,`prhId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

-- Fuente: DATABASE_SCHEMA.sql:1195
CREATE TABLE `productos_opciones` (
  `Empresa` varchar(45) NOT NULL DEFAULT '0',
  `ID_ProductoOpcion` int(11) NOT NULL DEFAULT 0,
  `ID_Producto` int(11) DEFAULT 0,
  `Opcion` varchar(45) DEFAULT '',
  `activo` bit(1) DEFAULT b'1',
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(45) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(45) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  `Foto` blob DEFAULT NULL,
  `Cantidad` decimal(10,3) DEFAULT 0.000,
  `Orden` int(11) DEFAULT 0,
  `ID_MateriaPrimaOrigen` int(11) DEFAULT 0,
  PRIMARY KEY (`Empresa`,`ID_ProductoOpcion`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:937
CREATE TABLE `movimientos_articulos` (
  `Empresa` int(11) NOT NULL,
  `Empresa_Nombre` varchar(145) DEFAULT NULL,
  `Sucursal` int(11) NOT NULL,
  `Sucursal_Nombre` varchar(250) DEFAULT NULL,
  `Computadora` int(11) NOT NULL DEFAULT 1,
  `Computadora_Nombre` varchar(255) DEFAULT '',
  `moaId` int(11) NOT NULL,
  `moaFechaHora` datetime DEFAULT NULL,
  `moaUsuario` int(11) DEFAULT 1,
  `moaUsuarioNombre` varchar(255) DEFAULT '',
  `moaArticuloCodigo` int(255) DEFAULT 0,
  `moaArticuloNombre` varchar(255) DEFAULT '',
  `moaStockActual` decimal(10,3) DEFAULT 0.000,
  `moaCantidad` decimal(10,3) DEFAULT 0.000,
  `moaStockFinal` decimal(10,3) DEFAULT 0.000,
  `moaNotas` varchar(255) DEFAULT '',
  `moaNumero` int(11) DEFAULT 0,
  `activo` bit(1) DEFAULT b'1',
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(50) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(50) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  PRIMARY KEY (`Empresa`,`Sucursal`,`Computadora`,`moaId`),
  KEY `busqueda_stock` (`Empresa`,`Sucursal`,`moaArticuloCodigo`,`activo`) USING BTREE,
  KEY `idx_movimientos_articulos_empresa_sucursal_fecha` (`Empresa`,`Sucursal`,`moaFechaHora`),
  KEY `idx_movimientos_articulos_codigo` (`moaArticuloCodigo`),
  KEY `idx_movimientos_articulos_activo` (`activo`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:1104
CREATE TABLE `ofertas` (
  `Empresa` int(11) NOT NULL,
  `Empresa_Nombre` varchar(250) DEFAULT NULL,
  `ofeId` int(11) NOT NULL,
  `ofeNombre` varchar(255) DEFAULT '',
  `ofeDesde` date DEFAULT NULL,
  `ofeHasta` date DEFAULT NULL,
  `ofeTipo` int(11) DEFAULT 1 COMMENT '1=Sector, 2=Familia, 3=Subfamilia, 4=Producto, 5=Marca, 6=Combo',
  `ofeTipoNombre` varchar(255) DEFAULT '',
  `ofeCodigo` varchar(255) DEFAULT '',
  `ofeCodigoNombre` varchar(255) DEFAULT '',
  `ofeDescuentoPorcentaje` decimal(10,2) DEFAULT 0.00,
  `activo` bit(1) NOT NULL DEFAULT b'1',
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(50) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(50) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  `TipoDescuento` varchar(10) DEFAULT NULL,
  `Sucursal` varchar(255) DEFAULT '',
  `ID_Pago` int(11) DEFAULT 0,
  `Lleva` int(11) DEFAULT 0,
  `Paga` decimal(18,2) DEFAULT 0.00,
  `Configuracion` varchar(5000) DEFAULT '',
  PRIMARY KEY (`Empresa`,`ofeId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Fuente: DATABASE_SCHEMA.sql:1410
CREATE TABLE `t_fin_listaprecio` (
  `Empresa` int(11) NOT NULL,
  `Sucursal` int(11) NOT NULL,
  `ID_ListaPrecio` int(11) NOT NULL,
  `ID_Proveedor` int(11) DEFAULT NULL,
  `Nombre_ListaPrecio` varchar(255) DEFAULT NULL,
  `activo` bit(1) DEFAULT b'1',
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(255) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(255) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  PRIMARY KEY (`Empresa`,`Sucursal`,`ID_ListaPrecio`),
  KEY `Empresa y Lista` (`Empresa`,`ID_ListaPrecio`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:1429
CREATE TABLE `t_fin_listapreciodetalle` (
  `Empresa` int(11) NOT NULL,
  `Sucursal` int(11) NOT NULL,
  `ID_ListaPrecioDetalle` int(11) NOT NULL,
  `ID_ListaPrecio` int(11) DEFAULT NULL,
  `ID_Producto` int(11) DEFAULT NULL,
  `Codigo_Proveedor` varchar(45) DEFAULT NULL,
  `PrecioCosto` decimal(10,3) NOT NULL DEFAULT 0.000,
  `CostoFlete` decimal(10,3) NOT NULL DEFAULT 0.000,
  `PorcentajeGanancia` decimal(10,3) NOT NULL DEFAULT 0.000,
  `ImporteGanancia` decimal(10,3) NOT NULL,
  `PorcentajeIva` decimal(10,3) NOT NULL,
  `ImporteIva` decimal(10,3) NOT NULL,
  `PrecioVenta` decimal(10,3) NOT NULL DEFAULT 0.000,
  `activo` bit(1) DEFAULT b'1',
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(255) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(255) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  `esPrecioCalculado` bit(1) NOT NULL DEFAULT b'1',
  `PrecioNeto` decimal(10,3) NOT NULL,
  `ID_Moneda` int(11) NOT NULL,
  PRIMARY KEY (`Empresa`,`Sucursal`,`ID_ListaPrecioDetalle`),
  UNIQUE KEY `un producto por lista` (`Empresa`,`ID_ListaPrecio`,`ID_Producto`),
  KEY `sincronizacion` (`Empresa`,`ID_ListaPrecioDetalle`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente: DATABASE_SCHEMA.sql:1159
CREATE TABLE `producto_codigo` (
  `Empresa` int(11) NOT NULL DEFAULT 0,
  `ID_ProductoCodigo` int(11) NOT NULL DEFAULT 0,
  `ID_Producto` int(11) NOT NULL DEFAULT 0,
  `Codigo` varchar(255) DEFAULT '',
  `activo` bit(1) DEFAULT b'1',
  `fecha_insert` datetime DEFAULT '1990-01-01 00:00:00',
  `usuario_insert` varchar(55) DEFAULT '',
  `fecha_update` datetime DEFAULT '1990-01-01 00:00:00',
  `usuario_update` varchar(55) DEFAULT '',
  PRIMARY KEY (`Empresa`,`ID_ProductoCodigo`),
  KEY `select_por_codigo` (`Empresa`,`Codigo`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Migraciones verificadas ausentes del snapshot historico.
-- Fuente 4b80ca6af137d1a7c06ac6d4545e1c08f9f21f1a: DATABASE_SCHEMA.sql:226-245.
CREATE TABLE `_pagos` (
  `Empresa` int(11) NOT NULL,
  `Empresa_Nombre` varchar(250) DEFAULT NULL,
  `pagId` int(11) NOT NULL,
  `pagNombre` varchar(255) DEFAULT '',
  `pagPorcentajeDescuento` decimal(10,2) DEFAULT 0.00,
  `activo` bit(1) DEFAULT b'1',
  `fecha_insert` datetime DEFAULT NULL,
  `usuario_insert` varchar(50) DEFAULT NULL,
  `fecha_update` datetime DEFAULT NULL,
  `usuario_update` varchar(50) DEFAULT NULL,
  `fecha_sync` datetime DEFAULT NULL,
  `ID_TipoPago` int(11) DEFAULT 1,
  `pagComisionMedioPago` decimal(10,2) DEFAULT 0.00,
  `Orden` int(11) DEFAULT 0,
  `ID_PedidosYa` varchar(255) DEFAULT NULL,
  `ID_TiendaNube` varchar(255) DEFAULT NULL,
  `Configuracion` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`Empresa`,`pagId`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- Fuente mismo commit: VerificadorDeBaseDeDatos.java:1507-1517, Constantes.java:842.
-- El catálogo Cobrado/A Cobrar lo prepara el baseline sintético, nunca el seed.
CREATE TABLE `t_sis_tipopago` (
  `ID_TipoPago` int(11) NOT NULL DEFAULT 0,
  `Nombre_TipoPago` varchar(55) NULL DEFAULT '',
  PRIMARY KEY (`ID_TipoPago`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- VerificadorDeBaseDeDatos.java:3872-3873 y :3901-3902.
ALTER TABLE `articulos`
  ADD COLUMN `artPrecioBulto` DECIMAL(18,3) NOT NULL DEFAULT 0.000;

-- VerificadorDeBaseDeDatos.java:2221; Constantes.java:833 (decimal).
ALTER TABLE `productos_hijos`
  ADD COLUMN `prhPrecioUnitario` DECIMAL(14,2) NULL DEFAULT 0.0;

-- VerificadorDeBaseDeDatos.java:3572-3573; Constantes.java:831 (integerNoNulo).
ALTER TABLE `movimientos_articulos`
  ADD COLUMN `ID_Venta` INT(11) NOT NULL DEFAULT 0,
  ADD COLUMN `ID_Compra` INT(11) NOT NULL DEFAULT 0;

-- VerificadorDeBaseDeDatos.java:4250 y :4263-4266; el fixture no tiene datos
-- que normalizar. Se crea directamente el NOT NULL DEFAULT 0 verificado.
ALTER TABLE `movimientos_articulos`
  ADD COLUMN `ID_ComputadoraModifica` INT(11) NOT NULL DEFAULT 0;

-- VerificadorDeBaseDeDatos.java:3832, clave vigente de cinco columnas.
ALTER TABLE `movimientos_articulos`
  DROP PRIMARY KEY,
  ADD PRIMARY KEY (`Empresa`,`Sucursal`,`Computadora`,`moaId`,`ID_ComputadoraModifica`);

-- VerificadorDeBaseDeDatos.java:2098-2102; Constantes.java:833 (decimal).
ALTER TABLE `t_fin_listapreciodetalle`
  ADD COLUMN `Cantidad` DECIMAL(14,2) NULL DEFAULT 0.0,
  ADD INDEX `buscar por producto y cantidad` (`Empresa`,`Sucursal`,`ID_Producto`,`Cantidad`,`activo`);
