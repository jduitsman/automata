#!/usr/bin/env python3
"""Zet de invulvelden in de leerlingeditie: de denkvragen en de zelfevaluatie
uit het lesmateriaal (gemeten op de losse render, verschoven met het voorwerk),
plus naam/klas/datum op het voorblad."""
import json
import os
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fill import (INK, TEXTUAL, ensure_form_resources, rects_by_index,  # noqa: E402
                  regroup_radios, safe_name, set_pill_appearance, set_placeholder)

SCRATCH = os.path.dirname(os.path.abspath(__file__))
A = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
EDITIE = f"{A}/docs/automata-leerlingeditie.pdf"
VERSCHUIVING = 2          # voorblad + inhoudsopgave


def voorbladvelden(doc, used):
    """Naam / klas / datum op het voorblad, rechts van hun label."""
    page = doc[0]
    kolom = (page.rect.width - 2 * 39.7 - 2 * 14) / 3
    for label in ("Naam", "Klas", "Datum"):
        treffers = page.search_for(label)
        if not treffers:
            print(f"  ! label {label} niet gevonden op het voorblad")
            continue
        r = treffers[0]
        w = fitz.Widget()
        w.rect = fitz.Rect(r.x0, r.y1 + 2, r.x0 + kolom, r.y1 + 20)
        w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        w.field_name = safe_name(label.lower(), "veld", used)
        w.field_label = label
        w.border_width, w.fill_color = 0, None
        w.text_color, w.text_font, w.text_fontsize = INK, "Helv", 10.5
        page.add_widget(w)


def main():
    werk = os.path.join(SCRATCH, "ed-work")
    meta = json.load(open(os.path.join(werk, "index.fields.json")))
    geo = rects_by_index(os.path.join(werk, "index.marked.pdf"))
    doc = fitz.open(EDITIE)

    used, groepnamen, radio_kids, n = set(), {}, {}, 0
    voorbladvelden(doc, used)

    for f in meta["fields"]:
        hit = geo.get(f["idx"])
        if hit is None:
            continue
        pno, rect = hit
        page = doc[pno + VERSCHUIVING]
        kind, label = f["kind"], f["label"]

        w = fitz.Widget()
        w.rect, w.border_width, w.fill_color = rect, 0, None
        w.text_color, w.text_font = INK, "Helv"
        if label:
            w.field_label = label

        if kind == "radio":
            grp = f["group"] or f["key"] or f"keuze{f['idx']}"
            groepnamen.setdefault(grp, safe_name(grp, "keuze", used))
            w.field_type = fitz.PDF_WIDGET_TYPE_RADIOBUTTON
            w.field_name = groepnamen[grp]
            w.field_value, w.button_caption = False, "l"
        elif kind == "checkbox":
            w.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
            w.field_name = safe_name(f["key"] or label[:40], "vinkje", used)
            w.field_value, w.button_caption = False, "4"
        elif kind in TEXTUAL:
            w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
            w.field_name = safe_name(f["key"] or label[:40], "veld", used)
            if kind == "textarea" or rect.height > 30:
                w.field_flags, w.text_fontsize = fitz.PDF_TX_FIELD_IS_MULTILINE, 9
            else:
                w.text_fontsize = max(7.5, min(10.5, rect.height * 0.55))
        else:
            continue

        annot = page.add_widget(w)
        n += 1
        if f.get("proxy") and kind in ("radio", "checkbox"):
            set_pill_appearance(doc, annot.xref, rect)
        if kind == "radio":
            radio_kids.setdefault(groepnamen[grp], []).append((annot.xref, f["value"]))
        elif kind in TEXTUAL and f.get("placeholder"):
            set_placeholder(doc, annot.xref, f["placeholder"], w.text_fontsize,
                            bool(w.field_flags & fitz.PDF_TX_FIELD_IS_MULTILINE), rect.height)

    if radio_kids:
        regroup_radios(doc, radio_kids)
    ensure_form_resources(doc)
    doc.set_metadata({"title": "Automata voor Staatsbosbeheer — leerlingeditie",
                      "subject": "Invulbaar werkboek · Techniek havo 2"})
    doc.saveIncr() if False else doc.save(EDITIE + ".tmp", garbage=4, deflate=True)
    doc.close()
    os.replace(EDITIE + ".tmp", EDITIE)
    print(f"  ✓ {n} invulvelden uit het lesmateriaal + 3 op het voorblad")
    print(f"    radiogroepen: {len(radio_kids)}")


if __name__ == "__main__":
    main()
