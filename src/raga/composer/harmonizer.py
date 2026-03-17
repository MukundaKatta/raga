"""Composition builder: combine melody and rhythm into structured compositions.

Generates complete compositions with proper section structure:
- Alap: slow, free-rhythm exploration of the raga
- Jor: rhythmic pulse introduced, still no tala cycle
- Jhala: fast rhythmic climax with repeated patterns
- Gat: composed section set to a tala cycle (sthayi + antara)
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from raga.models import (
    Composition,
    CompositionSection,
    RagaDefinition,
    Section,
    SwaraSequence,
    TalaDefinition,
)
from raga.composer.melody import MelodyGenerator
from raga.composer.rhythm import RhythmGenerator


class CompositionBuilder:
    """Build a complete Indian classical music composition."""

    def __init__(
        self,
        raga: RagaDefinition,
        tala: TalaDefinition,
        seed: Optional[int] = None,
    ) -> None:
        self.raga = raga
        self.tala = tala
        self.rng = np.random.default_rng(seed)
        self.melody_gen = MelodyGenerator(raga, seed=seed)
        self.rhythm_gen = RhythmGenerator(tala, seed=seed)

    def build_alap(self, num_phrases: int = 6) -> CompositionSection:
        """Build an alap section: slow, meditative raga exploration.

        The alap gradually unfolds the raga, starting from the lower register
        and slowly ascending, dwelling on each important note.
        """
        phrases: list[SwaraSequence] = []
        # Start with short phrases, gradually lengthen
        for i in range(num_phrases):
            length = 6 + i * 2  # Gradually longer phrases
            phrase = self.melody_gen.generate_alap_phrase(length=min(length, 16))
            phrases.append(phrase)

        return CompositionSection(
            section_type=Section.ALAP,
            phrases=phrases,
            tempo=0.5,
            description=f"Alap in {self.raga.name}: slow raga exploration, "
            f"emphasizing {self.raga.vadi} (vadi) and {self.raga.samvadi} (samvadi)",
        )

    def build_jor(self, num_phrases: int = 4) -> CompositionSection:
        """Build a jor section: rhythmic pulse without tala.

        Jor introduces a steady pulse. Phrases become more rhythmic
        and slightly faster than alap.
        """
        phrases: list[SwaraSequence] = []
        for _ in range(num_phrases):
            phrase = self.melody_gen.generate_phrase(length=8)
            phrases.append(phrase)

        return CompositionSection(
            section_type=Section.JOR,
            phrases=phrases,
            tempo=0.75,
            description=f"Jor in {self.raga.name}: steady rhythmic pulse introduced",
        )

    def build_jhala(self, num_phrases: int = 4) -> CompositionSection:
        """Build a jhala section: fast rhythmic climax.

        Jhala features rapid, energetic passages with repeated patterns
        and string crossings (on instruments like sitar/sarod).
        """
        phrases: list[SwaraSequence] = []
        for _ in range(num_phrases):
            # Shorter, more repetitive phrases for jhala energy
            base_phrase = self.melody_gen.generate_phrase(length=4)
            # Double the phrase for rhythmic repetition effect
            combined_swaras = base_phrase.swaras + base_phrase.swaras
            phrases.append(SwaraSequence(swaras=combined_swaras))

        return CompositionSection(
            section_type=Section.JHALA,
            phrases=phrases,
            tempo=1.5,
            description=f"Jhala in {self.raga.name}: energetic rhythmic climax",
        )

    def build_gat(self, num_cycles: int = 4) -> CompositionSection:
        """Build a gat section: composed piece set to tala.

        The gat has a fixed composition (sthayi in lower octave,
        antara in upper octave) with improvised variations.
        """
        phrases: list[SwaraSequence] = []

        # Sthayi: lower register, centered around Sa-Pa
        for _ in range(num_cycles // 2 + 1):
            phrase = self.melody_gen.generate_phrase(
                length=self.tala.beats,
                start_note="Sa",
            )
            phrases.append(phrase)

        # Antara: upper register, exploring taar saptak
        for _ in range(num_cycles // 2 + 1):
            phrase = self.melody_gen.generate_phrase(
                length=self.tala.beats,
                start_note=self.raga.vadi,
            )
            phrases.append(phrase)

        return CompositionSection(
            section_type=Section.GAT,
            phrases=phrases,
            tala_name=self.tala.name,
            tempo=1.0,
            description=f"Gat in {self.raga.name} set to {self.tala.name} "
            f"({self.tala.beats} beats): sthayi and antara",
        )

    def compose(
        self,
        sections: Optional[list[str]] = None,
        title: Optional[str] = None,
    ) -> Composition:
        """Build a complete composition with specified sections.

        Args:
            sections: List of section names to include.
                Defaults to ["alap", "jor", "jhala", "gat"].
            title: Composition title.

        Returns:
            A complete Composition model.
        """
        if sections is None:
            sections = ["alap", "jor", "jhala", "gat"]

        builders = {
            "alap": self.build_alap,
            "jor": self.build_jor,
            "jhala": self.build_jhala,
            "gat": self.build_gat,
        }

        comp_sections: list[CompositionSection] = []
        for section_name in sections:
            key = section_name.lower().strip()
            if key in builders:
                comp_sections.append(builders[key]())
            else:
                raise ValueError(
                    f"Unknown section '{section_name}'. "
                    f"Available: {', '.join(builders.keys())}"
                )

        comp_title = title or f"Composition in {self.raga.name.replace('_', ' ').title()}"

        return Composition(
            title=comp_title,
            raga=self.raga.name,
            tala=self.tala.name,
            sections=comp_sections,
            description=(
                f"A {self.raga.mood or 'classical'} composition in "
                f"Raga {self.raga.name.replace('_', ' ').title()} "
                f"set to {self.tala.name.replace('_', ' ').title()} "
                f"({self.tala.beats} beats). "
                f"Time: {self.raga.time or 'any time'}."
            ),
        )
