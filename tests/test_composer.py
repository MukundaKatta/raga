"""Tests for melody generation, rhythm, and composition building."""

from raga.music.ragas import RagaDatabase
from raga.music.talas import TalaDatabase
from raga.music.swaras import get_semitone, NOTATION_MAP
from raga.composer.melody import MelodyGenerator
from raga.composer.rhythm import RhythmGenerator
from raga.composer.harmonizer import CompositionBuilder


class TestMelodyGenerator:
    def setup_method(self) -> None:
        self.db = RagaDatabase()
        self.yaman = self.db.get("yaman")
        self.gen = MelodyGenerator(self.yaman, seed=42)

    def test_generate_phrase_length(self) -> None:
        phrase = self.gen.generate_phrase(length=8)
        assert len(phrase) == 8

    def test_generate_phrase_raga_compliance(self) -> None:
        """All generated notes must belong to the raga's note set."""
        allowed = self.db.get_allowed_swaras("yaman")
        phrase = self.gen.generate_phrase(length=16)
        for s in phrase.swaras:
            note = s.notation.lstrip(".").rstrip("*")
            assert note in allowed, f"Note {note} not in Yaman: {allowed}"

    def test_generate_multiple_phrases(self) -> None:
        phrases = self.gen.generate(num_beats=32, phrase_length=8)
        total = sum(len(p) for p in phrases)
        assert total == 32

    def test_generate_alap_phrase(self) -> None:
        phrase = self.gen.generate_alap_phrase(length=12)
        assert len(phrase) <= 12

    def test_malkauns_excludes_re_pa(self) -> None:
        """Malkauns must never use Re or Pa."""
        malkauns = self.db.get("malkauns")
        gen = MelodyGenerator(malkauns, seed=42)
        for _ in range(5):
            phrase = gen.generate_phrase(length=16)
            for s in phrase.swaras:
                note = s.notation.lstrip(".").rstrip("*")
                assert note not in ("Re", "re", "Pa"), (
                    f"Malkauns generated forbidden note: {note}"
                )

    def test_bhairav_uses_komal_re_dha(self) -> None:
        """Bhairav should have komal Re and komal Dha in its note set."""
        bhairav = self.db.get("bhairav")
        allowed = self.db.get_allowed_swaras("bhairav")
        assert "re" in allowed
        assert "dha" in allowed
        assert "Re" not in allowed  # shuddha Re not in Bhairav
        assert "Dha" not in allowed  # shuddha Dha not in Bhairav

    def test_deterministic_with_seed(self) -> None:
        gen1 = MelodyGenerator(self.yaman, seed=123)
        gen2 = MelodyGenerator(self.yaman, seed=123)
        p1 = gen1.generate_phrase(length=8)
        p2 = gen2.generate_phrase(length=8)
        assert p1.notation == p2.notation

    def test_different_seeds_produce_different_output(self) -> None:
        gen1 = MelodyGenerator(self.yaman, seed=1)
        gen2 = MelodyGenerator(self.yaman, seed=999)
        p1 = gen1.generate_phrase(length=16)
        p2 = gen2.generate_phrase(length=16)
        # Very unlikely to be identical with different seeds
        assert p1.notation != p2.notation


class TestRhythmGenerator:
    def setup_method(self) -> None:
        self.db = TalaDatabase()
        self.teentaal = self.db.get("teentaal")
        self.gen = RhythmGenerator(self.teentaal, seed=42)

    def test_theka_length(self) -> None:
        theka = self.gen.get_theka()
        assert len(theka) == 16

    def test_variation_length(self) -> None:
        var = self.gen.generate_variation(intensity=0.5)
        assert len(var) == 16

    def test_tihai(self) -> None:
        tihai = self.gen.generate_tihai(phrase_length=3)
        # 3 phrases of 3 + 2 gaps = 11
        assert len(tihai) == 11

    def test_peshkaar(self) -> None:
        peshkaar = self.gen.generate_peshkaar(cycles=3)
        assert len(peshkaar) == 3
        for cycle in peshkaar:
            assert len(cycle) == 16

    def test_kayda(self) -> None:
        kayda = self.gen.generate_kayda(theme_length=4)
        assert len(kayda) >= 2  # theme + at least one variation

    def test_pattern_generation(self) -> None:
        pattern = self.gen.generate_pattern(num_cycles=4)
        assert len(pattern) == 4


class TestCompositionBuilder:
    def setup_method(self) -> None:
        raga_db = RagaDatabase()
        tala_db = TalaDatabase()
        self.yaman = raga_db.get("yaman")
        self.teentaal = tala_db.get("teentaal")
        self.builder = CompositionBuilder(self.yaman, self.teentaal, seed=42)

    def test_compose_all_sections(self) -> None:
        comp = self.builder.compose()
        assert len(comp.sections) == 4
        section_types = [s.section_type.value for s in comp.sections]
        assert section_types == ["alap", "jor", "jhala", "gat"]

    def test_compose_selected_sections(self) -> None:
        comp = self.builder.compose(sections=["alap", "gat"])
        assert len(comp.sections) == 2

    def test_compose_has_phrases(self) -> None:
        comp = self.builder.compose()
        assert comp.total_phrases > 0

    def test_compose_metadata(self) -> None:
        comp = self.builder.compose(title="Test Composition")
        assert comp.title == "Test Composition"
        assert comp.raga == "yaman"
        assert comp.tala == "teentaal"

    def test_compose_invalid_section(self) -> None:
        try:
            self.builder.compose(sections=["invalid"])
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_alap_section(self) -> None:
        alap = self.builder.build_alap(num_phrases=4)
        assert alap.section_type.value == "alap"
        assert len(alap.phrases) == 4
        assert alap.tempo < 1.0  # Alap is slow

    def test_gat_section(self) -> None:
        gat = self.builder.build_gat(num_cycles=4)
        assert gat.section_type.value == "gat"
        assert gat.tala_name == "teentaal"

    def test_serialization_roundtrip(self) -> None:
        comp = self.builder.compose()
        data = comp.model_dump(mode="json")
        from raga.models import Composition
        restored = Composition.model_validate(data)
        assert restored.title == comp.title
        assert restored.total_phrases == comp.total_phrases
