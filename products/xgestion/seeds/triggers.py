"""Read-only certification of database automation reachable by commercial seeds.

Only reviewed XGestion2 f34238183d494259bed1279dd7d9aac0ce16a3ae bodies
are accepted. No routine, trigger or queue is created, changed or disabled.
Whitespace outside SQL tokens is immaterial; literals and identifiers remain
case-sensitive and complete. Unknown bodies fail closed without printing SQL.
"""

import hashlib
import re

from framework.errors import QAError

# DATABASE_SCHEMA.sql:2531-2569, full legacy ROUTINE_DEFINITION.
LEGACY_FUNCTION = """BEGIN

	SELECT SUBSTRING_INDEX(USER(), '@', 1) INTO @usuario;
	SELECT IFNULL(@cpu_actual, 0) INTO @cpu_actual;

	IF IFNULL(@usuario, '') NOT IN ('xgestion', 'backend_sincronizador') AND IFNULL(p_usuario, '') NOT IN ('xgestion', 'backend_sincronizador') THEN

		SELECT group_concat(sucId) INTO @sucursales FROM _sucursales WHERE Empresa = p_empresa AND activo=TRUE AND sucId<>999;
		SELECT group_concat(cpuId) INTO @computadoras FROM _computadoras WHERE Empresa = p_empresa AND activo=TRUE AND cpuId<>999;

		SET @cpu_modifica = 0;
		IF p_tabla = 'ventas' THEN
			SELECT IFNULL(ID_ComputadoraModifica, 0) INTO @cpu_modifica
			FROM ventas
			WHERE Empresa = p_empresa AND Sucursal = p_sucursal AND Computadora = p_computadora AND venId = p_id
			LIMIT 1;
		ELSEIF p_tabla = 'ventas_cuerpo' THEN
			SELECT IFNULL(ID_ComputadoraModifica, 0) INTO @cpu_modifica
			FROM ventas_cuerpo
			WHERE Empresa = p_empresa AND Sucursal = p_sucursal AND Computadora = p_computadora AND vecId = p_id
			LIMIT 1;
		END IF;
		IF @cpu_modifica = 0 THEN
			SET @cpu_modifica = @cpu_actual;
		END IF;

		IF (p_accion = 'update' OR p_accion = 'insert') AND p_tabla IN ('ventas', 'ventas_cuerpo') AND @cpu_modifica <> 0 AND @cpu_modifica <> p_computadora THEN
			SET @computadoras = TRIM(BOTH ',' FROM REPLACE(CONCAT(',', REPLACE(COALESCE(@computadoras, ''), ' ', ''), ','), CONCAT(',', @cpu_modifica, ','), ','));
		END IF;

		INSERT INTO t_int_sincronizador (Empresa, Sucursal, Computadora, ID, Tabla, Accion, SucursalesDestino, ComputadorasDestino, fecha_insert, usuario_insert)
		VALUES( p_empresa, p_sucursal, p_computadora, p_id, p_tabla, p_accion, @sucursales, @computadoras, NOW(), p_usuario )
		ON DUPLICATE KEY
		UPDATE fecha_update=NOW(), usuario_update=p_usuario;

	END IF;

	RETURN 1;
END"""

