#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genererer Pydantic v2-modeller fra DTDL v2 (REC/Brick m.fl.), uten stubs/duplikater.

Bruk:
  python dtdl_to_pydantic.py \
    --input ./Source/DTDLv2 \
    --out ./rec_brick_models.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set

from ruamel.yaml import YAML

# ----------------------------
# Konfig / mapping
# ----------------------------

PRIMITIVE_MAP: Dict[str, str] = {
    "boolean": "bool",
    "integer": "int",
    "double": "float",
    "float": "float",
    "long": "int",
    "string": "str",
    "dateTime": "datetime.datetime",
    "duration": "datetime.timedelta",
    "time": "datetime.time",
    "date": "datetime.date",
    # DTDL geospatial (forenklet):
    "geopoint": "tuple[float, float]",
}

SAFE_NAME_RE = re.compile(r"[^0-9a-zA-Z_]")
RESERVED = {
    "class", "def", "return", "raise", "from", "import", "global", "nonlocal",
    "as", "pass", "lambda", "yield", "match", "case", "if", "elif", "else",
    "for", "while", "try", "except", "finally", "with", "in", "is", "and",
    "or", "not", "True", "False", "None"
}

def safe_ident(name: str) -> str:
    s = SAFE_NAME_RE.sub("_", name)
    if re.match(r"^[0-9]", s):
        s = f"_{s}"
    if s in RESERVED:
        s = s + "_"
    return s

def dtmi_to_class(dtmi: str) -> str:
    """
    dtmi:org:w3id:rec:RealEstate;1 -> Rec_RealEstate
    dtmi:org:brickschema:schema:Brick:Room;1 -> Brick_Room
    ellers: siste segment før ; -> ident
    """
    try:
        core = dtmi.split(":")
        last = core[-1].split(";")[0] if core else "Type"
        if "rec" in core or "w3id" in core:
            return f"Rec_{safe_ident(last)}"
        if "brickschema" in core or "Brick" in core:
            return f"Brick_{safe_ident(last)}"
        return safe_ident(last)
    except Exception:
        return "UnknownType"

def _get_at_type(obj: Any) -> Optional[str]:
    t = None
    if isinstance(obj, dict):
        t = obj.get("@type") or obj.get("type")
        if isinstance(t, list):
            t = t[0] if t else None
    return t

def _is_interface(m: Dict[str, Any]) -> bool:
    t = m.get("@type") or m.get("type")
    if isinstance(t, list):
        return "Interface" in t
    return t == "Interface"

