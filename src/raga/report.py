"""Rich composition display with swara notation rendering."""

from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from raga.models import Composition, CompositionSection, RagaDefinition, TalaDefinition
from raga.music.notation import SwarNotation


def display_raga_info(raga: RagaDefinition, console: Console | None = None) -> None:
    """Display detailed raga information with rich formatting."""
    con = console or Console()

    title = f"Raga {raga.name.replace('_', ' ').title()}"

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Property", style="bold cyan", width=16)
    table.add_column("Value")

    table.add_row("Thaat", raga.thaat.title() if raga.thaat else "N/A")
    table.add_row("Aroha", " ".join(raga.aroha))
    table.add_row("Avaroha", " ".join(raga.avaroha))
    table.add_row("Vadi", raga.vadi)
    table.add_row("Samvadi", raga.samvadi)
    table.add_row("Jati", raga.jati)

    if raga.pakad:
        table.add_row("Pakad", " ".join(raga.pakad))
    if raga.varjit_aroha:
        table.add_row("Varjit (aroha)", " ".join(raga.varjit_aroha))
    if raga.varjit_avaroha:
        table.add_row("Varjit (avaroha)", " ".join(raga.varjit_avaroha))

    table.add_row("Mood", raga.mood or "N/A")
    table.add_row("Time", raga.time or "N/A")

    if raga.description:
        table.add_row("Description", raga.description)

    con.print(Panel(table, title=title, border_style="bright_blue"))


def display_tala_info(tala: TalaDefinition, console: Console | None = None) -> None:
    """Display detailed tala information."""
    con = console or Console()

    title = f"Tala: {tala.name.replace('_', ' ').title()}"

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Property", style="bold cyan", width=16)
    table.add_column("Value")

    table.add_row("Beats (matras)", str(tala.beats))
    table.add_row("Vibhags", " + ".join(str(v) for v in tala.vibhags))
    table.add_row("Sam", str(tala.sam))
    table.add_row("Khali", ", ".join(str(k) for k in tala.khali) if tala.khali else "None")
    table.add_row("Theka", tala.theka or "N/A")

    if tala.description:
        table.add_row("Description", tala.description)

    con.print(Panel(table, title=title, border_style="bright_green"))


def display_composition(composition: Composition, console: Console | None = None) -> None:
    """Display a full composition with rich formatting."""
    con = console or Console()

    # Header
    header = Text()
    header.append(f"\n{composition.title}\n", style="bold bright_white")
    header.append(f"Raga: {composition.raga.replace('_', ' ').title()}", style="cyan")
    header.append(" | ", style="dim")
    header.append(f"Tala: {composition.tala.replace('_', ' ').title()}", style="green")
    header.append(" | ", style="dim")
    header.append(f"Tempo: {composition.tempo_bpm} BPM", style="yellow")
    con.print(header)

    if composition.description:
        con.print(f"\n[dim]{composition.description}[/dim]")

    con.print()

    # Each section
    for section in composition.sections:
        _display_section(section, con)

    # Summary
    summary = Table(title="Summary", show_header=False, box=None)
    summary.add_column("", style="bold")
    summary.add_column("")
    summary.add_row("Total sections", str(len(composition.sections)))
    summary.add_row("Total phrases", str(composition.total_phrases))
    con.print(Panel(summary, border_style="dim"))


def _display_section(section: CompositionSection, con: Console) -> None:
    """Display a single composition section."""
    section_name = section.section_type.value.upper()
    tempo_label = {0.5: "Vilambit", 0.75: "Madhya-Vilambit", 1.0: "Madhya", 1.5: "Drut"}.get(
        section.tempo, f"x{section.tempo}"
    )

    con.print(f"[bold magenta]--- {section_name} ---[/bold magenta]  [dim]({tempo_label})[/dim]")

    if section.description:
        con.print(f"  [dim italic]{section.description}[/dim italic]")

    if section.tala_name:
        con.print(f"  [green]Tala: {section.tala_name}[/green]")

    for i, phrase in enumerate(section.phrases, 1):
        notation = SwarNotation.render(phrase)
        con.print(f"  [bright_white]{i:2d}.[/bright_white] {notation}")

    con.print()


def display_raga_list(ragas: list[RagaDefinition], console: Console | None = None) -> None:
    """Display a table listing multiple ragas."""
    con = console or Console()

    table = Table(title="Ragas", show_lines=False)
    table.add_column("#", style="dim", width=4)
    table.add_column("Name", style="bold cyan")
    table.add_column("Thaat", style="green")
    table.add_column("Vadi", width=6)
    table.add_column("Samvadi", width=8)
    table.add_column("Time")
    table.add_column("Mood", max_width=30)

    for i, r in enumerate(ragas, 1):
        table.add_row(
            str(i),
            r.name.replace("_", " ").title(),
            r.thaat.title() if r.thaat else "",
            r.vadi,
            r.samvadi,
            r.time or "",
            r.mood or "",
        )

    con.print(table)