# VerificadorDeBaseDeDatos.java:4028-4121, full current ROUTINE_DEFINITION.
CURRENT_FUNCTION = """BEGIN
    DECLARE v_sucursales    TEXT;
    DECLARE v_computadoras  TEXT;
    DECLARE v_rows          INT DEFAULT 0;
    DECLARE v_cpu_modifica  INT DEFAULT 0;

    SELECT SUBSTRING_INDEX(USER(), '@', 1) INTO @usuario;
    SELECT IFNULL(@cpu_actual, 0) INTO @cpu_actual;

    IF IFNULL(@usuario, '') NOT IN ('xgestion', 'backend_sincronizador') AND IFNULL(p_usuario, '') NOT IN ('xgestion', 'backend_sincronizador') THEN

        SELECT GROUP_CONCAT(sucId) INTO v_sucursales
        FROM _sucursales
        WHERE Empresa = p_empresa
          AND activo = TRUE
          AND sucId <> 999;

        SELECT GROUP_CONCAT(cpuId) INTO v_computadoras
        FROM _computadoras
        WHERE Empresa = p_empresa
          AND activo = TRUE
          AND cpuId <> 999
          AND (p_tabla <> 't_fin_impuestos' OR cpuId <> p_computadora)
          AND NOT (
              CASE
                  WHEN JSON_VALID(COALESCE(NULLIF(TRIM(Configuracion), ''), '{}')) THEN
                      CASE
                          WHEN JSON_TYPE(JSON_EXTRACT(COALESCE(NULLIF(TRIM(Configuracion), ''), '{}'), '$.sincronizacionV2')) = 'BOOLEAN' THEN
                              JSON_UNQUOTE(JSON_EXTRACT(COALESCE(NULLIF(TRIM(Configuracion), ''), '{}'), '$.sincronizacionV2')) = 'true'
                          ELSE FALSE
                      END
                  ELSE FALSE
              END
          );

        IF p_tabla = 'ventas' THEN
            SELECT IFNULL(ID_ComputadoraModifica, 0) INTO v_cpu_modifica
            FROM ventas
            WHERE Empresa = p_empresa AND Sucursal = p_sucursal AND Computadora = p_computadora AND venId = p_id
            LIMIT 1;
        ELSEIF p_tabla = 'ventas_cuerpo' THEN
            SELECT IFNULL(ID_ComputadoraModifica, 0) INTO v_cpu_modifica
            FROM ventas_cuerpo
            WHERE Empresa = p_empresa AND Sucursal = p_sucursal AND Computadora = p_computadora AND vecId = p_id
            LIMIT 1;
        ELSEIF p_tabla = 'ventas_pagos' THEN
            SELECT IFNULL(ID_ComputadoraModifica, 0) INTO v_cpu_modifica
            FROM ventas_pagos
            WHERE Empresa = p_empresa AND Sucursal = p_sucursal AND Computadora = p_computadora AND ID_VentaPago = p_id
            LIMIT 1;
        ELSEIF p_tabla = 'movimientos_articulos' THEN
            SELECT IFNULL(ID_ComputadoraModifica, 0) INTO v_cpu_modifica
            FROM movimientos_articulos
            WHERE Empresa = p_empresa AND Sucursal = p_sucursal AND Computadora = p_computadora AND moaId = p_id
            LIMIT 1;
        ELSEIF p_tabla = 'compra' THEN
            SELECT IFNULL(ID_ComputadoraModifica, 0) INTO v_cpu_modifica
            FROM compra
            WHERE Empresa = p_empresa AND Sucursal = p_sucursal AND Computadora = p_computadora AND comId = p_id
            LIMIT 1;
        ELSEIF p_tabla = 'compra_detalle' THEN
            SELECT IFNULL(ID_ComputadoraModifica, 0) INTO v_cpu_modifica
            FROM compra_detalle
            WHERE Empresa = p_empresa AND Sucursal = p_sucursal AND Computadora = p_computadora AND codId = p_id
            LIMIT 1;
        END IF;

        IF v_cpu_modifica = 0 THEN
            SET v_cpu_modifica = @cpu_actual;
        END IF;

        IF (p_accion = 'update' OR p_accion = 'insert') AND p_tabla IN ('ventas', 'ventas_cuerpo') AND v_cpu_modifica <> 0 AND v_cpu_modifica <> p_computadora THEN
            SET v_computadoras = TRIM(BOTH ',' FROM REPLACE(CONCAT(',', REPLACE(COALESCE(v_computadoras, ''), ' ', ''), ','), CONCAT(',', v_cpu_modifica, ','), ','));
        END IF;

        INSERT INTO t_int_sincronizador (
            Empresa, Sucursal, Computadora, ID, Tabla, Accion,
            SucursalesDestino, fecha_insert, usuario_insert, ComputadorasDestino, ID_Computadora
        )
        VALUES (
            p_empresa, p_sucursal, p_computadora, p_id, p_tabla, p_accion,
            COALESCE(v_sucursales, ''), NOW(), @usuario, COALESCE(v_computadoras, ''), 0
        )
        ON DUPLICATE KEY UPDATE
            Accion = IF(p_tabla = 't_fin_impuestos', VALUES(Accion), Accion),
            SucursalesDestino = IF(p_tabla = 't_fin_impuestos', VALUES(SucursalesDestino), SucursalesDestino),
            ComputadorasDestino = IF(p_tabla = 't_fin_impuestos', VALUES(ComputadorasDestino), ComputadorasDestino),
            fecha_update = NOW(),
            usuario_update = @usuario;
    END IF;

    SET v_rows = ROW_COUNT();
    RETURN v_rows;
END"""

# VerificadorDeBaseDeDatos.java:4129-4131 and :5822-5824, existing ERP bootstrap fallback.
NOOP_FUNCTION = "RETURN 1"

# Tokens preserve quoted content and identifier case; replacing whitespace by
# tokens cannot turn a different string literal or identifier into an approved one.
_TOKEN = re.compile(
    r"'(?:''|\\.|[^'\\])*'|\"(?:\"\"|\\.|[^\"\\])*\"|`(?:``|[^`])*`|"
    r"[A-Za-z_][A-Za-z_0-9$]*|\d+(?:\.\d+)?|[^\s]"
)


