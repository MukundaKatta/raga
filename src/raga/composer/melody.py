"""Melody generator that produces raga-compliant melodies with proper phrasing.

Follows raga grammar rules:
- Uses only swaras from aroha (ascending) and avaroha (descending)
- Emphasizes vadi and samvadi swaras
- Incorporates pakad (characteristic phrases)
- Respects vakra (oblique) movements where applicable
- Handles varjit (omitted) swaras correctly
"""

from __future__ import annotations

from typing import Optional

import numpy as np

from raga.models import RagaDefinition, Swara, SwaraSequence, SwaraType
from raga.music.swaras import CHROMATIC_SWARAS, NOTATION_MAP, get_semitone


class MelodyGenerator:
    """Generate raga-compliant melodies following traditional grammar rules."""

    def __init__(self, raga: RagaDefinition, seed: Optional[int] = None) -> None:
        self.raga = raga
        self.rng = np.random.default_rng(seed)

        # Build note sets
        self._aroha_notes = self._clean_notes(raga.aroha)
        self._avaroha_notes = self._clean_notes(raga.avaroha)
        self._all_notes = sorted(
            set(self._aroha_notes + self._avaroha_notes),
            key=lambda n: get_semitone(n),
        )
        self._pakad = [n.rstrip("*").lstrip(".") for n in raga.pakad] if raga.pakad else []

        # Build probability weights emphasizing vadi/samvadi
        self._weights = self._build_weights()

    @staticmethod
    def _clean_notes(notes: list[str]) -> list[str]:
        """Remove octave markers to get base note names."""
        return [n.rstrip("*").lstrip(".") for n in notes if n not in ("Sa*", ".Sa")]

    def _build_weights(self) -> dict[str, float]:
        """Build swara selection weights respecting raga hierarchy."""
        weights: dict[str, float] = {}
        for note in self._all_notes:
            if note == self.raga.vadi:
                weights[note] = 4.0
            elif note == self.raga.samvadi:
                weights[note] = 3.0
            elif note == "Sa" or note == "Pa":
                weights[note] = 2.0
            else:
                weights[note] = 1.0

        # Boost notes that appear in pakad
        for note in self._pakad:
            if note in weights:
                weights[note] *= 1.5

        return weights

    def _get_direction_notes(self, ascending: bool) -> list[str]:
        """Get allowed notes based on melodic direction."""
        if ascending:
            return self._aroha_notes
        return self._avaroha_notes

    def _weighted_choice(self, candidates: list[str]) -> str:
        """Choose a swara from candidates using raga-weighted probabilities."""
        if not candidates:
            return "Sa"
        w = np.array([self._weights.get(n, 1.0) for n in candidates])
        w = w / w.sum()
        idx = self.rng.choice(len(candidates), p=w)
        return candidates[idx]

    def _note_to_swara(self, notation: str, octave: int = 0) -> Swara:
        """Convert a notation string to a Swara model."""
        if notation in NOTATION_MAP:
            name, variant = NOTATION_MAP[notation]
            return Swara(name=name, variant=variant, octave=octave)
        return Swara(name="Sa", variant=SwaraType.SHUDDHA, octave=octave)

    def _is_ascending_move(self, from_note: str, to_note: str) -> bool:
        """Check if movement from one note to another is ascending."""
        return get_semitone(to_note) > get_semitone(from_note)

    def _get_neighbors(self, current: str, ascending: bool) -> list[str]:
        """Get valid neighboring notes in the given direction."""
        notes = self._get_direction_notes(ascending)
        current_pos = get_semitone(current)

        if ascending:
            return [n for n in notes if get_semitone(n) > current_pos]
        else:
            return [n for n in notes if get_semitone(n) < current_pos]

    def generate_phrase(self, length: int = 8, start_note: Optional[str] = None) -> SwaraSequence:
        """Generate a single raga-compliant phrase.

        Args:
            length: Number of swaras in the phrase.
            start_note: Starting swara notation (default: weighted random).

        Returns:
            A SwaraSequence following raga grammar rules.
        """
        swaras: list[Swara] = []

        # Start note
        if start_note and start_note in self._all_notes:
            current = start_note
        else:
            current = self._weighted_choice(self._all_notes)
        swaras.append(self._note_to_swara(current))

        # Track direction for raga-compliant movement
        ascending = self.rng.random() > 0.5

        for _ in range(length - 1):
            # Occasionally inject pakad fragment
            if self._pakad and self.rng.random() < 0.15 and len(swaras) + 3 <= length:
                start_idx = self.rng.integers(0, max(1, len(self._pakad) - 2))
                frag_len = min(3, len(self._pakad) - start_idx, length - len(swaras))
                for j in range(frag_len):
                    note = self._pakad[start_idx + j]
                    if note in self._all_notes:
                        swaras.append(self._note_to_swara(note))
                        current = note
                if len(swaras) >= length:
                    break
                continue

            # Get neighbors in current direction
            neighbors = self._get_neighbors(current, ascending)

            if not neighbors:
                # Reverse direction at scale boundaries
                ascending = not ascending
                neighbors = self._get_neighbors(current, ascending)

            if not neighbors:
                # Fallback: pick any note
                next_note = self._weighted_choice(self._all_notes)
            else:
                # Prefer stepwise motion with occasional leaps
                if self.rng.random() < 0.7 and len(neighbors) > 1:
                    # Stepwise: pick closest neighbor
                    neighbors_sorted = sorted(
                        neighbors,
                        key=lambda n: abs(get_semitone(n) - get_semitone(current)),
                    )
                    next_note = self._weighted_choice(neighbors_sorted[:3])
                else:
                    next_note = self._weighted_choice(neighbors)

            swaras.append(self._note_to_swara(next_note))
            current = next_note

            # Occasionally change direction for natural phrasing
            if self.rng.random() < 0.25:
                ascending = not ascending

        return SwaraSequence(swaras=swaras[:length])

    def generate(
        self,
        num_beats: int = 16,
        phrase_length: int = 8,
    ) -> list[SwaraSequence]:
        """Generate a full melodic passage as a list of phrases.

        Args:
            num_beats: Total number of beats to generate.
            phrase_length: Swaras per phrase.

        Returns:
            List of SwaraSequence phrases.
        """
        phrases: list[SwaraSequence] = []
        remaining = num_beats

        while remaining > 0:
            plen = min(phrase_length, remaining)
            # Use last note of previous phrase as start for continuity
            start = None
            if phrases and phrases[-1].swaras:
                last = phrases[-1].swaras[-1]
                notation = last.notation.rstrip("*").lstrip(".")
                if notation in self._all_notes:
                    start = notation

            phrase = self.generate_phrase(length=plen, start_note=start)
            phrases.append(phrase)
            remaining -= len(phrase)

        return phrases

    def generate_alap_phrase(self, length: int = 12) -> SwaraSequence:
        """Generate an alap-style phrase: slow, exploratory, emphasizing vadi."""
        swaras: list[Swara] = []
        # Start from Sa
        current = "Sa"
        swaras.append(self._note_to_swara(current))

        # Slowly ascend, dwelling on important notes
        ascending = True
        for _ in range(length - 1):
            neighbors = self._get_neighbors(current, ascending)
            if not neighbors:
                ascending = not ascending
                neighbors = self._get_neighbors(current, ascending)
            if not neighbors:
                next_note = "Sa"
            else:
                # Strong preference for stepwise motion in alap
                neighbors_sorted = sorted(
                    neighbors,
                    key=lambda n: abs(get_semitone(n) - get_semitone(current)),
                )
                next_note = neighbors_sorted[0]

            # Dwell on vadi/samvadi by repeating
            if next_note in (self.raga.vadi, self.raga.samvadi) and self.rng.random() < 0.4:
                swaras.append(self._note_to_swara(next_note, octave=0))
                swaras.append(self._note_to_swara(next_note, octave=0))
            else:
                swaras.append(self._note_to_swara(next_note))

            current = next_note
            if len(swaras) >= length:
                break

            # Gentle direction changes
            if self.rng.random() < 0.15:
                ascending = not ascending

        return SwaraSequence(swaras=swaras[:length])
