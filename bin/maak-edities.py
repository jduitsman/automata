#!/usr/bin/env python3
"""Leerlingeditie en docenteneditie als twee losse documenten."""
import os
import sys

import fitz

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bundel import bouw, koppen_op_grootte, paginas_van, VOORWERK_BLADEN  # noqa: E402

A = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
LES = f"{os.path.dirname(os.path.abspath(__file__))}/ed-work/index.clean.pdf"
BOUW = f"{A}/docs/bouwplaat-proefmodel.pdf"
HAND = f"{A}/docentenhandleiding.pdf"
FOTO = f"{A}/docs/afbeeldingen/houthakker-vos.jpg"

SECTIES = [
    "Context & aanleiding", "De opdracht", "Leerdoelen", "Deelvragen",
    "Producten & deliverables", "Planning", "Achtergrond & vakkennis",
    "Randvoorwaarden & veiligheid", "Opdrachten & denkvragen per les",
    "Beoordelingsrubric", "Check jezelf",
]
TITELS = {"Check jezelf": "Check jezelf — zelfevaluatie"}

# ─────────────────────────────── leerlingeditie ───────────────────────────────
les_blz = len(fitz.open(LES))
gevonden = paginas_van(LES, SECTIES)
ontbreekt = [s for s in SECTIES if s not in gevonden]
if ontbreekt:
    print("  ! kop niet teruggevonden:", ontbreekt)

regels = [(TITELS.get(s, s), gevonden[s] + 1 + VOORWERK_BLADEN)
          for s in SECTIES if s in gevonden]
bouwplaat_start = VOORWERK_BLADEN + les_blz + 1
regels_bouw = [("Bouwplaat proefmodel — blad 1 t/m 5", bouwplaat_start)]

bouw(
    uit=f"{A}/docs/automata-leerlingeditie.pdf",
    velden={
        "__VAK__": "Techniek · havo 2", "__DUUR__": "8 lessen · 100 min",
        "__EDITIE__": "Leerlingeditie", "__FOTO__": FOTO,
        "__INVUL__": '<div class="invul">'
                     '<div><span class="lbl">Naam</span><span class="lijn"></span></div>'
                     '<div><span class="lbl">Klas</span><span class="lijn"></span></div>'
                     '<div><span class="lbl">Datum</span><span class="lijn"></span></div></div>',
        "__ONDER__": "Jij bouwt een houten machientje: draai aan de slinger en jouw figuur "
                     "komt tot leven. Hij pikt, klapt met zijn vleugels, hakt hout of gaat "
                     "open als een bloem — en hij maakt minimaal twee bewegingen op één as.",
        "__IHINTRO__": "Dit boekje is je werkboek voor acht lessen. Je kunt het invullen op "
                       "je laptop of uitprinten en met pen invullen. Klik op een hoofdstuk "
                       "om er meteen naartoe te gaan.",
        "__TIP__": "<b>De video en de 3D-animaties staan online.</b> Die kunnen niet in een "
                   "pdf: kijk op <b>jduitsman.github.io/automata</b> voor het bewegende "
                   "voorbeeld en om in de kast rond te kijken.",
    },
    ih_items=[("Lesmateriaal", regels), ("Bijlage", regels_bouw)],
    bronnen=[(LES, 0, les_blz - 1), (BOUW, 0, len(fitz.open(BOUW)) - 1)],
    bladwijzers=([[1, "Voorblad", 1], [1, "Inhoud", 2]]
                 + [[1, t, p] for t, p in regels]
                 + [[1, "Bouwplaat proefmodel", bouwplaat_start]]),
    springpunten=regels + regels_bouw,
)
print(f"  ✓ leerlingeditie — {VOORWERK_BLADEN + les_blz + len(fitz.open(BOUW))} blz")

# ─────────────────────────────── docenteneditie ───────────────────────────────
hand_blz = len(fitz.open(HAND))
# koppen op tekstgrootte: zoeken op woorden vindt gewone tekst en zet de
# volgorde door elkaar
regels_h = [(t, p + 1 + VOORWERK_BLADEN)
            for t, p in koppen_op_grootte(HAND, 17.5,
                                          overslaan=("AUTOMATA VOOR STAATSBOSBEHEER",))]
if not regels_h:
    regels_h = [("Docentenhandleiding", VOORWERK_BLADEN + 1)]

bouw(
    uit=f"{A}/automata-docenteneditie.pdf",
    velden={
        "__VAK__": "Techniek · havo 2", "__DUUR__": "8 lessen · 100 min",
        "__EDITIE__": "Docenteneditie", "__FOTO__": FOTO, "__INVUL__": "",
        "__ONDER__": "Voorbereiding, timing per les, waar leerlingen vastlopen en hoe je "
                     "beoordeelt. Leg dit naast de leerlingeditie: die bevat de opdracht, "
                     "de denkvragen, de rubric en de zelfevaluatie.",
        "__IHINTRO__": "Dit is het docentmateriaal. Het hoort niet bij het leerlingmateriaal "
                       "en staat niet op de publieke website.",
        "__TIP__": "<b>Naast dit document hoort de leerlingeditie.</b> Daarin staan de "
                   "opdracht, de acht denkvragen met voorbeeldantwoorden, de rubric, de "
                   "zelfevaluatie en de bouwplaat.",
    },
    ih_items=[("Docentenhandleiding", regels_h)],
    bronnen=[(HAND, 0, hand_blz - 1)],
    bladwijzers=[[1, "Voorblad", 1], [1, "Inhoud", 2]] + [[1, t, p] for t, p in regels_h],
    springpunten=regels_h,
)
print(f"  ✓ docenteneditie — {VOORWERK_BLADEN + hand_blz} blz")