def _fingerprint(body):
    if not isinstance(body, str) or not body.strip():
        return None
    tokens = _TOKEN.findall(body.strip())
    if tokens and tokens[-1] == ";":
        tokens.pop()  # MySQL metadata may omit the final statement terminator.
    return hashlib.sha256(" ".join(tokens).encode("utf-8")).hexdigest()


_FUNCTIONS = {
    _fingerprint(LEGACY_FUNCTION): ("legacy", "bit"),
    _fingerprint(CURRENT_FUNCTION): ("current", "int"),
    _fingerprint(NOOP_FUNCTION): ("bootstrap-noop", "int"),
}

# DATABASE_SCHEMA.sql:2664-3065; variantes: VerificadorDeBaseDeDatos.java:3856-3866.
_TRIGGER_ARGUMENTS = {
    "_familias": ("0", "0", "famId"),
    "_subfamilias": ("0", "0", "subId"),
    "_ubicaciones": ("0", "0", "ubiId"),
    "_proveedores": ("0", "0", "proId"),
    "articulos": ("0", "0", "artId"),
    "productos_hijos": ("0", "0", "prhId"),
    "productos_opciones": ("0", "0", "ID_ProductoOpcion"),
    "variantes": ("0", "0", "ID_Variante"),
    "ofertas": ("0", "0", "ofeId"),
    "movimientos_articulos": ("NEW.Sucursal", "NEW.Computadora", "moaId"),
    "t_fin_listaprecio": ("NEW.Sucursal", "0", "ID_ListaPrecio"),
    "t_fin_listapreciodetalle": ("NEW.Sucursal", "0", "ID_ListaPrecioDetalle"),
}
_QUEUE = "t_int_sincronizador"
# Snapshot: DATABASE_SCHEMA.sql:1591. Migrated order: Verificador.java:1960-1962.
_QUEUE_PRIMARY_KEYS = {
    ("Empresa", "Sucursal", "Computadora", "ID", "Tabla", "ID_Computadora", "fecha_insert"),
    ("Empresa", "Sucursal", "Computadora", "Tabla", "ID", "ID_Computadora", "fecha_insert"),
}
_QUEUE_COLUMNS = {
    "Empresa": "int", "Sucursal": "int", "Computadora": "int", "ID": "int",
    "Tabla": "varchar", "Accion": "varchar", "SucursalesDestino": "varchar",
    "ComputadorasDestino": "varchar", "ID_Computadora": "int", "fecha_insert": "datetime",
    "usuario_insert": "varchar", "fecha_update": "datetime", "usuario_update": "varchar",
}
_PARAMETERS = [(name, kind, 255 if kind == "varchar" else None) for name, kind in (
    ("p_empresa", "int"), ("p_sucursal", "int"), ("p_computadora", "int"),
    ("p_id", "int"), ("p_tabla", "varchar"), ("p_accion", "varchar"), ("p_usuario", "varchar"),
)]


def _query(connection, sql, values=()):
    with connection.cursor() as cursor:
        cursor.execute(sql, values)
        return list(cursor.fetchall())


def _triggers(connection, names):
    placeholders = ",".join("%s" for _ in names)
    return _query(connection, "SELECT TRIGGER_NAME AS name, EVENT_OBJECT_TABLE AS table_name, "
                  "ACTION_TIMING AS timing, EVENT_MANIPULATION AS event, ACTION_ORIENTATION AS orientation, "
                  "ACTION_STATEMENT AS body FROM information_schema.TRIGGERS "
                  f"WHERE EVENT_OBJECT_SCHEMA=DATABASE() AND EVENT_OBJECT_TABLE IN ({placeholders})", tuple(names))


