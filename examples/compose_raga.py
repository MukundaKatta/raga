#!/usr/bin/env python3
"""Example: compose and display a piece in Raga Yaman set to Teentaal."""

from rich.console import Console

from raga.music.ragas import RagaDatabase
from raga.music.talas import TalaDatabase
from raga.composer.melody import MelodyGenerator
from raga.composer.rhythm import RhythmGenerator
from raga.composer.harmonizer import CompositionBuilder
from raga.report import display_composition, display_raga_info, display_tala_info

console = Console()


def main() -> None:
    # Initialize databases
    raga_db = RagaDatabase()
    tala_db = TalaDatabase()

    console.print(f"[bold]RAGA - AI Indian Music Composer[/bold]")
    console.print(f"Available ragas: {raga_db.count} | Available talas: {tala_db.count}\n")

    # Select raga and tala
    yaman = raga_db.get("yaman")
    teentaal = tala_db.get("teentaal")

    # Display raga and tala info
    display_raga_info(yaman, console)
    display_tala_info(teentaal, console)

    # Generate a quick melody phrase
    console.print("\n[bold cyan]--- Quick Melody Generation ---[/bold cyan]")
    melody_gen = MelodyGenerator(yaman, seed=42)
    phrase = melody_gen.generate_phrase(length=8)
    console.print(f"  Single phrase: {phrase.notation}")

    alap_phrase = melody_gen.generate_alap_phrase(length=12)
    console.print(f"  Alap phrase:   {alap_phrase.notation}")

    # Generate rhythm pattern
    console.print("\n[bold green]--- Rhythm Pattern ---[/bold green]")
    rhythm_gen = RhythmGenerator(teentaal, seed=42)
    theka = rhythm_gen.get_theka()
    console.print(f"  Theka: {' '.join(theka)}")

    variation = rhythm_gen.generate_variation(intensity=0.3)
    console.print(f"  Variation: {' '.join(variation)}")

    tihai = rhythm_gen.generate_tihai(phrase_length=3)
    console.print(f"  Tihai: {' '.join(tihai)}")

    # Build full composition
    console.print("\n[bold magenta]--- Full Composition ---[/bold magenta]\n")
    builder = CompositionBuilder(yaman, teentaal, seed=42)
    composition = builder.compose(title="Evening Melody in Yaman")
    display_composition(composition, console)

    # Demonstrate with a different raga
    console.print("\n[bold]--- Composition in Raga Bhairav ---[/bold]\n")
    bhairav = raga_db.get("bhairav")
    display_raga_info(bhairav, console)

    builder2 = CompositionBuilder(bhairav, teentaal, seed=99)
    comp2 = builder2.compose(
        sections=["alap", "gat"],
        title="Dawn Meditation in Bhairav",
    )
    display_composition(comp2, console)


if __name__ == "__main__":
    main()
