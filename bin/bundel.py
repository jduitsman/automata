#!/usr/bin/env python3
"""Bouwt een editie: voorblad + inhoudsopgave + inhoud, met bladwijzers,
klikbare inhoudsopgave en doorlopende paginanummers."""
import html
import os
import subprocess
import sys

import fitz

SCRATCH = os.path.dirname(os.path.abspath(__file__))
TEAL = (0.059, 0.239, 0.227)
GRIJS = (0.42, 0.47, 0.45)
VOORWERK_BLADEN = 2          # voorblad + inhoudsopgave


def paginas_van(pdf, koppen):
    """{kop: 0-gebaseerd paginanummer} — eerste pagina waarop de kop staat."""
    uit = {}
    with fitz.open(pdf) as d:
        for kop in koppen:
            for pno, page in enumerate(d):
                if page.search_for(kop, quads=False):
                    uit[kop] = pno
                    break
    return uit


def render(html_pad, pdf_pad):
    subprocess.run(["node", os.path.join(SCRATCH, "print.js"), html_pad],
                   check=True, capture_output=True)
    os.replace(html_pad[:-5] + ".pdf", pdf_pad)


def maak_voorwerk(velden, items, pdf_uit):
    sjabloon = open(os.path.join(SCRATCH, "voorwerk.html"), encoding="utf-8").read()
    rijen = []
    for deel, regels in items:
        if deel:
            rijen.append(f'<div class="deel">{html.escape(deel)}</div>')
        rijen.append('<ol class="ih">')
        for titel, blz in regels:
            rijen.append(
                f'<li><span class="t">{html.escape(titel)}</span>'
                f'<span class="stip"></span><span class="p">{blz}</span></li>')
        rijen.append("</ol>")
    velden = {**velden, "__ITEMS__": "\n".join(rijen)}
    for k, v in velden.items():
        sjabloon = sjabloon.replace(k, v)
    tmp = os.path.join(SCRATCH, "_voorwerk.html")
    open(tmp, "w", encoding="utf-8").write(sjabloon)
    render(tmp, pdf_uit)


def bouw(uit, velden, ih_items, bronnen, bladwijzers, springpunten):
    """bronnen: [(pad, van, tot)] · bladwijzers: [(niveau, titel, pagina)]"""
    voorwerk = os.path.join(SCRATCH, "_voorwerk.pdf")
    maak_voorwerk(velden, ih_items, voorwerk)

    doc = fitz.open(voorwerk)
    if doc.page_count != VOORWERK_BLADEN:
        print(f"  ! voorwerk is {doc.page_count} blz, verwacht {VOORWERK_BLADEN}")
    for pad, a, b in bronnen:
        with fitz.open(pad) as bron:
            doc.insert_pdf(bron, from_page=a, to_page=b)

    # paginanummers, vanaf de eerste inhoudspagina
    for pno in range(VOORWERK_BLADEN, doc.page_count):
        page = doc[pno]
        r = page.rect
        page.draw_line(fitz.Point(40, r.height - 30), fitz.Point(r.width - 40, r.height - 30),
                       color=(0.87, 0.84, 0.77), width=0.6)
        page.insert_text(fitz.Point(40, r.height - 19), "Automata voor Staatsbosbeheer",
                         fontname="helv", fontsize=8.5, color=GRIJS)
        nr = str(pno + 1)
        page.insert_text(fitz.Point(r.width - 40 - fitz.get_text_length(nr, "hebo", 10), r.height - 19),
                         nr, fontname="hebo", fontsize=10, color=TEAL)

    # klikbare inhoudsopgave
    for titel, blz in springpunten:
        for rect in doc[1].search_for(titel):
            doc[1].insert_link({"kind": fitz.LINK_GOTO, "page": blz - 1,
                                "from": fitz.Rect(rect.x0 - 30, rect.y0 - 3,
                                                  doc[1].rect.width - 40, rect.y1 + 3)})

    doc.set_toc([[n, t, p] for n, t, p in bladwijzers])
    doc.save(uit, garbage=4, deflate=True)
    doc.close()
    return uit


def koppen_op_grootte(pdf, min_grootte, overslaan=()):
    """[(tekst, 0-gebaseerde pagina)] — koppen herkend aan hun tekstgrootte.
    Regels van één kop die over meerdere spans lopen worden samengevoegd."""
    uit = []
    with fitz.open(pdf) as d:
        for pno, page in enumerate(d):
            for blok in page.get_text("dict")["blocks"]:
                stukken = [s["text"].strip()
                           for lijn in blok.get("lines", [])
                           for s in lijn["spans"]
                           if s["text"].strip() and round(s["size"], 1) >= min_grootte]
                if not stukken:
                    continue
                tekst = " ".join(stukken).replace("  ", " ").strip()
                if tekst in overslaan:
                    continue
                uit.append((tekst.capitalize(), pno))
    return uit