def _certify_function(connection):
    found = _query(connection, "SELECT ROUTINE_DEFINITION AS body, DATA_TYPE AS kind, "
                   "SECURITY_TYPE AS security_type, ROUTINE_TYPE AS routine_type "
                   "FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA=DATABASE() AND ROUTINE_NAME=%s",
                   ("fEnviarSincronizacion",))
    if len(found) != 1:
        raise QAError("Falta la función de sincronización certificable; el seed no la crea ni reemplaza.")
    routine = found[0]
    variant = _FUNCTIONS.get(_fingerprint(routine["body"]))
    if (not variant or routine["kind"] != variant[1] or routine["security_type"] != "DEFINER"
            or routine["routine_type"] != "FUNCTION"):
        raise QAError("La función de sincronización no coincide con una versión fuente certificada.")
    parameters = _query(connection, "SELECT ORDINAL_POSITION AS position, PARAMETER_NAME AS name, "
                        "PARAMETER_MODE AS mode, DATA_TYPE AS kind, CHARACTER_MAXIMUM_LENGTH AS length "
                        "FROM information_schema.PARAMETERS WHERE SPECIFIC_SCHEMA=DATABASE() "
                        "AND SPECIFIC_NAME=%s AND ORDINAL_POSITION>0 ORDER BY ORDINAL_POSITION",
                        ("fEnviarSincronizacion",))
    signature = [(p["name"], p["kind"], p["length"]) for p in parameters]
    if signature != _PARAMETERS or any(p["position"] != i or p["mode"] != "IN"
                                       for i, p in enumerate(parameters, 1)):
        raise QAError("Los parámetros de la función de sincronización difieren del contrato fuente.")
    if variant[0] != "bootstrap-noop":
        # The reviewed routine reads these objects. A view could hide another
        # function call, so only physical tables may supply its context.
        for dependency in ("_sucursales", "_computadoras"):
            info = _query(connection, "SELECT ENGINE AS engine, TABLE_TYPE AS table_type "
                          "FROM information_schema.TABLES WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s",
                          (dependency,))
            if len(info) != 1 or info[0]["table_type"] != "BASE TABLE":
                raise QAError("Una dependencia de la función de sincronización no es una tabla física.")


def _certify_queue(connection):
    info = _query(connection, "SELECT ENGINE AS engine, TABLE_TYPE AS table_type "
                  "FROM information_schema.TABLES WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s", (_QUEUE,))
    if len(info) != 1 or info[0]["engine"] != "InnoDB" or info[0]["table_type"] != "BASE TABLE":
        raise QAError("La cola de sincronización debe ser una tabla física InnoDB certificada.")
    if _triggers(connection, (_QUEUE,)):
        raise QAError("La cola de sincronización contiene triggers no permitidos para el seed.")
    foreign = _query(connection, "SELECT CONSTRAINT_NAME AS name FROM information_schema.KEY_COLUMN_USAGE "
                     "WHERE REFERENCED_TABLE_NAME IS NOT NULL AND "
                     "((TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s) OR "
                     "(REFERENCED_TABLE_SCHEMA=DATABASE() AND REFERENCED_TABLE_NAME=%s))", (_QUEUE, _QUEUE))
    if foreign:
        raise QAError("La cola de sincronización contiene relaciones externas no certificadas.")
    indexes = _query(connection, "SELECT INDEX_NAME AS name, COLUMN_NAME AS field, SUB_PART AS prefix_length "
                     "FROM information_schema.STATISTICS WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s "
                     "AND NON_UNIQUE=0 ORDER BY INDEX_NAME, SEQ_IN_INDEX", (_QUEUE,))
    if (tuple(i["field"] for i in indexes) not in _QUEUE_PRIMARY_KEYS
            or any(i["name"] != "PRIMARY" or i["prefix_length"] is not None for i in indexes)):
        raise QAError("La clave de la cola de sincronización no coincide o tiene únicos adicionales.")
    columns = _query(connection, "SELECT COLUMN_NAME AS name, DATA_TYPE AS kind, EXTRA AS extra "
                     "FROM information_schema.COLUMNS WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s", (_QUEUE,))
    if ({c["name"]: c["kind"] for c in columns} != _QUEUE_COLUMNS
            or any(c["extra"] for c in columns)):
        raise QAError("Las columnas de la cola de sincronización difieren del contrato certificado.")


def check_triggers(connection, tables):
    """Certify reachable synchronization side effects without executing them.

    Called before the first write inside the seed transaction, on the exclusively
    owned QA server. No triggers is valid; any unknown automation blocks the batch.
    """
    names = [table.name for table in tables]
    if not names:
        return
    found = _triggers(connection, names)
    if not found:
        return
    seen = set()
    for trigger in found:
        name, event = trigger["table_name"], trigger["event"]
        args = _TRIGGER_ARGUMENTS.get(name)
        if (not args or name not in names or event not in {"INSERT", "UPDATE"}
                or trigger["timing"] != "AFTER" or trigger["orientation"] != "ROW"
                or trigger["name"] != f"{name}_AFTER_{event}" or (name, event) in seen):
            raise QAError("Existe un trigger no certificado en las tablas del seed; no se modifica.")
        branch, computer, identifier = args
        expected = (f"BEGIN SELECT fEnviarSincronizacion(NEW.Empresa,{branch},{computer},NEW.{identifier},"
                    f"'{name}','{event.lower()}',NEW.usuario_{event.lower()}) INTO @resultado; END")
        if _fingerprint(trigger["body"]) != _fingerprint(expected):
            raise QAError("El cuerpo de un trigger del seed difiere del contrato fuente certificado.")
        seen.add((name, event))
    _certify_function(connection)
    _certify_queue(connection)
