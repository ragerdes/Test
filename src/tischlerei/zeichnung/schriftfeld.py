from dataclasses import dataclass

FORMATE = {
    "A4": (210.0, 297.0, 20.0, 5.0),
    "A3": (420.0, 297.0, 20.0, 5.0),
    "A2": (594.0, 420.0, 25.0, 10.0),
}

SCHRIFTFELD_BREITE = 180.0
SCHRIFTFELD_HOEHE = 56.0


@dataclass
class SchriftfeldDaten:
    titel: str = ""
    vorgangsnummer: str = ""
    kunde: str = ""
    projekt: str = ""
    material: str = ""
    massstab: str = "1:1"
    datum: str = ""
    gezeichnet: str = ""
    geprueft: str = ""
    blatt: str = "1/1"
    format: str = ""
    firma: str = "Tischlerei Backmann"


def schriftfeld_zellen(daten: SchriftfeldDaten, breite: float = SCHRIFTFELD_BREITE, hoehe: float = SCHRIFTFELD_HOEHE) -> list[dict]:
    """Zellen des Schriftfelds (ISO-7200-Raster 180x56), Ursprung links unten."""
    zellen = []

    def zelle(x, y, w, h, label, value, wert_hoehe=3.5):
        zellen.append({"x": x, "y": y, "w": w, "h": h, "label": label, "value": value, "wert_hoehe": wert_hoehe})

    titel_h = hoehe - 34.0
    zelle(0.0, 34.0, 120.0, titel_h, "Bezeichnung / Titel", daten.titel, wert_hoehe=5.0)
    zelle(120.0, 34.0, breite - 120.0, titel_h, "Vorgangs- / Zeichnungs-Nr.", daten.vorgangsnummer)

    zelle(0.0, 14.0, 45.0, 20.0, "Kunde", daten.kunde)
    zelle(45.0, 14.0, 45.0, 20.0, "Projekt", daten.projekt)
    zelle(90.0, 14.0, 45.0, 20.0, "Material", daten.material)
    zelle(135.0, 14.0, breite - 135.0, 20.0, "Maßstab", daten.massstab)

    zelle(0.0, 0.0, 90.0, 14.0, "Firma", daten.firma)
    zelle(90.0, 0.0, 35.0, 14.0, "Gezeichnet", daten.gezeichnet)
    zelle(125.0, 0.0, 30.0, 14.0, "Geprüft", daten.geprueft)
    zelle(155.0, 0.0, breite - 155.0, 14.0, "Datum", daten.datum)
    return zellen
