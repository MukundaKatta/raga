"""Swara (note) definitions with frequency mappings and komal/tivra variants.

Indian classical music uses 12 semitones (shrutis) mapped to 7 swaras,
each with shuddha (natural), komal (flat), or tivra (sharp) variants.
"""

from __future__ import annotations

import numpy as np

from raga.models import Swara, SwaraType

# Base frequency for Sa (middle octave, standard pitch)
SA_FREQ_HZ = 261.63  # C4 equivalent, adjustable

# All 12 chromatic swara positions (semitone offsets from Sa)
SWARA_SEMITONES: dict[str, int] = {
    "Sa": 0,
    "re": 1,    # Komal Re
    "Re": 2,    # Shuddha Re
    "ga": 3,    # Komal Ga
    "Ga": 4,    # Shuddha Ga
    "Ma": 5,    # Shuddha Ma
    "Ma'": 6,   # Tivra Ma
    "Pa": 7,    # Pa (always shuddha)
    "dha": 8,   # Komal Dha
    "Dha": 9,   # Shuddha Dha
    "ni": 10,   # Komal Ni
    "Ni": 11,   # Shuddha Ni
}

# Frequency ratios (just intonation, traditional Indian tuning)
JUST_RATIOS: dict[str, float] = {
    "Sa": 1.0,
    "re": 16 / 15,
    "Re": 9 / 8,
    "ga": 6 / 5,
    "Ga": 5 / 4,
    "Ma": 4 / 3,
    "Ma'": 45 / 32,
    "Pa": 3 / 2,
    "dha": 8 / 5,
    "Dha": 5 / 3,
    "ni": 9 / 5,
    "Ni": 15 / 8,
}

# Mapping from notation string to (name, variant)
NOTATION_MAP: dict[str, tuple[str, SwaraType]] = {
    "Sa": ("Sa", SwaraType.SHUDDHA),
    "Re": ("Re", SwaraType.SHUDDHA),
    "re": ("Re", SwaraType.KOMAL),
    "Ga": ("Ga", SwaraType.SHUDDHA),
    "ga": ("Ga", SwaraType.KOMAL),
    "Ma": ("Ma", SwaraType.SHUDDHA),
    "Ma'": ("Ma", SwaraType.TIVRA),
    "Pa": ("Pa", SwaraType.SHUDDHA),
    "Dha": ("Dha", SwaraType.SHUDDHA),
    "dha": ("Dha", SwaraType.KOMAL),
    "Ni": ("Ni", SwaraType.SHUDDHA),
    "ni": ("Ni", SwaraType.KOMAL),
}

# The 7 shuddha swaras in order
SHUDDHA_SWARAS = ["Sa", "Re", "Ga", "Ma", "Pa", "Dha", "Ni"]

# All 12 notes in chromatic order
CHROMATIC_SWARAS = [
    "Sa", "re", "Re", "ga", "Ga", "Ma", "Ma'", "Pa", "dha", "Dha", "ni", "Ni"
]


def swara_from_notation(notation: str, octave: int = 0, duration: float = 1.0) -> Swara:
    """Create a Swara from notation string like 'Re', 'ga', 'Ma\\''."""
    clean = notation.strip()
    # Handle octave markers
    oct = octave
    if clean.startswith("."):
        oct = -1
        clean = clean[1:]
    elif clean.endswith("*"):
        oct = 1
        clean = clean[:-1]

    if clean in NOTATION_MAP:
        name, variant = NOTATION_MAP[clean]
        return Swara(name=name, variant=variant, octave=oct, duration=duration)

    raise ValueError(f"Unknown swara notation: '{notation}'")


def get_frequency(swara_notation: str, base_sa: float = SA_FREQ_HZ) -> float:
    """Get the frequency in Hz for a swara notation string."""
    clean = swara_notation.strip()
    octave_mult = 1.0
    if clean.startswith("."):
        octave_mult = 0.5
        clean = clean[1:]
    elif clean.endswith("*"):
        octave_mult = 2.0
        clean = clean[:-1]

    if clean not in JUST_RATIOS:
        raise ValueError(f"Unknown swara: '{clean}'")

    return base_sa * JUST_RATIOS[clean] * octave_mult


def get_semitone(swara_notation: str) -> int:
    """Get semitone offset from Sa (0-11) for a swara notation."""
    clean = swara_notation.strip()
    if clean.startswith("."):
        clean = clean[1:]
    elif clean.endswith("*"):
        clean = clean[:-1]
    if clean not in SWARA_SEMITONES:
        raise ValueError(f"Unknown swara: '{clean}'")
    return SWARA_SEMITONES[clean]


def generate_tanpura_frequencies(sa_freq: float = SA_FREQ_HZ) -> np.ndarray:
    """Generate the four tanpura string frequencies: Pa(low), Sa, Sa, Sa(low)."""
    return np.array([
        sa_freq * 0.5 * JUST_RATIOS["Pa"],  # Mandra Pa
        sa_freq,
        sa_freq,
        sa_freq * 0.5,  # Mandra Sa
    ])


def interval_between(swara1: str, swara2: str) -> int:
    """Calculate interval in semitones between two swaras."""
    s1 = get_semitone(swara1)
    s2 = get_semitone(swara2)
    return (s2 - s1) % 12
