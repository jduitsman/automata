# Review-rapport: Automata voor Eindhoven Zoo

**Beoordeeld op:** 2026-07-23
**Materialen bekeken:** `projectdocument.md`, `rubric.md`, `automata.html`, `docentenhandleiding.md`, `kerndoelen-automata-koppeling.csv`, `voorbeeld-leerlingwerk.md`, `feedback-voorbeeld.md`
**Programma:** Onderbouw havo 2 · Techniek — gekoppeld aan de **nieuwe SLO-kerndoelen** (Mens en natuur KD29/KD30, Kunst en cultuur KD40/41, Digitale geletterdheid KD21), *niet* aan de HAVO-P eindtermen.

> **Ankering.** Dit is een onderbouwproject, dus ik heb bewust níet tegen `references/eindtermen-technologie-groot.md` (bovenbouw HAVO-P) geankerd, maar tegen de kerndoelenkoppeling van het project. De exacte SLO-formuleringen heb ik niet regel-voor-regel tegen de bron-PDF (`bronnen/nieuwe kernoelen/…-2026-derde-druk.pdf`) kunnen leggen; controleer de letterlijke kerndoelteksten daar nog één keer tegen.

---

## In het kort

Dit is een sterk, praktisch en zorgvuldig uitgelijnd onderbouwproject. De recente ombouw naar **twee mechanische bewegingen op één as** is consequent doorgetrokken door document, rubric, HTML en docentenhandleiding, en maakt van "wrijving bij de tweede beweging oplossen" een scherpe, herkenbare rode draad. De constructive alignment is bijna voorbeeldig (elk leerdoel → een rubriccriterium → een kerndoel) en het formatieve ijkmateriaal (fictief leerlingwerk + modelfeedback) is uitzonderlijk goed. Het belangrijkste wat het sterker maakt is klein maar concreet: één blok docentinhoud lekt naar de leerlingpagina, en de peer-feedback komt in de leerlingplanning te laat om nog verwerkt te kunnen worden.

---

## Wat werkt goed

- **Bijna voorbeeldige constructive alignment.** De alignment-tabel in `docentenhandleiding.md` §9 koppelt elk van de 8 leerdoelen aan een rubriccriterium én aan een kerndoel. Geen leerdoel zonder toetsing, geen criterium zonder leerdoel.
- **Twee-bewegingen-op-één-as als rode draad.** De eis stuurt overal dezelfde kant op: rubriccriteria 1–4, de planning (les 2 "één as"), de vastlopers #2 en #3 in de handleiding en de differentiatie. Het typische leermoment — wrijving/speling, juist bij de tweede beweging — is daardoor overal geborgd (`rubric.md` crit 4; `docentenhandleiding.md` les 6 + vastloper #2).
- **Authentieke opdrachtgever + echte ontwerpvrijheid.** Eindhoven Zoo, tentoonstelling "Dieren in beweging" (`projectdocument.md` Context & aanleiding). Leerlingen kiezen zelf dier, bewegingen én mechanismen — geen bouwpakket. Past bij de docent-kernwaarde uit het profiel.
- **Iteratief ontwerpen expliciet ingebouwd.** mock-up → tekening → bouw → test → verbeter, met een helder "waarom eerst karton" (`projectdocument.md` → Achtergrond → "Van proefmodel naar hout").
- **Uitstekend formatief ijkmateriaal.** `voorbeeld-leerlingwerk.md` (fictieve, gemengd-sterke inzending van Noor & Sam) + `feedback-voorbeeld.md` vormen samen een *worked example* van hoe de rubric valt — inclusief een bewust ingebouwde tegenstrijdigheid (logboek zegt "bleef hangen", onderbouwing zegt "loopt soepel") die precies het leermoment blootlegt. Dit is zeldzaam goed onderbouwd.
- **Eerlijke kerndoelenkoppeling.** `kerndoelen-automata-koppeling.csv` claimt niet te veel: Sterk/Deels/Niet met bewijs per subkerndoel, een expliciet voorbehoud (kerndoelen worden over de hele onderbouw afgesloten), en concrete routes om KD30C (elektromotor) en KD21 (3D-print/laser) alsnog te raken.
- **Vorm voldoet aan de standaard.** Think-first + reveal per denkvraag (22×), géén leerling/docent-schakelaar, tekst over de volle bladbreedte (`.sheet` 1040px, geen smalle leeskolom), PDF-export + werkende print-CSS.

