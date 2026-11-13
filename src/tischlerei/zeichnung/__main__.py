import argparse
from datetime import date

from tischlerei.zeichnung.ausgabe import dxf_schreiben, svg_schreiben
from tischlerei.zeichnung.geometrie import faltenmarke, schriftfeld_position, zentriermarken, zeichnungsrahmen
from tischlerei.zeichnung.schriftfeld import FORMATE, SCHRIFTFELD_BREITE, SCHRIFTFELD_HOEHE, SchriftfeldDaten, schriftfeld_zellen


def baue(format_name: str, daten: SchriftfeldDaten) -> tuple[float, float, list, list]:
    breite, hoehe, _, _ = FORMATE[format_name]
    x0, y0, x1, y1 = zeichnungsrahmen(format_name)
    linien = [
        ("Zeichnungsrahmen", x0, y0, x1, y0),
        ("Zeichnungsrahmen", x1, y0, x1, y1),
        ("Zeichnungsrahmen", x1, y1, x0, y1),
        ("Zeichnungsrahmen", x0, y1, x0, y0),
    ]
    for mx1, my1, mx2, my2 in zentriermarken(format_name):
        linien.append(("Zeichnungsrahmen", mx1, my1, mx2, my2))
    for fx1, fy1, fx2, fy2 in faltenmarke(format_name):
        linien.append(("Zeichnungsrahmen", fx1, fy1, fx2, fy2))

    sx, sy = schriftfeld_position(format_name)
    linien.append(("Schriftfeld", sx, sy, sx + SCHRIFTFELD_BREITE, sy))
    linien.append(("Schriftfeld", sx + SCHRIFTFELD_BREITE, sy, sx + SCHRIFTFELD_BREITE, sy + SCHRIFTFELD_HOEHE))
    linien.append(("Schriftfeld", sx + SCHRIFTFELD_BREITE, sy + SCHRIFTFELD_HOEHE, sx, sy + SCHRIFTFELD_HOEHE))
    linien.append(("Schriftfeld", sx, sy + SCHRIFTFELD_HOEHE, sx, sy))

    texte = []
    for z in schriftfeld_zellen(daten):
        zx, zy = sx + z["x"], sy + z["y"]
        linien.append(("Schriftfeld", zx, zy, zx + z["w"], zy))
        linien.append(("Schriftfeld", zx + z["w"], zy, zx + z["w"], zy + z["h"]))
        linien.append(("Schriftfeld", zx + z["w"], zy + z["h"], zx, zy + z["h"]))
        linien.append(("Schriftfeld", zx, zy + z["h"], zx, zy))
        texte.append(("Texte", zx + 1.0, zy + z["h"] - 3.0, 2.2, z["label"]))
        if z["value"]:
            texte.append(("Texte", zx + 1.0, zy + z["h"] - 3.0 - z["wert_hoehe"] - 1.0, z["wert_hoehe"], z["value"]))
    return breite, hoehe, linien, texte


def main() -> None:
    p = argparse.ArgumentParser(description="Erzeugt Zeichnungsrahmen mit Schriftfeld als DXF und SVG.")
    p.add_argument("--format", choices=sorted(FORMATE), default="A3")
    p.add_argument("--ausgabe", default="zeichnungsrahmen")
    p.add_argument("--titel", default="")
    p.add_argument("--vorgangsnummer", default="")
    p.add_argument("--kunde", default="")
    p.add_argument("--projekt", default="")
    p.add_argument("--material", default="")
    p.add_argument("--massstab", default="1:1")
    p.add_argument("--datum", default=date.today().isoformat())
    p.add_argument("--gezeichnet", default="R. Gerdes")
    p.add_argument("--geprueft", default="")
    p.add_argument("--firma", default="Tischlerei Backmann")
    args = p.parse_args()

    daten = SchriftfeldDaten(
        titel=args.titel, vorgangsnummer=args.vorgangsnummer, kunde=args.kunde, projekt=args.projekt,
        material=args.material, massstab=args.massstab, datum=args.datum, gezeichnet=args.gezeichnet,
        geprueft=args.geprueft, format=args.format, firma=args.firma,
    )
    breite, hoehe, linien, texte = baue(args.format, daten)
    dxf_schreiben(f"{args.ausgabe}.dxf", linien, texte)
    svg_schreiben(f"{args.ausgabe}.svg", breite, hoehe, linien, texte)
    print(f"{args.ausgabe}.dxf und {args.ausgabe}.svg erzeugt ({args.format}, {breite}x{hoehe} mm)")


if __name__ == "__main__":
    main()
