from tischlerei.zeichnung.schriftfeld import FORMATE, SCHRIFTFELD_BREITE, SCHRIFTFELD_HOEHE


def zeichnungsrahmen(format_name: str) -> tuple[float, float, float, float]:
    """Rechteck des Zeichnungsrahmens (x0, y0, x1, y1) in mm, Rand nach DIN 6771-1."""
    breite, hoehe, rand_links, rand_uebrige = FORMATE[format_name]
    return rand_links, rand_uebrige, breite - rand_uebrige, hoehe - rand_uebrige


def zentriermarken(format_name: str) -> list[tuple[float, float, float, float]]:
    """Zentriermarken an den Seitenmitten, die den Rahmen kreuzen."""
    breite, hoehe, rand_links, rand_uebrige = FORMATE[format_name]
    x0, y0 = rand_links, rand_uebrige
    x1, y1 = breite - rand_uebrige, hoehe - rand_uebrige
    l = 5.0
    return [
        (x0 - l, (y0 + y1) / 2.0, x0 + l, (y0 + y1) / 2.0),
        (x1 - l, (y0 + y1) / 2.0, x1 + l, (y0 + y1) / 2.0),
        ((x0 + x1) / 2.0, y0 - l, (x0 + x1) / 2.0, y0 + l),
        ((x0 + x1) / 2.0, y1 - l, (x0 + x1) / 2.0, y1 + l),
    ]


def faltenmarke(format_name: str) -> list[tuple[float, float, float, float]]:
    """Faltmarke oben, 185 mm von der rechten Kante (DIN 6771-1), nur bei Breitformat."""
    breite, hoehe, _, rand_uebrige = FORMATE[format_name]
    if breite <= 297.0:
        return []
    x = breite - 185.0
    y = hoehe - rand_uebrige
    return [(x - 5.0, y, x + 5.0, y), (x + 5.0, y, x, y - 5.0), (x, y - 5.0, x - 5.0, y)]


def schriftfeld_position(format_name: str) -> tuple[float, float]:
    """Ursprung (links unten) des Schriftfelds: 180x56 mm in der unteren rechten Ecke."""
    x0, y0, x1, _ = zeichnungsrahmen(format_name)
    return x1 - SCHRIFTFELD_BREITE, y0
