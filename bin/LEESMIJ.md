# Edities opnieuw maken

De twee pdf-edities worden gegenereerd uit `docs/index.html`, de bouwplaat en
de docentenhandleiding. Aanpassing in de html? Dan hier opnieuw draaien.

## Eenmalig installeren

```bash
npm install puppeteer-core          # gebruikt de Chrome die al op je Mac staat
python3 -m venv venv && ./venv/bin/pip install pymupdf
```

## Genereren

```bash
node print.js ../docs/index.html && mv ../docs/index.pdf ../docs/automata.pdf
mkdir -p ed-work/src && cp ../docs/index.html ed-work/src/
ln -sf ../../../docs/afbeeldingen ed-work/src/afbeeldingen
node render.js ed-work/src ed-work        # meet waar de invulvelden staan
./venv/bin/python maak-edities.py         # voorblad, inhoudsopgave, bladwijzers
./venv/bin/python velden-editie.py        # invulvelden in de leerlingeditie
```

## Hoe het werkt

`render.js` rendert de pagina twee keer met exact dezelfde opmaak: één keer met
een onzichtbare kleurcode per invulveld om de positie te meten, en één keer
schoon. `velden-editie.py` legt de formuliervelden daarna precies op die
plekken, verschoven met de twee bladen voorwerk.

`maak-edities.py` bepaalt de paginanummers voor de inhoudsopgave door de
koppen in de pdf terug te zoeken — in de handleiding op tekstgrootte, want
zoeken op woorden vindt daar ook gewone tekst.

## Uitvoer

| Bestand | Waar | Voor wie |
|---|---|---|
| `docs/automata-leerlingeditie.pdf` | op de site | leerlingen, invulbaar |
| `automata-docenteneditie.pdf` | buiten `docs/` | alleen de docent |