---

## Verbeterpunten

Prioriteit: **[must]** raakt de kern · **[should]** merkbare verbetering · **[could]** mooie extra.

### 🎯 Constructive alignment

- **[could]** Leerdoel 8 (samenwerken & feedback, 10% in de rubric) is maar los aan een kerndoel te koppelen.
  - *Waar:* `docentenhandleiding.md` §9, alignment-tabel — rij "8. Samenwerken…" → KD29D, KD40A.
  - *Waarom:* KD29D gaat over "hoe technologen systematisch werken" en KD40A over het iteratieve creatieve proces; samenwerken/feedback valt daar strikt genomen buiten. De koppeling suggereert nu een dekking die er niet echt is.
  - *Suggestie:* benoem in §9 dat criterium 7 een **brede/algemene vaardigheid** beoordeelt die buiten de vakkerndoelen valt (en koppel het eventueel aan een burgerschaps- of brede-vaardigheden-kerndoel als je dat in je programma gebruikt). Dan blijft de tabel eerlijk.

- **[could]** Kleine inconsistentie in de mechanismenlijst.
  - *Waar:* leerdoel 1 en de mechanismentabel noemen zes mechanismen inclusief **nokkenas**; de alignment-tabel en rubriccriterium 1 ("Uitstekend": nok, krukas, excenter, hefboom, tandwiel) laten nokkenas weg.
  - *Suggestie:* hanteer overal dezelfde lijst vaktermen, zodat leerdoel, rubric en verantwoording exact matchen.

### 🛠️ Activerende & praktijkgerichte didactiek

- **[could]** De 3D-mechanismenanimaties worden niet vanuit de leerlingpagina ontsloten.
  - *Waar:* `automata.html` les 1 verwijst naar "de mechanismen-demo's", maar er is geen link naar de bestaande animaties in `animaties/` (`automata-3d`, `automata-papegaai-3d`, `automata-olifant-3d`, `automata-leeuw-3d`, `automata-proefmodel-3d`, `kruk-drijfstang`).
  - *Waarom:* die demo's zijn precies wat les 1 nodig heeft om "leren zien welk mechanisme welke beweging maakt" te activeren; nu vindt de leerling ze niet zelfstandig. Past bij het docent-uitgangspunt "materiaal moet zelfstandig te volgen zijn".
  - *Suggestie:* link de animaties in de les-1-rij van de planning of in "Achtergrond → Mechanismen".

### 🔁 Formatief evalueren & feedback