def schema_to_type(
    s: Any,
    known_enums: Dict[str, str],
    known_objects: Dict[str, str],
    *,
    current_cls: str = "Type",
    current_prop: str = "field",
) -> Tuple[str, List[str]]:
    """
    Returnerer (py_type, helper_defs) for en DTDL 'schema'.
    Håndterer primitives, Enum/Object/Array/Map, og referanser til lokale schemas.
    """
    helpers: List[str] = []

    # 1) Streng: primitive eller referanse til lokalt schema-id
    if isinstance(s, str):
        if s in PRIMITIVE_MAP:
            return PRIMITIVE_MAP[s], helpers
        if s in known_enums:
            return known_enums[s], helpers
        if s in known_objects:
            return known_objects[s], helpers
        if s.startswith("dtmi:"):
            print(
                f"WARN: Uoppløst schema-referanse '{s}' (ikke i lokale schemas for {current_cls}.{current_prop})",
                file=sys.stderr,
            )
        return "Any", helpers

    # 2) Dict: eksplisitt schema
    if isinstance(s, dict):
        t = _get_at_type(s)

        # Enum
        if t == "Enum":
            enum_name = safe_ident(s.get("name") or f"{current_cls}_{current_prop}_Enum")
            enum_members = s.get("enumValues", [])
            members = []
            for ev in enum_members:
                mname = safe_ident(str(ev.get("name") or ev.get("displayName") or ev.get("value") or "Unknown"))
                raw = ev.get("value")
                if raw is None:
                    raw = ev.get("name") or ev.get("displayName") or mname
                mv = json.dumps(raw)
                members.append(f"    {mname} = {mv}")
            enum_cls = f"class {enum_name}(Enum):\n" + ("\n".join(members) if members else "    pass") + "\n"
            helpers.append(enum_cls)
            return enum_name, helpers

        # Object
        if t == "Object":
            oname = safe_ident(s.get("name") or f"{current_cls}_{current_prop}_Object")
            fields = []
            for fp in s.get("fields", []):
                fname = safe_ident(fp["name"])
                f_schema = fp.get("schema", "string")
                ftype, h2 = schema_to_type(
                    f_schema, known_enums, known_objects,
                    current_cls=current_cls, current_prop=f"{current_prop}_{fname}"
                )
                helpers += h2
                fields.append(f"    {fname}: Optional[{ftype}] = None")
            pobj = f"class {oname}(BaseModel):\n" + ("\n".join(fields) if fields else "    pass") + "\n"
            helpers.append(pobj)
            return oname, helpers

        # Array
        if t == "Array":
            es = s.get("elementSchema", "string")
            etype, h2 = schema_to_type(
                es, known_enums, known_objects, current_cls=current_cls, current_prop=f"{current_prop}_item"
            )
            helpers += h2
            return f"List[{etype}]", helpers

        # Map (DTDL v2: mapKey/mapValue). Fallback: valueSchema.
        if t == "Map":
            mv = s.get("mapValue") or s.get("valueSchema")
            if mv is None:
                print("WARN: Map uten mapValue/valueSchema:", s, file=sys.stderr)
                return "Dict[str, Any]", helpers
            if isinstance(mv, dict):
                mv_schema = mv.get("schema", "string")
            else:
                mv_schema = mv
            vtype, h2 = schema_to_type(
                mv_schema, known_enums, known_objects, current_cls=current_cls, current_prop=f"{current_prop}_value"
            )
            helpers += h2
            return f"Dict[str, {vtype}]", helpers

        # Fallback: prøv "schema"-feltet hvis ukjent type
        if "schema" in s:
            return schema_to_type(
                s["schema"], known_enums, known_objects, current_cls=current_cls, current_prop=current_prop
            )

    # 3) Default
    return "Any", helpers

def load_models(path: Path) -> List[Dict[str, Any]]:
    """
    Leser alle .json/.jsonld/.yaml/.yml og flater ut arrays av modeller.
    Filtrerer til Interface-typer.
    """
    yaml = YAML(typ="safe")
    out: List[Any] = []
    for p in path.rglob("*"):
        if not p.is_file():
            continue
        suffix = p.suffix.lower()
        try:
            if suffix in (".json", ".jsonld", ".dtdl.json"):
                out.append(json.loads(p.read_text(encoding="utf-8")))
            elif suffix in (".yml", ".yaml"):
                out.append(yaml.load(p.read_text(encoding="utf-8")))
        except Exception as e:
            print(f"WARN: Kunne ikke lese {p}: {e}", file=sys.stderr)

    # Flatten
    flat: List[Dict[str, Any]] = []
    for item in out:
        if isinstance(item, list):
            flat.extend([x for x in item if isinstance(x, dict)])
        elif isinstance(item, dict):
            flat.append(item)

    # Filtrer til Interface
    interfaces = [m for m in flat if _is_interface(m)]
    return interfaces

