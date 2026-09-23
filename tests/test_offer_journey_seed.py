import json
from dataclasses import replace
from datetime import date

import pytest

from framework.errors import QAError
from products.xgestion.offer_journeys.model import Journey, Offer, PriceList, Product, Step, Variant
from products.xgestion.seeds.journeys import build_journey_tables
from products.xgestion.seeds.model import SeedContext, merge_tables
from products.xgestion.seeds.pricing import pricing_tables
from products.xgestion.seeds.products import product_tables

CTX = SeedContext(1, 1, 1, 1, date(2026, 9, 22))
A = Product("A", 981101, "QA-PRM-TEST-A", family=981100, subfamily=981100)
OFFER = Offer(981100, "QA-PRM-TEST-OFERTA", 4, A.id, "%", "10")


def variant(products=(A,), offers=(OFFER,), lists=(), name="principal"):
    return Variant(name, products, offers, (Step("open"), Step("abandon")), price_lists=lists)


def rows(*variants):
    return {table.name: table.rows for table in build_journey_tables(CTX, (Journey("XG-PRM-011", variants),))}


def test_identical_variants_keep_one_identity_and_exact_public_names():
    result = rows(variant(), variant())
    assert len(result["articulos"]) == len(result["ofertas"]) == 1
    assert result["articulos"][0]["artCodigo"] == A.code
    assert result["ofertas"][0]["ofeNombre"] == OFFER.name
    assert result["articulos"][0]["artFamiliaNombre"] == result["_familias"][0]["famNombre"]
    assert result["articulos"][0]["artSubfamiliaNombre"] == result["_subfamilias"][0]["subNombre"]
    assert all(row["famId"] != 980001 for row in result["_familias"])
    assert result["movimientos_articulos"][0]["moaCantidad"] == "100.000"


def test_same_product_id_with_different_price_is_rejected():
    with pytest.raises(QAError, match="incompatibles"):
        rows(variant(), variant(products=(replace(A, price="1200.00"),)))


def test_two_product_ids_cannot_claim_the_same_code():
    with pytest.raises(QAError, match="natural"):
        rows(variant(products=(A, replace(A, id=981102, ref="B"))))


def test_one_subfamily_cannot_belong_to_two_families():
    conflicting = replace(A, id=981102, code="QA-PRM-TEST-B", ref="B", family=981200)
    with pytest.raises(QAError, match="_subfamilias"):
        rows(variant(products=(A, conflicting)))


def test_catalog_merges_with_original_battery_without_redefining_its_rows():
    original = product_tables(CTX) + pricing_tables(CTX)
    added = build_journey_tables(CTX, (Journey("XG-PRM-011", (variant(),)),))
    combined = merge_tables(original + added)
    assert len(next(table.rows for table in combined if table.name == "articulos")) == 49
    assert next(row for table in combined if table.name == "articulos" for row in table.rows
                if row["artId"] == 980001)["artCodigo"] == "QA-SEED-NORMAL"


def test_empty_fallback_list_keeps_header_without_inventing_a_price():
    lists = (PriceList("empty", 988200, "QA-PRM-LISTA-VACIA"),
             PriceList("priced", 988201, "QA-PRM-LISTA-PRECIO", (("A", "750.00"),)))
    result = rows(variant(lists=lists))
    assert {row["ID_ListaPrecio"] for row in result["t_fin_listaprecio"]} == {988200, 988201}
    details = result["t_fin_listapreciodetalle"]
    assert len(details) == 1
    assert details[0]["ID_ListaPrecio"] == details[0]["ID_ListaPrecioDetalle"] == 988201
    assert details[0]["ID_Producto"] == A.id


def test_unknown_list_product_is_rejected():
    unknown = PriceList("bad", 988200, "QA-PRM-LISTA-BAD", (("UNKNOWN", "750.00"),))
    with pytest.raises(QAError, match="Producto de lista desconocido"):
        rows(variant(lists=(unknown,)))


def test_grouped_and_combo_keep_distinct_json_contracts():
    grouped = replace(OFFER, scope=2, target=A.family, grouped=True)
    assert json.loads(rows(variant(offers=(grouped,)))["ofertas"][0]["Configuracion"]) == {"agrupada": True}
    combo = replace(OFFER, scope=6, target=0, formula="COMBO", discount="0", pay="400",
                    components=((A.id, "0.5"),))
    assert json.loads(rows(variant(offers=(combo,)))["ofertas"][0]["Configuracion"]) == {
        "combo": {"version": 1, "productos": [{"idProducto": A.id, "cantidad": 0.5}]},
    }


@pytest.mark.parametrize("component", ["A", "981101", True, 999999])
def test_combo_rejects_non_integer_or_unknown_component_identity(component):
    combo = replace(OFFER, scope=6, target=0, formula="COMBO", components=((component, "1"),))
    with pytest.raises(QAError, match="IDs enteros|desconocido"):
        rows(variant(offers=(combo,)))


def test_nested_classifications_from_067_are_consistent_across_all_variants():
    from products.xgestion.offer_journeys.conditions import CASES

    tables = build_journey_tables(CTX, (CASES["XG-PRM-067"],))
    declared = {}
    for item in CASES["XG-PRM-067"].variants:
        for product in item.products:
            if product.subfamily != 980001:
                previous = declared.setdefault(product.subfamily, product.family)
                assert previous == product.family
    actual = next(table.rows for table in tables if table.name == "_subfamilias")
    assert {row["subId"]: row["famId"] for row in actual} == declared


