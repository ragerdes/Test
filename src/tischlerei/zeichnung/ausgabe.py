def dxf_schreiben(pfad: str, linien: list[tuple[str, float, float, float, float]], texte: list[tuple[str, float, float, float, str]]) -> None:
    """Minimaler DXF-Writer (AutoCAD R12), Einheiten mm, ohne externe Abhängigkeiten."""
    layer = {"Zeichnungsrahmen": 7, "Schriftfeld": 5, "Texte": 2}
    namen = list(dict.fromkeys([l[0] for l in linien] + [t[0] for t in texte]))

    with open(pfad, "w", encoding="utf-8") as f:
        f.write("0\nSECTION\n2\nHEADER\n9\n$ACADVER\n1\nAC1009\n9\n$INSUNITS\n70\n4\n0\nENDSEC\n")
        f.write("0\nSECTION\n2\nTABLES\n0\nTABLE\n2\nLAYER\n70\n%d\n" % len(namen))
        for name in namen:
            f.write("0\nLAYER\n2\n%s\n70\n0\n62\n%d\n6\nCONTINUOUS\n" % (name, layer.get(name, 7)))
        f.write("0\nENDTAB\n0\nENDSEC\n")
        f.write("0\nSECTION\n2\nENTITIES\n")
        for lay, x1, y1, x2, y2 in linien:
            f.write("0\nLINE\n8\n%s\n10\n%.4f\n20\n%.4f\n30\n0.0\n11\n%.4f\n21\n%.4f\n31\n0.0\n" % (lay, x1, y1, x2, y2))
        for lay, x, y, hoehe, text in texte:
            f.write("0\nTEXT\n8\n%s\n10\n%.4f\n20\n%.4f\n30\n0.0\n40\n%.4f\n1\n%s\n" % (lay, x, y, hoehe, text))
        f.write("0\nENDSEC\n0\nEOF\n")


def svg_schreiben(pfad: str, breite: float, hoehe: float, linien: list[tuple[str, float, float, float, float]], texte: list[tuple[str, float, float, float, str]]) -> None:
    """SVG-Vorschau, gleiche mm-Geometrie wie der DXF (y-Achse gespiegelt)."""
    farbe = {"Zeichnungsrahmen": "#000000", "Schriftfeld": "#1a5fb4", "Texte": "#7a3000"}
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    with open(pfad, "w", encoding="utf-8") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" width="{breite}mm" height="{hoehe}mm" viewBox="0 0 {breite} {hoehe}">\n')
        f.write(f'<rect x="0" y="0" width="{breite}" height="{hoehe}" fill="#ffffff"/>\n')
        for lay, x1, y1, x2, y2 in linien:
            f.write(f'<line x1="{x1:.3f}" y1="{hoehe - y1:.3f}" x2="{x2:.3f}" y2="{hoehe - y2:.3f}" stroke="{farbe.get(lay, "#000000")}" stroke-width="0.35"/>\n')
        for lay, x, y, h, text in texte:
            f.write(f'<text x="{x:.3f}" y="{hoehe - y:.3f}" font-family="Arial, sans-serif" font-size="{h:.2f}" fill="{farbe.get(lay, "#000000")}">{esc(text)}</text>\n')
        f.write("</svg>\n")
