"""Pydantic models for Indian classical music structures."""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class SwaraType(str, Enum):
    """Swara variant types."""

    SHUDDHA = "shuddha"
    KOMAL = "komal"
    TIVRA = "tivra"


class Swara(BaseModel):
    """A single swara (note) in Indian classical music."""

    name: str = Field(description="Swara name: Sa, Re, Ga, Ma, Pa, Dha, Ni")
    variant: SwaraType = Field(default=SwaraType.SHUDDHA)
    octave: int = Field(default=0, description="-1=mandra, 0=madhya, 1=taar")
    duration: float = Field(default=1.0, description="Duration in beats")

    @property
    def notation(self) -> str:
        """Return standard notation string."""
        base = self.name
        if self.variant == SwaraType.KOMAL:
            base = base.lower()
        elif self.variant == SwaraType.TIVRA:
            base = base + "'"
        if self.octave == -1:
            base = "." + base
        elif self.octave == 1:
            base = base + "*"
        return base

    def __str__(self) -> str:
        return self.notation


class SwaraSequence(BaseModel):
    """An ordered sequence of swaras forming a phrase."""

    swaras: list[Swara] = Field(default_factory=list)

    @property
    def notation(self) -> str:
        return " ".join(s.notation for s in self.swaras)

    def __len__(self) -> int:
        return len(self.swaras)


class RagaDefinition(BaseModel):
    """Full definition of a raga."""

    name: str
    thaat: str = Field(default="", description="Parent thaat/melakarta")
    aroha: list[str] = Field(description="Ascending scale notes")
    avaroha: list[str] = Field(description="Descending scale notes")
    vadi: str = Field(description="Most important swara")
    samvadi: str = Field(description="Second most important swara")
    pakad: list[str] = Field(default_factory=list, description="Characteristic phrase")
    varjit_aroha: list[str] = Field(default_factory=list, description="Notes omitted in ascent")
    varjit_avaroha: list[str] = Field(default_factory=list, description="Notes omitted in descent")
    mood: str = Field(default="")
    time: str = Field(default="", description="Prahar / time of performance")
    jati: str = Field(default="sampurna-sampurna", description="Jati classification")
    description: str = Field(default="")


class TalaDefinition(BaseModel):
    """Full definition of a tala."""

    name: str
    beats: int = Field(description="Total matras in one cycle (avartan)")
    vibhags: list[int] = Field(description="Beat groupings")
    bols: list[str] = Field(default_factory=list, description="Syllable pattern")
    sam: int = Field(default=1, description="Sam position")
    khali: list[int] = Field(default_factory=list, description="Khali positions")
    theka: str = Field(default="", description="Basic bol pattern")
    description: str = Field(default="")


class Section(str, Enum):
    """Sections of a classical composition."""

    ALAP = "alap"
    JOR = "jor"
    JHALA = "jhala"
    GAT = "gat"
    STHAYI = "sthayi"
    ANTARA = "antara"
    SANCHARI = "sanchari"
    ABHOG = "abhog"


class CompositionSection(BaseModel):
    """A single section of a composition."""

    section_type: Section
    phrases: list[SwaraSequence] = Field(default_factory=list)
    tala_name: Optional[str] = None
    tempo: float = Field(default=1.0, description="Relative tempo multiplier")
    description: str = Field(default="")


class Composition(BaseModel):
    """A complete musical composition."""

    title: str = Field(default="Untitled")
    raga: str
    tala: str = Field(default="teentaal")
    sections: list[CompositionSection] = Field(default_factory=list)
    tempo_bpm: float = Field(default=80.0)
    description: str = Field(default="")

    @property
    def total_phrases(self) -> int:
        return sum(len(s.phrases) for s in self.sections)
