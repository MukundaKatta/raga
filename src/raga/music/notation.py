"""Indian music notation parser and renderer.

Supports standard Hindustani notation conventions:
- Uppercase = shuddha, lowercase = komal, trailing ' = tivra
- . prefix = mandra saptak (lower octave)
- * suffix = taar saptak (upper octave)
- - = sustain, | = bar line, S = rest (khali)
"""

from __future__ import annotations

import re
from typing import Optional

from raga.models import Swara, SwaraSequence, SwaraType
from raga.music.swaras import NOTATION_MAP


class SwarNotation:
    """Parse and render Indian music notation."""

    # Regex for a single swara token
    _SWARA_RE = re.compile(
        r"(\.*)"           # leading dots for mandra octave
        r"([A-Z][a-z]*'?|[a-z][a-z]*)"  # swara name
        r"(\**)"           # trailing stars for taar octave
    )

    @classmethod
    def parse(cls, notation_str: str) -> SwaraSequence:
        """Parse a notation string into a SwaraSequence.

        Examples:
            "Sa Re Ga Ma Pa Dha Ni Sa*"
            ".Pa .Dha Sa Re ga Ma Pa"
            "Sa re ga Ma Pa dha ni Sa*"  (Bhairav aroha)
        """
        tokens = notation_str.strip().split()
        swaras: list[Swara] = []

        for token in tokens:
            if token in ("-", "|"):
                continue
            if token == "S":
                # Rest
                swaras.append(Swara(name="S", variant=SwaraType.SHUDDHA, duration=1.0))
                continue

            m = cls._SWARA_RE.fullmatch(token)
            if not m:
                raise ValueError(f"Cannot parse swara token: '{token}'")

            dots, name, stars = m.groups()
            octave = 0
            if dots:
                octave = -len(dots)
            elif stars:
                octave = len(stars)

            if name in NOTATION_MAP:
                sname, variant = NOTATION_MAP[name]
                swaras.append(Swara(name=sname, variant=variant, octave=octave))
            else:
                raise ValueError(f"Unknown swara in notation: '{name}'")

        return SwaraSequence(swaras=swaras)

    @classmethod
    def render(cls, sequence: SwaraSequence, bar_every: Optional[int] = None) -> str:
        """Render a SwaraSequence to notation string."""
        parts: list[str] = []
        for i, s in enumerate(sequence.swaras):
            if bar_every and i > 0 and i % bar_every == 0:
                parts.append("|")
            parts.append(s.notation)
        return " ".join(parts)

    @classmethod
    def render_with_beats(cls, sequence: SwaraSequence, beats_per_bar: int = 4) -> str:
        """Render with beat markers and bar lines for tala alignment."""
        lines: list[str] = []
        bar: list[str] = []
        beat = 0

        for s in sequence.swaras:
            bar.append(s.notation)
            beat += 1
            if beat >= beats_per_bar:
                lines.append(" ".join(bar))
                bar = []
                beat = 0

        if bar:
            lines.append(" ".join(bar))

        return " | ".join(lines)

    @classmethod
    def validate_against_raga(
        cls, sequence: SwaraSequence, allowed_swaras: set[str]
    ) -> list[str]:
        """Check if all swaras in the sequence belong to the raga's note set.

        Returns list of violation descriptions (empty if valid).
        """
        violations: list[str] = []
        for i, s in enumerate(sequence.swaras):
            if s.name == "S":  # rest
                continue
            if s.notation.lstrip(".").rstrip("*") not in allowed_swaras:
                violations.append(
                    f"Position {i}: '{s.notation}' not in raga "
                    f"(allowed: {sorted(allowed_swaras)})"
                )
        return violations
