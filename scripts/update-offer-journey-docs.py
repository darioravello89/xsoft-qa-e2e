"""Regenera fichas y suites de los recorridos de ofertas desde su registro público.

Uso: python scripts/update-offer-journey-docs.py [--check] [--case XG-PRM-063]
Conserva identidad, título, tags previos y el diseño funcional original completo.
No calcula reglas comerciales ni accede a un JAR, paquete privado o base de datos.
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from products.xgestion.offer_journeys.catalog import get_journey, get_journeys  # noqa: E402
from products.xgestion.offer_journeys.model import PAYMENT_METHODS  # noqa: E402

GENERATED_START = "<!-- BEGIN GENERATED OFFER JOURNEY -->"
GENERATED_END = "<!-- END GENERATED OFFER JOURNEY -->"
ARCHIVE_START = "<!-- BEGIN ORIGINAL OFFER DESIGN -->"
ARCHIVE_END = "<!-- END ORIGINAL OFFER DESIGN -->"
SEED = "catalogo-comercial-v1"
SCENARIOS = Path("products/xgestion/scenarios/promociones")
REQUIREMENTS = {
    "manual-discount": "Permisos general y sobre ofertas habilitados; descuento manual por importe total de línea.",
    "manual-price-list": "Elección manual de listas habilitada; cliente y turno sin lista automática.",
    "recalculate-price-list": "Recalcular productos al cambiar lista de precio: habilitado.",
    "manual-payments": "Medios QA manuales offline, tipo Cobrado, sin recargos, terminal ni proveedor externo.",
    "warning-on": "Aviso de riesgo del descuento manual: visible al guardar.",
    "warning-off": "Aviso de riesgo del descuento manual: ausente durante la ventana de observación calibrada.",
}
PROFILES = {
    "general-off": "Permiso general de descuento manual deshabilitado.",
    "offers-off": "Permiso general habilitado y permiso de descuento sobre ofertas deshabilitado.",
}


def money(value, currency="ARS"):
    return ("USD " if currency == "USD" else "$") + format(Decimal(value), ",.2f").translate(
        str.maketrans(",.", ".,"))


def quantity(value):
    return str(value).replace(".", ",")


def safe(value):
    return str(value).replace("|", "\\|").replace("\n", " ")


def suite_path(identifier):
    number = int(identifier.rsplit("-", 1)[1])
    for first, last, name in ((8, 10, "producto"), (11, 17, "familia"), (18, 24, "subfamilia"),
                              (25, 31, "marca"), (32, 38, "sector"), (39, 59, "agrupadas"),
                              (60, 64, "combos"), (65, 72, "condiciones"), (73, 76, "medios-pago"),
                              (79, 79, "condiciones"), (80, 84, "usd")):
        if first <= number <= last:
            return f"products/xgestion/suites/ofertas/{name}.robot"
    raise ValueError("Escenario fuera del alcance de este generador.")


def metadata_from(document):
    match = re.match(r"\A---\n(?P<metadata>.+?)\n---\n", document, flags=re.DOTALL)
    if not match:
        raise ValueError("La ficha no tiene frontmatter JSON válido.")
    return json.loads(match["metadata"]), match.end()


def implemented_metadata(metadata):
    result = dict(metadata)
    result.update(status="implemented", test=suite_path(metadata["id"]), seed=SEED)
    result["tags"] = list(dict.fromkeys((*metadata["tags"], "escritura")))
    return result


def _formula(offer, currency="ARS"):
    if offer.formula == "%":
        return f"{quantity(offer.discount)} % sobre el importe"
    if offer.formula == "$":
        return f"{money(offer.discount)} de descuento por unidad"
    if offer.formula == "C":
        return f"Llevar {offer.minimum} y pagar {quantity(offer.pay)}"
    if offer.formula == "C%":
        return f"{quantity(offer.pay)} % en una unidad de cada grupo completo de {offer.minimum}"
    if offer.formula == "LXO+%":
        return f"Desde {offer.minimum}: {quantity(offer.pay)} % sobre toda la cantidad"
    if offer.formula == "LXO+$":
        return f"Desde {offer.minimum}: {money(offer.pay)} de descuento por unidad"
    if offer.formula == "LXO+$CU":
        return f"Desde {offer.minimum}: precio final {money(offer.pay, currency)} por unidad"
    if offer.formula == "COMBO":
        return f"Precio final del combo completo: {money(offer.pay)}"
    raise ValueError(f"Fórmula sin descripción pública: {offer.formula}")


def _day(offset):
    return "hoy" if offset == 0 else f"hoy {offset:+d} días"


def _offer_scope(offer, products):
    if offer.scope == 6:
        by_id = {product.id: product for product in products.values()}
        return " + ".join(f"{quantity(amount)} × `{by_id[identifier].code}`"
                          for identifier, amount in offer.components)
    if offer.scope == 4:
        product = next(product for product in products.values() if product.id == offer.target)
        return f"Producto `{product.code}`"
    return f"{ {1: 'Sector', 2: 'Familia', 3: 'Subfamilia', 5: 'Marca'}[offer.scope]} `{safe(offer.target)}`"


def _basket(lines, products, lists):
    if not lines:
        return "Sin renglones en la operación."
    return "<br>".join(
        f"`{products[line.product].code}` × {quantity(line.quantity)} "
        f"{'kg' if products[line.product].unit == 2 else 'u'}: precio {money(line.price)}; "
        f"automático {money(line.discount)}; manual {money(line.manual)}; neto {money(line.total)}; "
        + (f"original USD: precio {money(line.original_price, 'USD')}, "
           f"descuento {money(line.original_discount, 'USD')}; " if line.original_price is not None else "") +
        f"lista aplicada: {safe(lists[line.price_list_id].name) if line.price_list_id else 'precio normal'}"
        for line in lines
    )


def _action(step, products, lists, medium):
    product = products.get(step.product)
    code = f"`{product.code}`" if product else ""
    unit = "kg" if product and product.unit == 2 else "u"
    if step.action == "open":
        return "Abrir una venta nueva y comprobar el contexto QA."
    if step.action == "add":
        return f"Cargar {quantity(step.value)} {unit} de {code} por código."
    if step.action == "edit":
        return f"Seleccionar {code}, abrir Ctrl+E, dejar {quantity(step.value)} {unit} y guardar."
    if step.action == "remove":
        return f"Seleccionar {code}, abrir Ctrl+E y elegir Eliminar."
    if step.action == "price_list":
        return f"Elegir la lista `{safe(lists[step.value].name)}` y comprobar el precio aplicado."
    if step.action == "payment_method":
        return f"Elegir `{PAYMENT_METHODS[step.value][1]}` y comprobar el recálculo."
    if step.action == "manual":
        return f"Abrir Ctrl+E en {code}, guardar {money(step.value)} de descuento manual total."
    if step.action == "manual_blocked":
        return f"Abrir Ctrl+E en {code} y comprobar que no permite editar {money(step.value)} de descuento manual."
    if step.action == "check":
        return "Comprobar todos los renglones y el total visible."
    if step.action == "abandon":
        return "Abandonar la venta y confirmar la salida sin cobrar."
    total = money(sum((line.total for line in step.expected), Decimal(0)))
    if step.action == "cancel_payment":
        return f"Abrir cobro en {medium}, ingresar {total} y cancelar antes de confirmar."
    if step.action == "pay":
        return f"Retomar el cobro en {medium}, ingresar {total} y confirmar una sola vez."
    raise ValueError(f"Acción sin descripción pública: {step.action}")


def _result(step, products, medium):
    if step.action == "abandon":
        return "Sin venta cobrada, pago ni cambios de stock o destino de cobro."
    total = money(sum((line.total for line in step.expected), Decimal(0)))
    result = f"Total **{total}**."
    if step.action == "open":
        return result + " ARS; precio normal y efectivo del perfil QA."
    if step.action == "cancel_payment":
        return result + " Conserva toda la canasta; sin venta cobrada, pago ni movimientos."
    if step.action == "pay":
        stock = "; ".join(f"`{products[line.product].code}` −{quantity(line.quantity)} "
                          f"{'kg' if products[line.product].unit == 2 else 'u'}" for line in step.expected)
        return result + f" Una venta y un cobro en {medium}; vuelto cero. Stock: {stock}."
    if step.action == "manual_blocked":
        return result + " Canasta y descuentos sin cambios; control de importe no editable."
    return result


def render(journey, metadata):
    usd = any(variant.exchange_rate is not None for variant in journey.variants)
    currency_profile = ("Productos y renglones USD; comprobante y cobro ARS; cotización 1500 ARS/USD. "
                        if usd else "ARS, ")
    chunks = [GENERATED_START, "", "## Recorrido de automatización", "",
              f"Estado del catálogo: **{metadata['status']}**. Automatización catalogada en "
              f"[`{Path(metadata['test']).name}`](../../suites/ofertas/{Path(metadata['test']).name}). "
              "Validación real: **pendiente**; requiere ejecutar el JAR exacto en el laboratorio calibrado.", "",
              "Las tablas siguientes son los datos y pasos actuales del recorrido. Los importes son expectativas "
              "fijas, no resultados medidos. El diseño anterior queda al final como referencia histórica "
              "para conservar reglas, variantes y límites; sus estados y códigos no describen la implementación actual.", "",
              "```powershell",
              f".\\qa.cmd run --product xgestion --scenario {journey.id} --seed {SEED} --log-level DEBUG", "```", "",
              "## Perfil y preparación", "",
              "Windows QA exclusivo y offline, escritorio desbloqueado, paquete autorizado y baseline restaurable. "
              f"{currency_profile}IVA 0 %, comprobante interno 99, stock suficiente, sin impresión ni fiscalización. "
              "Cliente y turno sin listas automáticas; otros descuentos, recargos y fidelización deshabilitados, "
              "salvo lo indicado en cada variante.", "",
              f"Preparar mediante el runner y `{SEED}` antes de abrir el JAR. Los códigos públicos de abajo "
              "pertenecen a este recorrido y reemplazan los ejemplos genéricos del diseño original. "
              "No cambiar reglas mediante SQL durante la venta. La falta de perfil, seed o calibración accesible "
              "se informa como bloqueo.", "",
              "Cada variante inicia el JAR de forma independiente. Los perfiles de configuración de 070 y 079 "
              "además requieren su preparación y restauración por fase. Una misma ficha conserva un solo ID lógico; "
              "solo queda aprobada si todas las variantes requeridas producen evidencia completa.", "",
              "**Lectura de importes:** automático y manual son descuentos totales del renglón. "
              "La grilla muestra ambos sumados en Descuentos; el informe y la evidencia de persistencia los distinguen. "
              "El neto de todos los renglones debe sumar el total de la venta."]
    if usd:
        chunks += ["", "**P0.** Requiere [calibración ofertas-usd-v1](../../docs/ofertas-usd.md). "
                   "En la canasta de abajo, $ indica ARS operativos; la grilla muestra los originales USD. "
                   "No convertir el precio promocional 50 a pesos en el seed. "
                   "Fallo o bloqueo impide acreditar aceptación de ofertas."]
    for index, variant in enumerate(journey.variants, start=1):
        products = {product.ref: product for product in variant.products}
        lists = {item.ref: item for item in variant.price_lists}
        by_id = {item.id: item for item in variant.price_lists}
        chunks += ["", f"## Variante {index}: {variant.name}", ""]
        if journey.id == "XG-PRM-079" and variant.name in PROFILES:
            chunks += [PROFILES[variant.name], ""]
        for requirement in variant.requirements:
            chunks.append(f"- {REQUIREMENTS[requirement]}")
        if variant.requirements:
            chunks.append("")
        chunks += ["### Productos preparados", "",
                   "| Referencia | Código | Precio base | Unidad | Familia / subfamilia / sector | Marca |",
                   "| --- | --- | ---: | --- | --- | --- |"]
        for product in variant.products:
            chunks.append(f"| {product.ref} | `{product.code}` | {money(product.price, product.currency)} | "
                          f"{'kg' if product.unit == 2 else 'unidad'} | "
                          f"{product.family} / {product.subfamily} / {product.sector} | {safe(product.brand)} |")
        chunks += ["", "### Ofertas preparadas", "",
                   "| Oferta | Incluye | Regla | Agrupación | Estado / vigencia inclusiva | Medios habilitados |",
                   "| --- | --- | --- | --- | --- | --- |"]
        for offer in variant.offers:
            media = ", ".join(PAYMENT_METHODS[ref][1] for ref in offer.payment_refs) or "Todos"
            chunks.append(f"| `{safe(offer.name)}` | {_offer_scope(offer, products)} | "
                          f"{_formula(offer, 'USD' if variant.exchange_rate is not None else 'ARS')} | "
                          f"{'No aplica: combo por componentes' if offer.scope == 6 else 'ON' if offer.grouped else 'OFF'} | "
                          f"{'Activa' if offer.active else 'Inactiva'}; {_day(offer.start_days)} a "
                          f"{_day(offer.end_days)} | {media} |")
        chunks += ["", "Las fechas se refieren a la fecha local usada al preparar el seed; Windows y MySQL "
                   "deben coincidir. No se modifica el reloj durante el recorrido."]
        if variant.price_lists:
            chunks += ["", "### Listas preparadas", "", "| Lista | Entradas de precio |", "| --- | --- |"]
            for item in variant.price_lists:
                entries = "; ".join(f"`{products[ref].code}`: {money(price)}" for ref, price in item.prices)
                chunks.append(f"| `{safe(item.name)}` | {entries or 'Sin entrada para los productos del recorrido'} |")
        chunks += ["", "### Pasos y resultados esperados", "",
                   "| Paso | Acción del usuario | Canasta completa después del paso | Resultado |",
                   "| ---: | --- | --- | --- |"]
        medium = "efectivo del perfil QA"
        for step_number, step in enumerate(variant.steps, start=1):
            if step.action == "open":
                medium = "efectivo del perfil QA"
            elif step.action == "payment_method":
                medium = f"`{PAYMENT_METHODS[step.value][1]}`"
            chunks.append(f"| {step_number} | {_action(step, products, lists, medium)} | "
                          f"{_basket(step.expected, products, by_id)} | {_result(step, products, medium)} |")
    if journey.notes:
        chunks += ["", "## Notas del recorrido", "", *(f"- {note}" for note in journey.notes)]
    chunks += ["", "## Evidencia, recuperación y límites", "",
               "Registrar cada variante y paso con esperado, observado, resultado y ubicación del informe privado. "
               "Conservar cantidades, precios, descuentos y netos visibles; comprobar por identidad de la operación "
               "venta, detalle, oferta, lista aplicada, medio, stock y destino de cobro. Cancelar o abandonar "
               "no debe crear esos efectos; confirmar produce una sola operación. No se deduce el número de filas "
               "de pago sin el contrato de cobro simple del perfil.", "",
               "Ante una discrepancia, conservar evidencia y detener la confirmación. Finalizar únicamente el JAR "
               "del runner; restaurar el baseline antes de repetir. No corregir importes o movimientos en la base "
               "para conseguir un resultado aprobado. INFO resume; DEBUG muestra los pasos; TRACE añade diagnóstico "
               "saneado. Un fallo informa paso, esperado, observado, categoría y evidencia; causa no determinada "
               "si no está demostrada.", "",
               "La automatización y su dry-run no acreditan ejecución real. No cubre producción, emisión fiscal, "
               "impresoras, balanzas, pasarelas de pago, red ni concurrencia. Las variantes descritas solamente "
               "en el diseño original deben contrastarse antes de acreditarlas como cubiertas.", "",
               "## Trazabilidad de la automatización", "",
               (f"- Fuente ERP del contrato técnico: commit `{journey.source_commit}`; "
                "la regla USD 50 proviene del incidente y del plan aprobado. Las rutas y tests "
                if usd else f"- Fuente ERP de las expectativas: commit `{journey.source_commit}`. Las rutas y tests de reglas ") +
               "están preservados en el anexo original; no son evidencia de ejecución sobre el JAR.",
               "- Contrato de datos y pasos: [catálogo de recorridos](../../offer_journeys/catalog.py).",
               "- Identidad de ofertas, precios y deltas: [oráculos de lectura](../../offer_journeys/oracles.py).",
               "- Mantener SHA256/build del JAR, paquete, perfil, versión de datos, fecha y responsable en evidencia "
               "privada; no publicar credenciales, filas completas, capturas de autenticación ni árboles privados.",
               "- Regenerar desde la raíz: `python scripts/update-offer-journey-docs.py`; comprobar sincronización "
               "con `python scripts/update-offer-journey-docs.py --check`.", "", GENERATED_END]
    return "\n".join(chunks)


def update_document(document, journey):
    metadata, header_end = metadata_from(document)
    if metadata.get("id") != journey.id:
        raise ValueError("La identidad de ficha y recorrido no coincide.")
    metadata = implemented_metadata(metadata)
    markers = (GENERATED_START, GENERATED_END, ARCHIVE_START, ARCHIVE_END)
    counts = [document.count(marker) for marker in markers]
    if any(counts) and counts != [1, 1, 1, 1]:
        raise ValueError("Los marcadores de documentación están incompletos o duplicados.")
    if any(counts):
        positions = [document.index(marker) for marker in markers]
        if positions != sorted(positions):
            raise ValueError("Los marcadores de documentación están fuera de orden.")
        prefix = document[header_end:positions[0]].rstrip()
        original = document[positions[2] + len(ARCHIVE_START):positions[3]].strip("\n")
    else:
        original_start = document.find("\n## Estado y alcance", header_end)
        if original_start < 0:
            raise ValueError("La ficha no contiene la sección original de estado y alcance.")
        prefix = document[header_end:original_start].rstrip()
        original = document[original_start:].strip("\n")
    header = "---\n" + json.dumps(metadata, ensure_ascii=False, separators=(",", ":")) + "\n---\n"
    archive = ("<details>\n<summary>Diseño funcional original: referencia histórica y variantes a contrastar</summary>\n\n"
               "Este bloque conserva el diseño previo completo. Sus menciones de estado, seed pendiente o ausencia "
               "de Robot son históricas; el contrato actual está en las tablas anteriores. Una variante adicional "
               "de este bloque no se considera ejecutada por aparecer documentada.\n\n"
               f"{ARCHIVE_START}\n{original}\n{ARCHIVE_END}\n\n</details>")
    return header + prefix + "\n\n" + render(journey, metadata) + "\n\n" + archive + "\n"


def _robot_cells(prefix, cells):
    lines = [prefix]
    for cell in cells:
        if len(lines[-1]) + 4 + len(cell) > 120:
            lines.append("    ...")
        lines[-1] += "    " + cell
    return lines


def render_suite(metadata_rows):
    rows = sorted(metadata_rows, key=lambda row: row["id"])
    shared = set.intersection(*(set(row["tags"]) for row in rows))
    common_tags = [tag for tag in rows[0]["tags"] if tag in shared]
    chunks = ["*** Settings ***", "Documentation    Recorridos de ofertas con datos fijos y validación real pendiente.",
              "Library          products.xgestion.offer_journeys.library.XGestionOfferJourneysLibrary",
              "Test Teardown    Finalizar Recorrido De Ofertas",
              *_robot_cells("Test Tags   ", common_tags), "", "", "*** Test Cases ***"]
    for metadata in rows:
        journey = get_journey(metadata["id"])
        count = len(journey.variants)
        tags = [tag for tag in metadata["tags"] if tag not in shared]
        chunks += [f"{metadata['id']} {metadata['title']}",
                   f"    [Documentation]    {count} {'variante' if count == 1 else 'variantes'}; "
                   "ver ficha y pasos exactos del catálogo.",
                   *_robot_cells("    [Tags]", (*tags, metadata["id"])),
                   f"    Ejecutar Recorrido De Ofertas    {metadata['id']}", ""]
    return "\n".join(chunks)


def artifacts(root=ROOT, identifiers=None):
    selected = set(identifiers or (journey.id for journey in get_journeys()))
    unknown = selected - {journey.id for journey in get_journeys()}
    if unknown:
        raise ValueError("Escenarios fuera del catálogo: " + ", ".join(sorted(unknown)))
    result, groups = {}, defaultdict(list)
    for journey in get_journeys():
        path = SCENARIOS / f"{journey.id}.md"
        original = (root / path).read_text(encoding="utf-8")
        metadata, _ = metadata_from(original)
        if metadata.get("id") != journey.id:
            raise ValueError("La identidad de ficha y recorrido no coincide.")
        metadata = implemented_metadata(metadata)
        groups[Path(metadata["test"])].append(metadata)
        if journey.id in selected:
            result[path] = update_document(original, journey)
    selected_suites = {Path(suite_path(identifier)) for identifier in selected}
    result.update((path, render_suite(rows)) for path, rows in groups.items() if path in selected_suites)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verifica sincronización sin escribir archivos.")
    parser.add_argument("--case", action="append", dest="identifiers", help="Limita fichas; mantiene suites completas.")
    args = parser.parse_args(argv)
    generated = artifacts(identifiers=args.identifiers)
    changed = [path for path, content in generated.items()
               if not (ROOT / path).is_file() or (ROOT / path).read_text(encoding="utf-8") != content]
    if args.check:
        for path in changed:
            print(f"Desactualizado: {path.as_posix()}")
        print(f"Documentación y suites: {len(generated)} archivos; {len(changed)} desactualizados.")
        return 1 if changed else 0
    for path in changed:
        (ROOT / path).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / path).write_text(generated[path], encoding="utf-8", newline="\n")
    print(f"Documentación y suites: {len(changed)} archivos actualizados; sin ejecución real del producto.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
