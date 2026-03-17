"""Database of 20+ talas with beats, vibhags, patterns, and theka.

Covers major Hindustani talas used in classical and semi-classical music.
"""

from __future__ import annotations

from raga.models import TalaDefinition

_TALA_DATA: list[dict] = [
    {
        "name": "teentaal",
        "beats": 16,
        "vibhags": [4, 4, 4, 4],
        "sam": 1,
        "khali": [9],
        "theka": "Dha Dhin Dhin Dha | Dha Dhin Dhin Dha | Dha Tin Tin Ta | Ta Dhin Dhin Dha",
        "bols": [
            "Dha", "Dhin", "Dhin", "Dha",
            "Dha", "Dhin", "Dhin", "Dha",
            "Dha", "Tin", "Tin", "Ta",
            "Ta", "Dhin", "Dhin", "Dha",
        ],
        "description": "The most common tala in Hindustani music. 16 beats, 4 vibhags.",
    },
    {
        "name": "ektaal",
        "beats": 12,
        "vibhags": [2, 2, 2, 2, 2, 2],
        "sam": 1,
        "khali": [3, 7],
        "theka": "Dhin Dhin | DhaGe TiRaKiTa | Tu Na | Kat Ta | DhaGe TiRaKiTa | Dhi Na",
        "bols": [
            "Dhin", "Dhin", "DhaGe", "TiRaKiTa",
            "Tu", "Na", "Kat", "Ta",
            "DhaGe", "TiRaKiTa", "Dhi", "Na",
        ],
        "description": "12-beat tala widely used in khayal, especially vilambit.",
    },
    {
        "name": "jhaptaal",
        "beats": 10,
        "vibhags": [2, 3, 2, 3],
        "sam": 1,
        "khali": [6],
        "theka": "Dhi Na | Dhi Dhi Na | Ti Na | Dhi Dhi Na",
        "bols": [
            "Dhi", "Na", "Dhi", "Dhi", "Na",
            "Ti", "Na", "Dhi", "Dhi", "Na",
        ],
        "description": "10-beat tala with asymmetric vibhag structure.",
    },
    {
        "name": "rupak",
        "beats": 7,
        "vibhags": [3, 2, 2],
        "sam": 1,
        "khali": [1],
        "theka": "Tin Tin Na | Dhi Na | Dhi Na",
        "bols": ["Tin", "Tin", "Na", "Dhi", "Na", "Dhi", "Na"],
        "description": "7-beat tala. Uniquely, sam coincides with khali.",
    },
    {
        "name": "dadra",
        "beats": 6,
        "vibhags": [3, 3],
        "sam": 1,
        "khali": [4],
        "theka": "Dha Dhin Na | Dha Tin Na",
        "bols": ["Dha", "Dhin", "Na", "Dha", "Tin", "Na"],
        "description": "6-beat tala for light classical forms like thumri and dadra.",
    },
    {
        "name": "kaherwa",
        "beats": 8,
        "vibhags": [4, 4],
        "sam": 1,
        "khali": [5],
        "theka": "Dha Ge Na Ti | Na Ka Dhi Na",
        "bols": ["Dha", "Ge", "Na", "Ti", "Na", "Ka", "Dhi", "Na"],
        "description": "8-beat tala for light classical, thumri, and folk.",
    },
    {
        "name": "chautaal",
        "beats": 12,
        "vibhags": [2, 2, 2, 2, 2, 2],
        "sam": 1,
        "khali": [9],
        "theka": "Dha Dha | Dhin Ta | KiTa Dha | Dhin Ta | TiTa KaTa | GaDi GaNa",
        "bols": [
            "Dha", "Dha", "Dhin", "Ta",
            "KiTa", "Dha", "Dhin", "Ta",
            "TiTa", "KaTa", "GaDi", "GaNa",
        ],
        "description": "12-beat tala used in dhrupad.",
    },
    {
        "name": "dhamar",
        "beats": 14,
        "vibhags": [5, 2, 3, 4],
        "sam": 1,
        "khali": [6],
        "theka": "Ka Dhi Ta Dhi Ta | Dha - | Ge Ti Ta | Ti Ta Ta -",
        "bols": [
            "Ka", "Dhi", "Ta", "Dhi", "Ta",
            "Dha", "Ge", "Ti", "Ta", "Ti",
            "Ta", "Ta", "Dha", "Ge",
        ],
        "description": "14-beat tala for dhamar and hori compositions.",
    },
    {
        "name": "tilwada",
        "beats": 16,
        "vibhags": [4, 4, 4, 4],
        "sam": 1,
        "khali": [9],
        "theka": "Dha TiRaKiTa Dhin Dhin | Dha Dha Tin Tin | Ta TiRaKiTa Dhin Dhin | Dha Dha Dhin Dhin",
        "bols": [
            "Dha", "TiRaKiTa", "Dhin", "Dhin",
            "Dha", "Dha", "Tin", "Tin",
            "Ta", "TiRaKiTa", "Dhin", "Dhin",
            "Dha", "Dha", "Dhin", "Dhin",
        ],
        "description": "16-beat tala for vilambit khayal.",
    },
    {
        "name": "adachautaal",
        "beats": 14,
        "vibhags": [2, 2, 2, 2, 2, 2, 2],
        "sam": 1,
        "khali": [3, 11],
        "theka": "Dhin TiRaKiTa | Dhi Na | Tu Na | Kat Ta | DhaGe TiRaKiTa | Dhi Na | Dha Dha",
        "bols": [
            "Dhin", "TiRaKiTa", "Dhi", "Na",
            "Tu", "Na", "Kat", "Ta",
            "DhaGe", "TiRaKiTa", "Dhi", "Na",
            "Dha", "Dha",
        ],
        "description": "14-beat tala used in dhrupad.",
    },
    {
        "name": "deepchandi",
        "beats": 14,
        "vibhags": [3, 4, 3, 4],
        "sam": 1,
        "khali": [4, 11],
        "theka": "Dha Dhin - | Dha Dha Tin - | Ta Tin - | Dha Dha Dhin -",
        "bols": [
            "Dha", "Dhin", "Dha", "Dha", "Dha",
            "Tin", "Ta", "Ta", "Tin", "Dha",
            "Dha", "Dha", "Dhin", "Dha",
        ],
        "description": "14-beat tala for thumri and light classical.",
    },
    {
        "name": "jhoomra",
        "beats": 14,
        "vibhags": [3, 4, 3, 4],
        "sam": 1,
        "khali": [4],
        "theka": "Dhin - DhaGe TiRaKiTa | Dhin DhaGe TiRaKiTa | Tin - DhaGe TiRaKiTa | Dhin DhaGe TiRaKiTa",
        "bols": [
            "Dhin", "DhaGe", "TiRaKiTa", "Dhin",
            "DhaGe", "TiRaKiTa", "Tin", "DhaGe",
            "TiRaKiTa", "Dhin", "DhaGe", "TiRaKiTa",
            "Dhin", "DhaGe",
        ],
        "description": "14-beat tala for slow-tempo vilambit khayal.",
    },
    {
        "name": "sooltaal",
        "beats": 10,
        "vibhags": [2, 2, 2, 2, 2],
        "sam": 1,
        "khali": [5],
        "theka": "Dha Dha | Dhin Ta | KiTa Dha | Dhin Ta | Ta Ta",
        "bols": [
            "Dha", "Dha", "Dhin", "Ta",
            "KiTa", "Dha", "Dhin", "Ta",
            "Ta", "Ta",
        ],
        "description": "10-beat tala used in dhrupad.",
    },
    {
        "name": "tevra",
        "beats": 7,
        "vibhags": [3, 2, 2],
        "sam": 1,
        "khali": [4],
        "theka": "Dha Dhin Ta | TiTa KaTa | GaDi GaNa",
        "bols": ["Dha", "Dhin", "Ta", "TiTa", "KaTa", "GaDi", "GaNa"],
        "description": "7-beat tala used in compositions.",
    },
    {
        "name": "keherwa",
        "beats": 8,
        "vibhags": [4, 4],
        "sam": 1,
        "khali": [5],
        "theka": "Dha Ge Na Ti | Na Ke Dhi Na",
        "bols": ["Dha", "Ge", "Na", "Ti", "Na", "Ke", "Dhi", "Na"],
        "description": "8-beat tala, variant spelling. Common in thumri and bhajan.",
    },
    {
        "name": "chanchar",
        "beats": 14,
        "vibhags": [3, 4, 3, 4],
        "sam": 1,
        "khali": [8],
        "theka": "Dhi Na Dhi | Dhi Na Ti Na | Dhi Na Dhi | Dhi Na Dhi Na",
        "bols": [
            "Dhi", "Na", "Dhi", "Dhi", "Na", "Ti", "Na",
            "Dhi", "Na", "Dhi", "Dhi", "Na", "Dhi", "Na",
        ],
        "description": "14-beat tala used in semi-classical music.",
    },
    {
        "name": "matta",
        "beats": 9,
        "vibhags": [2, 2, 2, 3],
        "sam": 1,
        "khali": [3, 7],
        "theka": "Dhin Dhin | Ta Dhin | Dhin Dhin | Dha Tin Tin",
        "bols": ["Dhin", "Dhin", "Ta", "Dhin", "Dhin", "Dhin", "Dha", "Tin", "Tin"],
        "description": "9-beat tala with interesting asymmetric grouping.",
    },
    {
        "name": "pashto",
        "beats": 7,
        "vibhags": [3, 2, 2],
        "sam": 1,
        "khali": [4],
        "theka": "Dhin Dhin Na | Tin Na | Dhin Na",
        "bols": ["Dhin", "Dhin", "Na", "Tin", "Na", "Dhin", "Na"],
        "description": "7-beat tala popular in ghazal accompaniment.",
    },
    {
        "name": "pancham_sawari",
        "beats": 15,
        "vibhags": [3, 4, 4, 4],
        "sam": 1,
        "khali": [4],
        "theka": "Dhin Dhin DhaGe | TiRaKiTa Dhin Dhin DhaGe | TiRaKiTa Tin Tin DhaGe | TiRaKiTa Dhin Dhin DhaGe",
        "bols": [
            "Dhin", "Dhin", "DhaGe", "TiRaKiTa",
            "Dhin", "Dhin", "DhaGe", "TiRaKiTa",
            "Tin", "Tin", "DhaGe", "TiRaKiTa",
            "Dhin", "Dhin", "DhaGe",
        ],
        "description": "15-beat tala for elaborate compositions.",
    },
    {
        "name": "addha",
        "beats": 16,
        "vibhags": [4, 4, 4, 4],
        "sam": 1,
        "khali": [9],
        "theka": "Dhin TiRaKiTa Dhin Na | Tu Na Kat Ta | Dhin TiRaKiTa Dhin Na | Dha Dha Tin Na",
        "bols": [
            "Dhin", "TiRaKiTa", "Dhin", "Na",
            "Tu", "Na", "Kat", "Ta",
            "Dhin", "TiRaKiTa", "Dhin", "Na",
            "Dha", "Dha", "Tin", "Na",
        ],
        "description": "16-beat tala variant for dhrupad.",
    },
    {
        "name": "brahmtaal",
        "beats": 28,
        "vibhags": [4, 4, 4, 4, 4, 4, 4],
        "sam": 1,
        "khali": [15],
        "theka": "Dha - Dhin - | DhaGe Dhin - Dha | Dha Tin - Tin | DhaGe Dhin - Dha | Dha - Dhin - | DhaGe Dhin - Dha | Dha Tin - Ta",
        "bols": [
            "Dha", "Dhin", "DhaGe", "Dhin",
            "Dha", "Dha", "Tin", "Tin",
            "DhaGe", "Dhin", "Dha", "Dha",
            "Dhin", "DhaGe", "Dhin", "Dha",
            "Dha", "Tin", "Tin", "DhaGe",
            "Dhin", "Dha", "Dha", "Dhin",
            "DhaGe", "Dhin", "Dha", "Ta",
        ],
        "description": "Massive 28-beat tala. One of the longest standard talas.",
    },
    {
        "name": "farodast",
        "beats": 14,
        "vibhags": [3, 4, 3, 4],
        "sam": 1,
        "khali": [8],
        "theka": "Dhin Dha TiRaKiTa | Dha Dhin Dhin Dha | TiRaKiTa Tin Ta | Tin Na Dhin Dha",
        "bols": [
            "Dhin", "Dha", "TiRaKiTa", "Dha",
            "Dhin", "Dhin", "Dha", "TiRaKiTa",
            "Tin", "Ta", "Tin", "Na",
            "Dhin", "Dha",
        ],
        "description": "14-beat tala used in vilambit tempo.",
    },
]


class TalaDatabase:
    """Database of Hindustani talas with lookup and search."""

    def __init__(self) -> None:
        self._talas: dict[str, TalaDefinition] = {}
        for data in _TALA_DATA:
            tala = TalaDefinition(**data)
            self._talas[tala.name.lower()] = tala

    def get(self, name: str) -> TalaDefinition:
        """Get a tala by name (case-insensitive)."""
        key = name.lower().replace(" ", "_")
        if key not in self._talas:
            raise KeyError(
                f"Tala '{name}' not found. Available: {', '.join(sorted(self._talas))}"
            )
        return self._talas[key]

    def list_all(self) -> list[TalaDefinition]:
        """Return all talas sorted by name."""
        return sorted(self._talas.values(), key=lambda t: t.name)

    def list_names(self) -> list[str]:
        """Return sorted list of all tala names."""
        return sorted(self._talas.keys())

    def by_beats(self, beats: int) -> list[TalaDefinition]:
        """Get all talas with a specific beat count."""
        return [t for t in self._talas.values() if t.beats == beats]

    @property
    def count(self) -> int:
        return len(self._talas)
