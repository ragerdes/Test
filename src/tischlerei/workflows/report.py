from collections import Counter
from typing import Optional

import mistralai.workflows as workflows
from pydantic import BaseModel, Field


class Auftrag(BaseModel):
    nummer: str
    kunde: str
    projekt: str = ""
    pipeline_stufe: str = "Unbekannt"
    faellig: Optional[str] = None
    notiz: str = ""


class ReportInput(BaseModel):
    auftraege: list[Auftrag] = Field(default_factory=list)
    woche: str = ""


@workflows.activity()
async def erstelle_liste(auftraege: list[Auftrag]) -> str:
    """Baut die sortierte Markdown-Liste aller Auftraege."""
    zeilen = []
    for a in sorted(auftraege, key=lambda x: x.nummer):
        zeile = f"- **#{a.nummer} {a.kunde}** {('– ' + a.projekt) if a.projekt else ''} · Stufe: {a.pipeline_stufe}"
        if a.faellig:
            zeile += f" · faellig: {a.faellig}"
        if a.notiz:
            zeile += f" · {a.notiz}"
        zeilen.append(zeile)
    return "\n".join(zeilen)


@workflows.activity()
async def zaehle_stufen(auftraege: list[Auftrag]) -> dict:
    """Zaehlt die Auftraege je Pipeline-Stufe."""
    return dict(Counter(a.pipeline_stufe for a in auftraege))


@workflows.workflow.define(
    name="tischlerei-wochenbericht",
    workflow_display_name="Tischlerei Wochenbericht",
    workflow_description="Erzeugt einen Markdown-Wochenbericht ueber offene Auftraege nach Pipeline-Stufe.",
)
class TischlereiReportWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, input: ReportInput) -> dict:
        stufen = await zaehle_stufen(input.auftraege)
        liste = await erstelle_liste(input.auftraege)

        titel = f"Wochenbericht Tischlerei{' – ' + input.woche if input.woche else ''}"
        uebersicht = "\n".join(f"- {stufe}: {anzahl}" for stufe, anzahl in sorted(stufen.items()))
        faellige = [a for a in input.auftraege if a.faellig]
        faellige_zeilen = "\n".join(
            f"- #{a.nummer} {a.kunde} ({a.faellig})" for a in sorted(faellige, key=lambda x: x.nummer)
        ) or "- keine"

        bericht = (
            f"# {titel}\n\n"
            f"## Übersicht ({len(input.auftraege)} offene Aufträge)\n{uebersicht}\n\n"
            f"## Fällige / Follow-Up\n{faellige_zeilen}\n\n"
            f"## Alle Aufträge\n{liste}"
        )
        return {"result": bericht, "anzahl": len(input.auftraege), "stufen": stufen}