def activation_case():
    return Journey("XG-PRM-070", (
        variant(name="active"), variant(offers=(replace(OFFER, active=False),), name="inactive"),
        variant(name="active-again"),
    ))


def test_profile_070_selects_same_identity_with_only_active_flag_changed():
    journey = activation_case()
    base = build_journey_tables(CTX, (journey,))
    selected = build_journey_tables(CTX, (journey,), journey_profile=(journey.id, "inactive"))
    for original, changed in zip(base, selected, strict=True):
        assert changed.rows == ([{**original.rows[0], "activo": 0}]
                                if original.name == "ofertas" else original.rows)
    assert build_journey_tables(CTX, (journey,), journey_profile=(journey.id, "active-again")) == base


@pytest.mark.parametrize("profile", [("XG-PRM-070", "wrong"), ("XG-PRM-071", "active"),
                                    ("XG-PRM-999", "inactive"), "XG-PRM-070", ("XG-PRM-070",)])
def test_unknown_or_malformed_profile_is_rejected(profile):
    with pytest.raises(QAError, match="[Pp]erfil"):
        build_journey_tables(CTX, (activation_case(),), journey_profile=profile)


def test_profile_070_cannot_change_product_or_offer_rules():
    changed = replace(activation_case(), variants=(variant(name="active"),
                      variant(offers=(replace(OFFER, active=False, pay="123"),), name="inactive"),
                      variant(name="active-again")))
    with pytest.raises(QAError, match="070"):
        build_journey_tables(CTX, (changed,), journey_profile=(changed.id, "inactive"))


def test_manual_payment_rows_are_dedicated_local_methods_with_no_external_provider():
    result = rows(variant())["_pagos"]
    assert [(row["pagId"], row["pagNombre"]) for row in result] == [
        (989901, "QA-PRM-EFECTIVO"), (989902, "QA-PRM-TRANSFERENCIA"), (989903, "QA-PRM-TARJETA"),
    ]
    for row in result:
        assert row["ID_TipoPago"] == row["activo"] == 1
        assert row["pagPorcentajeDescuento"] == row["pagComisionMedioPago"] == "0.00"
        assert row["ID_PedidosYa"] == row["ID_TiendaNube"] == ""
        assert json.loads(row["Configuracion"]) == {}


@pytest.mark.parametrize("refs,payment_id,config", [
    ((), 0, {}), (("cash",), 989901, {}),
    (("cash", "transfer"), -1, {"tiposCobro": {"version": 1, "ids": [989901, 989902]}}),
])
def test_offer_payment_restrictions_use_reviewed_single_and_multiple_contracts(refs, payment_id, config):
    offer = replace(OFFER, payment_refs=refs)
    row = rows(variant(offers=(offer,)))["ofertas"][0]
    assert row["ID_Pago"] == payment_id
    assert json.loads(row["Configuracion"]) == config


@pytest.mark.parametrize("refs", [("external",), ("cash", "cash")])
def test_unknown_or_duplicate_payment_binding_is_rejected(refs):
    with pytest.raises(QAError, match="medio de pago"):
        rows(variant(offers=(replace(OFFER, payment_refs=refs),)))


def test_all_079_profiles_leave_public_catalog_identical():
    names = ("general-off", "offers-off", "allowed-warning-on", "allowed-warning-off")
    case = Journey("XG-PRM-079", tuple(variant(name=name) for name in names))
    baseline = build_journey_tables(CTX, (case,))
    for name in names:
        assert build_journey_tables(CTX, (case,), journey_profile=(case.id, name)) == baseline


def test_full_public_catalog_preserves_original_rows_and_includes_every_journey():
    from products.xgestion.offer_journeys.catalog import get_journeys
    from products.xgestion.seeds.engine import catalog

    actual = {table.name: table for table in catalog(CTX)}
    for table in merge_tables(product_tables(CTX) + pricing_tables(CTX)):
        for row in table.rows:
            assert row in actual[table.name].rows
    for table in build_journey_tables(CTX, get_journeys()):
        for row in table.rows:
            assert row in actual[table.name].rows


def test_seed_review_traces_base_and_journey_sources_separately():
    from products.xgestion.offer_journeys.catalog import get_journeys
    from products.xgestion.seeds.engine import describe_seed, render_seed

    summary = describe_seed(CTX.reference_date)
    assert summary["source_commit"] == "f34238183d494259bed1279dd7d9aac0ce16a3ae"
    assert {item.source_commit for item in get_journeys()} == {
        summary["journey_source_commit"], summary["usd_source_commit"]}
    export = render_seed(CTX.reference_date)
    assert summary["source_commit"] in export
    assert summary["journey_source_commit"] in export


def test_new_scope_offers_cannot_discount_products_from_other_variants_or_original_battery():
    from products.xgestion.offer_journeys.catalog import get_journeys
    from products.xgestion.seeds.engine import catalog

    allowed = {}
    for journey in get_journeys():
        for declared in journey.variants:
            for offer in declared.offers:
                allowed.setdefault(offer.id, set()).update(product.id for product in declared.products)
    tables = {table.name: table.rows for table in catalog(CTX)}
    fields = {1: "artUbicacion", 2: "artFamilia", 3: "artSubfamilia", 4: "artId", 5: "artMarca"}
    for offer in tables["ofertas"]:
        if offer["ofeId"] not in allowed or offer["ofeTipo"] not in fields:
            continue
        scope = fields[offer["ofeTipo"]]
        reached = {product["artId"] for product in tables["articulos"]
                   if str(product[scope]).casefold() == str(offer["ofeCodigo"]).casefold()}
        assert reached <= allowed[offer["ofeId"]], offer["ofeNombre"]
