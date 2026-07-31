#!/usr/bin/env python3
"""Zet de gemeten veldposities om in echte AcroForm-velden in de schone PDF."""
import json
import os
import re
import sys
import glob

import fitz

INK = (0.09, 0.13, 0.18)
MAGIC_R = 254
TEXTUAL = {"text", "number", "tel", "email", "url", "search", "date", "password", "textarea"}


def rects_by_index(marked_path):
    """{veldindex: (paginanummer, fitz.Rect)} uit de gemarkeerde render."""
    found = {}
    with fitz.open(marked_path) as doc:
        for pno, page in enumerate(doc):
            for d in page.get_drawings():
                fill = d.get("fill")
                if not fill:
                    continue
                r, g, b = (round(v * 255) for v in fill)
                if r != MAGIC_R:
                    continue
                idx = (g << 8) | b
                rect = d["rect"]
                prev = found.get(idx)
                # bij een pagina-afbreking: neem het grootste stuk
                if prev is None or rect.get_area() > prev[1].get_area():
                    found[idx] = (pno, rect)
    return found


def safe_name(raw, fallback, used):
    name = re.sub(r"[^0-9A-Za-z_-]+", "_", (raw or "").strip()).strip("_")
    if not name or name[0].isdigit():
        name = f"{fallback}_{name}" if name else fallback
    base, n = name, 2
    while name in used:
        name, n = f"{base}_{n}", n + 1
    used.add(name)
    return name


def pdf_name(raw, fallback):
    n = re.sub(r"[^0-9A-Za-z_-]+", "", (raw or "")) or fallback
    return n[:32]


def regroup_radios(doc, groups):
    """PyMuPDF zet elke radio als los veld met exportwaarde /Yes neer — dan
    schakelen ze samen. Hier worden ze één /Btn-veld met /Kids en per knop een
    eigen exportwaarde, zoals een radiogroep hoort te zijn."""
    cat = doc.pdf_catalog()
    fields = re.findall(r"\d+ 0 R", doc.xref_get_key(cat, "AcroForm/Fields")[1])
    for name, kids in groups.items():
        exports, seen = [], set()
        for i, (_xref, value) in enumerate(kids):
            e = pdf_name(value, f"optie{i + 1}")
            while e in seen:
                e = f"{e}_{i + 1}"
            seen.add(e)
            exports.append(e)

        parent = doc.get_new_xref()
        refs = " ".join(f"{x} 0 R" for x, _ in kids)
        doc.update_object(
            parent,
            f"<</FT/Btn/Ff 32768/T({name})/V/Off/DV/Off/Kids[{refs}]>>",
        )
        for (xref, _), export in zip(kids, exports):
            ap = doc.xref_get_key(xref, "AP/N")[1]
            doc.xref_set_key(xref, "AP/N", re.sub(r"/Yes\b", "/" + export, ap))
            doc.xref_set_key(xref, "AS", "/Off")
            for key in ("T", "FT", "Ff", "V", "DV"):
                doc.xref_set_key(xref, key, "null")
            doc.xref_set_key(xref, "Parent", f"{parent} 0 R")
            fields = [r for r in fields if r != f"{xref} 0 R"]
        fields.append(f"{parent} 0 R")
    doc.xref_set_key(cat, "AcroForm/Fields", "[" + " ".join(fields) + "]")


def pdf_string(text):
    """Nederlandse tekst als PDF-literal in WinAnsi (— en … horen erbij)."""
    raw = text.encode("cp1252", "replace")
    out = bytearray(b"(")
    for byte in raw:
        if byte in b"()\\":
            out += b"\\" + bytes([byte])
        elif byte < 32 or byte > 126:
            out += b"\\%03o" % byte
        else:
            out.append(byte)
    return bytes(out + b")").decode("latin-1")


PLACEHOLDER_GREY = "0.56 0.58 0.61 rg"


def set_placeholder(doc, xref, text, fontsize, multiline, height):
    """Grijze hinttekst in de appearance van een leeg tekstveld. Zodra de
    leerling typt, bouwt de viewer de appearance opnieuw op en verdwijnt hij —
    precies zoals een placeholder in de browser."""
    kind, ref = doc.xref_get_key(xref, "AP/N")
    if kind != "xref":
        return
    apx = int(ref.split()[0])
    stream = doc.xref_stream(apx).decode("latin-1")
    if "Tj" in stream:
        return
    baseline = height - fontsize * 1.15 if multiline else None
    body = f"/Helv {fontsize:.3f} Tf\n{PLACEHOLDER_GREY}\n{pdf_string(text)} Tj\n"

    def rewrite(m):
        y = f"{baseline:.3f}" if baseline is not None else m.group(2)
        return f"\n2 {y} Td\n{body}"

    new, n = re.subn(r"\n([-\d.]+) ([-\d.]+) Td\n", rewrite, stream, count=1)
    if n:
        doc.update_stream(apx, new.encode("latin-1"))