def build_index(models: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    by_id: Dict[str, Dict[str, Any]] = {}
    for m in models:
        _id = m.get("@id") or m.get("id")
        if _id:
            by_id[_id] = m
    return by_id

def infer_title(m: Dict[str, Any]) -> str:
    name = m.get("displayName") or m.get("name")
    if isinstance(name, dict):
        try:
            name = next(iter(name.values()))
        except Exception:
            name = None
    if not name:
        _id = m.get("@id", "")
        name = _id.split(":")[-1].split(";")[0] if _id else "Interface"
    return str(name)

# --------- Topologisk sort (enkeltarv) ---------

def first_extends_class(m: Dict[str, Any]) -> Optional[str]:
    ext = m.get("extends")
    if isinstance(ext, str):
        return dtmi_to_class(ext)
    if isinstance(ext, list):
        for e in ext:
            if isinstance(e, str):
                return dtmi_to_class(e)
    return None

def topo_order(models: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Topologisk sorter interfaces slik at baseklassen kommer før subklassen.
    Bruker KUN første extends (enkeltarv).
    """
    # map: class_name -> model
    name_to_model: Dict[str, Dict[str, Any]] = {}
    for m in models:
        mid = m.get("@id")
        if not mid:
            continue
        name_to_model[dtmi_to_class(mid)] = m

    visited: Set[str] = set()
    temp: Set[str] = set()
    order: List[str] = []

    def visit(cls_name: str):
        if cls_name in visited:
            return
        if cls_name in temp:
            # Syklisk arv — uvanlig i DTDL; bryt syklusen
            print(f"WARN: Cyclic extends detected at {cls_name}; breaking cycle", file=sys.stderr)
            return
        temp.add(cls_name)
        m = name_to_model.get(cls_name)
        if m:
            base = first_extends_class(m)
            if base:
                visit(base)
        temp.remove(cls_name)
        visited.add(cls_name)
        order.append(cls_name)

    for cls_name in list(name_to_model.keys()):
        visit(cls_name)

    # returnerer models i riktig rekkefølge
    return [name_to_model[n] for n in order if n in name_to_model]

# --------- Generator ---------

def generate(out_path: Path, in_path: Path):
    models = load_models(in_path)
    idx = build_index(models)

    # Topologisk ordning (base før derived)
    models = topo_order(models)

    # Samle lokale schemas per interface (@id -> { schema_id -> schema_obj/str })
    interface_schemas: Dict[str, Dict[str, Any]] = {}
    for m in models:
        sid = m.get("@id")
        schemas: Dict[str, Any] = {}
        for sc in m.get("schemas", []):
            if isinstance(sc, dict):
                scid = sc.get("@id") or sc.get("name") or f"{sid}#schema{len(schemas)+1}"
                schemas[str(scid)] = sc
            elif isinstance(sc, str):
                schemas[str(sc)] = sc
        interface_schemas[sid] = schemas

    header = textwrap.dedent(f"""
    # AUTO-GENERATED by dtdl_to_pydantic.py — do not edit by hand
    # Source directory: {in_path}
    from __future__ import annotations
    from pydantic import BaseModel, Field, ConfigDict
    from typing import Optional, List, Dict, Any
    from enum import Enum
    import datetime

    __all__ = []

    class DtMetadata(BaseModel):
        model_config = ConfigDict(extra='allow')

    class DtdlBase(BaseModel):
        \"\"\"Felles base for alle DTDL-baserte modeller.\"\"\"
        dtId: Optional[str] = Field(default=None, alias='$dtId')
        metadata: Optional[DtMetadata] = Field(default=None, alias='$metadata')
        model: Optional[str] = Field(default=None, alias='$model')
    """).lstrip()

    classes: List[str] = []
    exports: List[str] = []

    for m in models:
        mid = m.get("@id")
        if not mid:
            continue

        cls_name = dtmi_to_class(mid)

        # ENKELTARV: velg KUN første extends, og legg DtdlBase sist
        base = first_extends_class(m)
        if base:
            bases: List[str] = [base, "DtdlBase"]
        else:
            bases = ["DtdlBase"]

        # Lokale schemas for enum/object
        known_enums: Dict[str, str] = {}
        known_objects: Dict[str, str] = {}
        local_helpers: List[str] = []

        for scid, sc in interface_schemas.get(mid, {}).items():
            if isinstance(sc, dict):
                pyname, helpers = schema_to_type(
                    sc, known_enums, known_objects,
                    current_cls=cls_name, current_prop=sc.get("name") or "schema"
                )
                t = _get_at_type(sc)
                if t == "Enum":
                    known_enums[scid] = pyname
                elif t == "Object":
                    known_objects[scid] = pyname
                local_helpers += helpers

        fields: List[str] = []

        # contents: Property / Relationship / Component / Telemetry / Command
        for c in m.get("contents", []):
            ctype = c.get("@type") or c.get("type")
            if isinstance(ctype, list):
                ctype = ctype[0]
            cname = safe_ident(c["name"])

            if ctype == "Property":
                sch = c.get("schema", "string")
                pytype, helpers = schema_to_type(
                    sch, known_enums, known_objects, current_cls=cls_name, current_prop=c['name']
                )
                local_helpers += helpers
                ge = c.get("minValue")
                le = c.get("maxValue")
                unit = c.get("unit")
                extras = []
                if ge is not None: extras.append(f"ge={ge}")
                if le is not None: extras.append(f"le={le}")
                if unit is not None: extras.append(f"json_schema_extra={{'unit': {json.dumps(unit)}}}")
                extra_s = (", " + ", ".join(extras)) if extras else ""
                fields.append(f"{cname}: Optional[{pytype}] = Field(default=None, alias='{c['name']}'{extra_s})")

            elif ctype == "Relationship":
                rprops = c.get("properties", [])
                if rprops:
                    rname = f"{cls_name}_{safe_ident(c['name'])}_Rel"
                    rfields = []
                    for i, rp in enumerate(rprops):
                        if isinstance(rp, dict):
                            pname = safe_ident(rp.get("name") or f"prop_{i+1}")
                            rpschema = rp.get("schema", "string")
                        else:
                            pname = f"prop_{i+1}"
                            rpschema = rp
                        rptype, rhelpers = schema_to_type(
                            rpschema, known_enums, known_objects, current_cls=cls_name, current_prop=f"{c['name']}_{pname}"
                        )
                        local_helpers += rhelpers
                        rfields.append(f"    {pname}: Optional[{rptype}] = None")
                    rel_payload = (
                        f"class {rname}(BaseModel):\n"
                        + ("\n".join(rfields) if rfields else "    pass")
                        + "\n"
                    )
                    local_helpers.append(rel_payload)
                    fields.append(f"{cname}: Optional[List[{rname}]] = Field(default=None, alias='{c['name']}')")
                else:
                    fields.append(f"{cname}: Optional[List[str]] = Field(default=None, alias='{c['name']}')  # dtmi targets")

            elif ctype == "Component":
                target = c.get("schema")
                comp_type = dtmi_to_class(target) if isinstance(target, str) else "Any"
                fields.append(f"{cname}: Optional[{comp_type}] = Field(default=None, alias='{c['name']}')")

            elif ctype == "Telemetry":
                sch = c.get("schema", "string")
                pytype, helpers = schema_to_type(
                    sch, known_enums, known_objects, current_cls=cls_name, current_prop=c['name']
                )
                local_helpers += helpers
                unit = c.get("unit")
                extra = f", json_schema_extra={{'unit': {json.dumps(unit)}}}" if unit else ""
                fields.append(f"{cname}: Optional[{pytype}] = Field(default=None, alias='{c['name']}'{extra})")

            elif ctype == "Command":
                req = c.get("request")
                res = c.get("response")
                if req:
                    r_schema = req.get("schema", "string") if isinstance(req, dict) else req
                    rtype, rhelpers = schema_to_type(
                        r_schema, known_enums, known_objects, current_cls=cls_name, current_prop=f"{c['name']}_request"
                    )
                    local_helpers += rhelpers
                    fields.append(
                        f"{cname}_request: Optional[{rtype}] = Field(default=None, alias='{c['name']}.request')"
                    )
                if res:
                    s_schema = res.get("schema", "string") if isinstance(res, dict) else res
                    stype, shelpers = schema_to_type(
                        s_schema, known_enums, known_objects, current_cls=cls_name, current_prop=f"{c['name']}_response"
                    )
                    local_helpers += shelpers
                    fields.append(
                        f"{cname}_response: Optional[{stype}] = Field(default=None, alias='{c['name']}.response')"
                    )
                if not req and not res:
                    fields.append(f"{cname}: Optional[bool] = Field(default=None, alias='{c['name']}')")

            else:
                print(f"WARN: Ukjent content @type '{ctype}' i {mid}", file=sys.stderr)

        title = infer_title(m)
        doc = f'    """DTMI: {mid} — {title}"""'

        cls_lines = [f"class {cls_name}({', '.join(bases)}):", doc]
        if fields:
            for f in fields:
                cls_lines.append(f"    {f}")
        else:
            cls_lines.append("    pass")

        if local_helpers:
            classes.extend(local_helpers)
        classes.append("\n".join(cls_lines))
        exports.append(cls_name)

    footer = "\n__all__ += [" + ", ".join([f'\"{e}\"' for e in exports]) + "]\n"

    (out_path).write_text(header + "\n\n".join(classes) + footer, encoding="utf-8")
    print(f"Generated: {out_path}  ({len(exports)} classes)")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to folder with DTDL v2 models (JSON/YAML)")
    ap.add_argument("--out", required=True, help="Output .py file with pydantic models")
    args = ap.parse_args()

    in_path = Path(args.input)
    out_path = Path(args.out)
    if not in_path.exists():
        print(f"Input path not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    generate(out_path, in_path)

if __name__ == "__main__":
    main()