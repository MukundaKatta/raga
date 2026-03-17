"""Rhythm generator for tala patterns with variations.

Generates rhythmic patterns (bols) for tabla/percussion accompaniment,
including theka, variations (peshkaar, kayda, tukda), and tihai patterns.
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from raga.models import TalaDefinition


class RhythmGenerator:
    """Generate tala-based rhythmic patterns with variations."""

    # Common bol syllables grouped by resonance type
    BAYAN_BOLS = ["Ge", "Ga", "Ghi", "Ka", "Ke", "Ghe"]  # bass drum
    DAYAN_BOLS = ["Na", "Ta", "Ti", "Tin", "Tu", "Ra", "Te"]  # treble drum
    COMBINED_BOLS = ["Dha", "Dhin", "Dhi", "DhaGe", "TiRaKiTa", "DhiNa"]  # both drums

    def __init__(self, tala: TalaDefinition, seed: Optional[int] = None) -> None:
        self.tala = tala
        self.rng = np.random.default_rng(seed)
        self._base_bols = tala.bols if tala.bols else self._derive_bols()

    def _derive_bols(self) -> list[str]:
        """Derive basic bols from theka string if bols not provided."""
        if self.tala.theka:
            parts = self.tala.theka.replace("|", "").replace("-", "").split()
            return [p.strip() for p in parts if p.strip()]
        return ["Dha"] * self.tala.beats

    def get_theka(self) -> list[str]:
        """Return the basic theka pattern for one cycle."""
        return list(self._base_bols)

    def generate_variation(self, intensity: float = 0.3) -> list[str]:
        """Generate a variation of the theka.

        Args:
            intensity: 0.0 = pure theka, 1.0 = maximum variation.

        Returns:
            List of bol syllables for one tala cycle.
        """
        bols = list(self._base_bols)

        for i in range(len(bols)):
            if self.rng.random() < intensity:
                # Check if this is a sam or khali position
                beat_num = i + 1
                if beat_num == self.tala.sam:
                    # Sam must be a resonant bol
                    bols[i] = self.rng.choice(self.COMBINED_BOLS)
                elif beat_num in self.tala.khali:
                    # Khali uses non-resonant bols
                    bols[i] = self.rng.choice(self.DAYAN_BOLS)
                else:
                    # Other positions: mix of all bols
                    all_bols = self.BAYAN_BOLS + self.DAYAN_BOLS + self.COMBINED_BOLS
                    bols[i] = self.rng.choice(all_bols)

        return bols

    def generate_tihai(self, phrase_length: int = 3) -> list[str]:
        """Generate a tihai (three-fold cadential pattern ending on sam).

        A tihai repeats a phrase 3 times, ending precisely on sam.
        """
        # Build a short phrase
        phrase_bols: list[str] = []
        all_bols = self.COMBINED_BOLS + self.DAYAN_BOLS
        for _ in range(phrase_length):
            phrase_bols.append(self.rng.choice(all_bols))

        # Calculate gap needed: total = 3*phrase + 2*gap must fit in remaining beats
        # Simplified: just repeat three times with a gap bol
        gap_bol = self.rng.choice(self.DAYAN_BOLS)
        tihai = phrase_bols + [gap_bol] + phrase_bols + [gap_bol] + phrase_bols

        return tihai

    def generate_peshkaar(self, cycles: int = 2) -> list[list[str]]:
        """Generate a peshkaar (introductory elaboration) pattern.

        Returns a list of tala cycles, each a list of bols.
        """
        result: list[list[str]] = []
        for i in range(cycles):
            intensity = 0.1 + (i / max(1, cycles - 1)) * 0.3
            result.append(self.generate_variation(intensity))
        return result

    def generate_kayda(self, theme_length: int = 4) -> list[list[str]]:
        """Generate a kayda (theme and variations).

        Returns theme followed by variations.
        """
        # Create theme
        theme: list[str] = []
        for _ in range(theme_length):
            theme.append(self.rng.choice(self.COMBINED_BOLS))

        # Pad theme to fill one cycle
        cycle_bols = theme * (self.tala.beats // max(1, len(theme)))
        cycle_bols = cycle_bols[: self.tala.beats]
        while len(cycle_bols) < self.tala.beats:
            cycle_bols.append("Dha")

        # Generate variations
        variations: list[list[str]] = [list(cycle_bols)]
        for v in range(3):
            var = list(cycle_bols)
            # Substitute portions with related bols
            num_changes = (v + 1) * 2
            for _ in range(num_changes):
                pos = self.rng.integers(0, len(var))
                original = var[pos]
                if original in self.COMBINED_BOLS:
                    var[pos] = self.rng.choice(self.COMBINED_BOLS)
                elif original in self.DAYAN_BOLS:
                    var[pos] = self.rng.choice(self.DAYAN_BOLS)
                else:
                    var[pos] = self.rng.choice(self.BAYAN_BOLS)
            variations.append(var)

        return variations

    def generate_pattern(
        self,
        num_cycles: int = 4,
        intensity_curve: Optional[list[float]] = None,
    ) -> list[list[str]]:
        """Generate a multi-cycle rhythmic pattern with evolving intensity.

        Args:
            num_cycles: Number of tala cycles.
            intensity_curve: Intensity per cycle (0-1). Defaults to gradual increase.

        Returns:
            List of cycles, each a list of bols.
        """
        if intensity_curve is None:
            intensity_curve = [i / max(1, num_cycles - 1) * 0.5 for i in range(num_cycles)]

        cycles: list[list[str]] = []
        for i in range(num_cycles):
            intensity = intensity_curve[min(i, len(intensity_curve) - 1)]
            cycles.append(self.generate_variation(intensity))

        return cycles