- **[should]** Peer-feedback komt in de leerlingplanning te laat om nog te verwerken.
  - *Waar:* `projectdocument.md` / `automata.html` planning — les 8: "Presenteer aan 'de Zoo' en geef en verwerk feedback." De leerlingplanning kent vóór les 8 geen expliciet peer-feedbackmoment, terwijl `docentenhandleiding.md` (vastloper #6 + Timingrisico's) juist zegt: "plan de peer-feedback al in **les 6**, niet in les 8."
  - *Waarom:* feedback aan het eind is geen feed-forward meer — er is dan geen tijd om er iets mee te doen. Dat straft criterium 7 (feedback verwerken) én criterium 4. De leerlingplanning en de docentenhandleiding spreken elkaar hier tegen.
  - *Suggestie:* voeg aan de **les-6-rij** van de planning een expliciet peer-feedbackmoment toe ("wissel met een ander groepje: waar hapert hun tweede beweging, en wat kun jij vóór de eindtest nog aanpassen?") en laat les 8 alleen de *verwerking* + de eindpresentatie zijn.

- **[could]** Geen aparte zelfcheck tegen de rubric vóór de eindbeoordeling.
  - *Waar:* zelfscore gebeurt nu pas in les 8 (`rubric.md` beoordelingstip 3; `docentenhandleiding.md` §7).
  - *Suggestie:* een kort zelfcheck-blokje na les 6 in de dummy ("Draaien beide bewegingen soepel? Welk bewijs heb je?") maakt de formatieve lus eerder rond en sluit mooi aan op het peer-feedbackmoment hierboven.

### 🧱 Structurele conventies (opbouw)

- **[must]** Docentinhoud lekt naar de publieke leerlingpagina.
  - *Waar:* `automata.html` regels **950–955** — het blok `<h3>Beoordelingstips</h3>` + `<ol class="tips">` met pure docentinstructies: "Loop met een korte notitielijst rond", "…vóór jouw beoordeling zelf inschatten", "Zo beoordelen twee docenten hetzelfde werk hetzelfde."
  - *Waarom:* de standaard schrijft voor dat beoordelingstips in de docentenhandleiding horen, niet in de leerlingversie. Het is verwarrend voor 13-jarigen (waarom lezen zij hoe docenten kalibreren?) en het lekt je beoordelingsstrategie. De tips staan al correct in `docentenhandleiding.md` §7 en in `rubric.md`.
  - *Suggestie:* verwijder het blok "Beoordelingstips" uit `automata.html` en regenereer de PDF. Het blok "Proces- vs. productcriteria" (de 60/40-verdeling, regels 928–948) mag blijven — dat helpt de leerling begrijpen waarop gelet wordt. *Dit pak ik sowieso mee bij de layout-omzetting.*

### 🧩 Differentiatie & taalgebruik

Sterk — geen verbeterpunt nodig. Er is een concrete **steun-route** (voorgezaagde blanks, boormal, excenter, eerst één beweging) én **verdieping** (derde beweging, tandwiel/kroonwiel, 3D-print, elektromotor), en de taal is toegankelijk voor havo 2 met vaktermen die worden ingeleid (input/output, excenter, speling).

---

## Kerndoelen-dekking

Toetst opdracht + rubric de kerndoelen die het project claimt daadwerkelijk?

| Kerndoel (SLO, onderbouw) | Geraakt in opdracht? | Getoetst in rubric? | Opmerking |
|---|---|---|---|
| **KD30A** — technische systemen, overbrengingsprincipes | ✅ | ✅ crit 1, 2, 3 | Kern van het project; sterk en toetsbaar. |
| **KD30B** — krachten & beweging, wrijving | ✅ | ✅ crit 4 | Wrijving = centraal leermoment; goed geborgd. |
| **KD29B** — natuurwetenschappelijke denkwijzen (oorzaak-gevolg, systeem, vorm-functie) | ✅ | ✅ crit 1, 4 | Via deelvragen 2 en 5 expliciet ingebouwd. |
| **KD29C** — technologische werkwijzen (iteratief, veilig, vaktaal) | ✅ | ✅ crit 3, 4, 5, 6 | Rode draad; sterk. |
| **KD29A** — verkennen/onderzoeken | gedeeltelijk | gedeeltelijk | Oriënterend (drie voorbeelden), geen volledige onderzoeksopzet — eerlijk als "Deels". |
| **KD29D** — aard van technologie | gedeeltelijk | gedeeltelijk | Reflectie op maakbaarheid/ethiek ontbreekt (bewust "Deels"). |
| **KD40A / KD41A / KD41B** — creatief/kunstzinnig vermogen | gedeeltelijk | gedeeltelijk crit 2 | Toegepaste vormgeving; kunstzinnige reflectie is licht. |
| **KD30C** — elektrische schakelingen/energie | ❌ | ❌ | Slinger-aangedreven; alleen via de verdiepingsroute (elektromotor). |
| **KD21** — ontwerpen/maken met digitale technologie | ❌ | ❌ | Optioneel (laser/3D-print); verplicht maken om het te raken. |

De koppeling is **eerlijk en niet over-claimed**: de mechanica- en ontwerpkern is sterk gedekt en toetsbaar, en wat niet gedekt is (KD30C, KD21) staat correct op "Niet" met een concrete route ernaartoe.

---

## Top-3 als je maar drie dingen doet

1. **[must]** Haal het blok "Beoordelingstips" uit de leerlingpagina (`automata.html` 950–955) en regenereer de PDF — docentinhoud hoort niet op de publieke pagina. *(Neem ik mee in de layout-omzetting.)*
2. **[should]** Zet een expliciet peer-feedbackmoment in **les 6** van de leerlingplanning (nu pas les 8), zodat feedback nog verwerkt kan worden — dit sluit de formatieve lus die criterium 7 en 4 anders bestraffen.
3. **[could]** Link de bestaande 3D-mechanismenanimaties vanuit les 1 / "Achtergrond → Mechanismen", zodat leerlingen ze zelfstandig kunnen bekijken.
