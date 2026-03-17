"""CLI interface for RAGA - AI Indian Music Composer."""

from __future__ import annotations

import json
from typing import Optional

import click
from rich.console import Console

from raga.models import Composition
from raga.music.ragas import RagaDatabase
from raga.music.talas import TalaDatabase
from raga.composer.harmonizer import CompositionBuilder
from raga.report import (
    display_composition,
    display_raga_info,
    display_raga_list,
    display_tala_info,
)

console = Console()
raga_db = RagaDatabase()
tala_db = TalaDatabase()


@click.group()
@click.version_option(version="0.1.0", prog_name="raga")
def cli() -> None:
    """RAGA - AI Indian Music Composer.

    Generate raga-compliant Indian classical music compositions
    with proper phrasing, tala patterns, and structured sections.
    """


@cli.command()
@click.option("--raga", "-r", required=True, help="Raga name (e.g., yaman, bhairav)")
@click.option("--tala", "-t", default="teentaal", help="Tala name (default: teentaal)")
@click.option(
    "--sections", "-s",
    default="alap,jor,jhala,gat",
    help="Comma-separated sections: alap,jor,jhala,gat",
)
@click.option("--title", help="Composition title")
@click.option("--seed", type=int, help="Random seed for reproducibility")
@click.option("--output", "-o", type=click.Path(), help="Save composition as JSON")
def compose(
    raga: str,
    tala: str,
    sections: str,
    title: Optional[str],
    seed: Optional[int],
    output: Optional[str],
) -> None:
    """Compose a piece in a specified raga and tala."""
    try:
        raga_def = raga_db.get(raga)
    except KeyError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    try:
        tala_def = tala_db.get(tala)
    except KeyError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    section_list = [s.strip() for s in sections.split(",")]

    builder = CompositionBuilder(raga_def, tala_def, seed=seed)

    try:
        composition = builder.compose(sections=section_list, title=title)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise SystemExit(1)

    display_composition(composition, console)

    if output:
        with open(output, "w") as f:
            json.dump(composition.model_dump(mode="json"), f, indent=2)
        console.print(f"\n[green]Saved to {output}[/green]")


@cli.command()
@click.argument("composition_file", type=click.Path(exists=True))
def play(composition_file: str) -> None:
    """Play back a composition from a JSON file (renders notation)."""
    with open(composition_file) as f:
        data = json.load(f)

    try:
        composition = Composition.model_validate(data)
    except Exception as e:
        console.print(f"[red]Error loading composition:[/red] {e}")
        raise SystemExit(1)

    console.print(f"[bold]Playing: {composition.title}[/bold]\n")
    display_composition(composition, console)


@cli.command()
@click.option("--raga", "-r", help="Raga name to analyze")
@click.option("--tala", "-t", help="Tala name to analyze")
@click.option("--thaat", help="List all ragas in a thaat")
@click.option("--list-ragas", is_flag=True, help="List all available ragas")
@click.option("--list-talas", is_flag=True, help="List all available talas")
@click.option("--mood", help="Search ragas by mood keyword")
@click.option("--time", "time_", help="Search ragas by performance time")
def analyze(
    raga: Optional[str],
    tala: Optional[str],
    thaat: Optional[str],
    list_ragas: bool,
    list_talas: bool,
    mood: Optional[str],
    time_: Optional[str],
) -> None:
    """Analyze a raga or tala's properties."""
    if list_ragas:
        all_ragas = raga_db.list_all()
        display_raga_list(all_ragas, console)
        console.print(f"\n[dim]Total: {raga_db.count} ragas[/dim]")
        return

    if list_talas:
        all_talas = tala_db.list_all()
        for t in all_talas:
            display_tala_info(t, console)
        console.print(f"\n[dim]Total: {tala_db.count} talas[/dim]")
        return

    if thaat:
        ragas = raga_db.by_thaat(thaat)
        if not ragas:
            console.print(f"[yellow]No ragas found in thaat '{thaat}'[/yellow]")
            return
        console.print(f"[bold]Ragas in {thaat.title()} thaat:[/bold]\n")
        display_raga_list(ragas, console)
        return

    if mood:
        ragas = raga_db.search(mood=mood)
        if not ragas:
            console.print(f"[yellow]No ragas found for mood '{mood}'[/yellow]")
            return
        console.print(f"[bold]Ragas for mood '{mood}':[/bold]\n")
        display_raga_list(ragas, console)
        return

    if time_:
        ragas = raga_db.by_time(time_)
        if not ragas:
            console.print(f"[yellow]No ragas found for time '{time_}'[/yellow]")
            return
        console.print(f"[bold]Ragas for time '{time_}':[/bold]\n")
        display_raga_list(ragas, console)
        return

    if raga:
        try:
            raga_def = raga_db.get(raga)
            display_raga_info(raga_def, console)
        except KeyError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise SystemExit(1)

    if tala:
        try:
            tala_def = tala_db.get(tala)
            display_tala_info(tala_def, console)
        except KeyError as e:
            console.print(f"[red]Error:[/red] {e}")
            raise SystemExit(1)

    if not any([raga, tala, thaat, list_ragas, list_talas, mood, time_]):
        console.print("[yellow]Specify --raga, --tala, --list-ragas, or --list-talas[/yellow]")


if __name__ == "__main__":
    cli()