def set_pill_appearance(doc, xref, rect):
    """Aangevinkt-uiterlijk voor een keuzeknop die zelf het hele labelvlak is:
    een dikke blauwe omlijning met een stip links, in plaats van een vinkje
    midden over de tekst heen."""
    kind, ref = doc.xref_get_key(xref, "AP/N")
    if kind != "dict":
        return
    on = re.search(r"/(?!Off\b)([A-Za-z0-9_-]+) (\d+) 0 R", ref)
    if not on:
        return
    w, h, pad = rect.width, rect.height, 1.4
    cy, r = h / 2, 1.9
    stream = (
        "q\n0.118 0.373 0.549 RG 0.118 0.373 0.549 rg\n1.6 w\n"
        f"{pad} {pad} {w - 2 * pad:.2f} {h - 2 * pad:.2f} re\nS\n"
        f"{5.2 - r:.2f} {cy - r:.2f} {2 * r:.2f} {2 * r:.2f} re\nf\nQ\n"
    )
    # eigen appearance-object: PyMuPDF deelt streams tussen gelijke widgets en
    # deze knoppen verschillen in breedte
    apx = doc.get_new_xref()
    doc.update_object(apx, "<</Type/XObject/Subtype/Form/Matrix[1 0 0 1 0 0]"
                           f"/BBox[0 0 {w:.3f} {h:.3f}]/Resources<<>>>>")
    doc.update_stream(apx, stream.encode("latin-1"), new=True)
    doc.xref_set_key(xref, "AP/N",
                     ref.replace(f"{on.group(2)} 0 R", f"{apx} 0 R"))


def ensure_form_resources(doc):
    """AcroForm /DR + /DA — nodig zodra een viewer de appearance zelf hertekent."""
    cat = doc.pdf_catalog()
    helv = doc.get_new_xref()
    doc.update_object(helv, "<</Type/Font/Subtype/Type1/BaseFont/Helvetica"
                            "/Encoding/WinAnsiEncoding>>")
    zadb = doc.get_new_xref()
    doc.update_object(zadb, "<</Type/Font/Subtype/Type1/BaseFont/ZapfDingbats>>")
    doc.xref_set_key(cat, "AcroForm/DR",
                     f"<</Font<</Helv {helv} 0 R/ZaDb {zadb} 0 R>>>>")
    doc.xref_set_key(cat, "AcroForm/DA", "(0 g /Helv 0 Tf)")
    doc.xref_set_key(cat, "AcroForm/NeedAppearances", "false")


def build(base, workdir, outdir):
    meta = json.load(open(os.path.join(workdir, f"{base}.fields.json")))
    geo = rects_by_index(os.path.join(workdir, f"{base}.marked.pdf"))
    doc = fitz.open(os.path.join(workdir, f"{base}.clean.pdf"))

    used, group_names, radio_kids, added, skipped = set(), {}, {}, 0, []

    for f in meta["fields"]:
        hit = geo.get(f["idx"])
        if hit is None:
            skipped.append(f["key"] or f["idx"])
            continue
        pno, rect = hit
        page = doc[pno]
        kind, label = f["kind"], f["label"]

        w = fitz.Widget()
        w.rect = rect
        w.border_width = 0
        w.fill_color = None
        w.text_color = INK
        w.text_font = "Helv"
        if label:
            w.field_label = label

        if kind == "radio":
            grp = f["group"] or f["key"] or f"radio{f['idx']}"
            if grp not in group_names:
                group_names[grp] = safe_name(grp, "keuze", used)
            w.field_type = fitz.PDF_WIDGET_TYPE_RADIOBUTTON
            w.field_name = group_names[grp]
            w.field_value = False
            w.button_caption = "l"  # ZapfDingbats: gevulde stip
        elif kind == "checkbox":
            w.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
            w.field_name = safe_name(f["key"] or label[:40], "vinkje", used)
            w.field_value = False
            w.button_caption = "4"  # ZapfDingbats: vinkje
        elif kind in TEXTUAL:
            w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
            w.field_name = safe_name(f["key"] or label[:40], "veld", used)
            h = rect.height
            multiline = kind == "textarea" or h > 30
            if multiline:
                w.field_flags = fitz.PDF_TX_FIELD_IS_MULTILINE
                w.text_fontsize = 9
            else:
                w.text_fontsize = max(7.5, min(10.5, h * 0.55))
        else:
            skipped.append(f"{f['key']}({kind})")
            continue

        annot = page.add_widget(w)
        added += 1
        if f.get("proxy") and kind in ("radio", "checkbox"):
            set_pill_appearance(doc, annot.xref, rect)
        if kind == "radio":
            radio_kids.setdefault(group_names[grp], []).append((annot.xref, f["value"]))
        elif kind in TEXTUAL and f.get("placeholder"):
            set_placeholder(doc, annot.xref, f["placeholder"],
                            w.text_fontsize, multiline, rect.height)

    if radio_kids:
        regroup_radios(doc, radio_kids)
    ensure_form_resources(doc)

    doc.set_metadata({
        "title": meta.get("title", base),
        "subject": "Invulbaar werkblad — HAVO-P",
        "producer": "Chrome + PyMuPDF",
    })
    out = os.path.join(outdir, base + ".pdf")
    doc.save(out, garbage=4, deflate=True)
    doc.close()
    return added, skipped, out


if __name__ == "__main__":
    workdir, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    only = sys.argv[3] if len(sys.argv) > 3 else None
    for path in sorted(glob.glob(os.path.join(workdir, "*.clean.pdf"))):
        base = os.path.basename(path)[: -len(".clean.pdf")]
        if only and only != base:
            continue
        n, skipped, out = build(base, workdir, outdir)
        note = f"  overgeslagen: {skipped}" if skipped else ""
        print(f"  ✓ {base:32s} {n:3d} velden{note}")
