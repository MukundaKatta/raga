"""Tests for raga database, swaras, and notation."""

from raga.models import SwaraType
from raga.music.ragas import RagaDatabase
from raga.music.swaras import (
    get_frequency,
    get_semitone,
    interval_between,
    swara_from_notation,
    SA_FREQ_HZ,
)
from raga.music.notation import SwarNotation
from raga.music.talas import TalaDatabase


class TestRagaDatabase:
    def setup_method(self) -> None:
        self.db = RagaDatabase()

    def test_has_at_least_50_ragas(self) -> None:
        assert self.db.count >= 50

    def test_get_yaman(self) -> None:
        yaman = self.db.get("yaman")
        assert yaman.name == "yaman"
        assert yaman.thaat == "kalyan"
        assert yaman.vadi == "Ga"
        assert yaman.samvadi == "Ni"
        assert "Ma'" in yaman.aroha

    def test_get_bhairav(self) -> None:
        bhairav = self.db.get("bhairav")
        assert "re" in bhairav.aroha  # komal Re
        assert "dha" in bhairav.aroha  # komal Dha

    def test_get_case_insensitive(self) -> None:
        r1 = self.db.get("Yaman")
        r2 = self.db.get("YAMAN")
        assert r1.name == r2.name

    def test_get_nonexistent_raises(self) -> None:
        try:
            self.db.get("nonexistent_raga")
            assert False, "Should have raised KeyError"
        except KeyError:
            pass

    def test_search_by_thaat(self) -> None:
        kalyan_ragas = self.db.by_thaat("kalyan")
        assert len(kalyan_ragas) >= 3
        assert all(r.thaat == "kalyan" for r in kalyan_ragas)

    def test_search_by_mood(self) -> None:
        devotional = self.db.search(mood="devotional")
        assert len(devotional) >= 1

    def test_search_by_time(self) -> None:
        morning = self.db.by_time("morning")
        assert len(morning) >= 1

    def test_all_ragas_have_aroha_avaroha(self) -> None:
        for raga in self.db.list_all():
            assert len(raga.aroha) >= 5, f"{raga.name} aroha too short"
            assert len(raga.avaroha) >= 5, f"{raga.name} avaroha too short"

    def test_all_ragas_have_vadi_samvadi(self) -> None:
        for raga in self.db.list_all():
            assert raga.vadi, f"{raga.name} missing vadi"
            assert raga.samvadi, f"{raga.name} missing samvadi"

    def test_aroha_starts_with_sa(self) -> None:
        for raga in self.db.list_all():
            assert raga.aroha[0] == "Sa", f"{raga.name} aroha should start with Sa"

    def test_avaroha_ends_with_sa(self) -> None:
        for raga in self.db.list_all():
            assert raga.avaroha[-1] == "Sa", f"{raga.name} avaroha should end with Sa"

    def test_get_allowed_swaras(self) -> None:
        swaras = self.db.get_allowed_swaras("yaman")
        assert "Sa" in swaras
        assert "Ma'" in swaras
        assert "Pa" in swaras

    def test_malkauns_pentatonic(self) -> None:
        m = self.db.get("malkauns")
        assert "Re" not in m.aroha and "re" not in m.aroha
        assert "Pa" not in m.aroha

    def test_list_names(self) -> None:
        names = self.db.list_names()
        assert len(names) >= 50
        assert names == sorted(names)


class TestTalaDatabase:
    def setup_method(self) -> None:
        self.db = TalaDatabase()

    def test_has_at_least_20_talas(self) -> None:
        assert self.db.count >= 20

    def test_get_teentaal(self) -> None:
        t = self.db.get("teentaal")
        assert t.beats == 16
        assert len(t.vibhags) == 4
        assert t.sam == 1

    def test_get_ektaal(self) -> None:
        t = self.db.get("ektaal")
        assert t.beats == 12

    def test_get_rupak(self) -> None:
        t = self.db.get("rupak")
        assert t.beats == 7

    def test_by_beats(self) -> None:
        talas_16 = self.db.by_beats(16)
        assert len(talas_16) >= 1
        assert all(t.beats == 16 for t in talas_16)


class TestSwaras:
    def test_sa_frequency(self) -> None:
        freq = get_frequency("Sa")
        assert abs(freq - SA_FREQ_HZ) < 0.01

    def test_pa_frequency(self) -> None:
        freq = get_frequency("Pa")
        expected = SA_FREQ_HZ * 3 / 2
        assert abs(freq - expected) < 0.01

    def test_octave_lower(self) -> None:
        freq = get_frequency(".Sa")
        assert abs(freq - SA_FREQ_HZ * 0.5) < 0.01

    def test_octave_upper(self) -> None:
        freq = get_frequency("Sa*")
        assert abs(freq - SA_FREQ_HZ * 2.0) < 0.01

    def test_semitone_sa(self) -> None:
        assert get_semitone("Sa") == 0

    def test_semitone_pa(self) -> None:
        assert get_semitone("Pa") == 7

    def test_interval(self) -> None:
        assert interval_between("Sa", "Pa") == 7
        assert interval_between("Sa", "Ga") == 4

    def test_swara_from_notation(self) -> None:
        s = swara_from_notation("ga")
        assert s.name == "Ga"
        assert s.variant == SwaraType.KOMAL

    def test_swara_from_notation_tivra(self) -> None:
        s = swara_from_notation("Ma'")
        assert s.name == "Ma"
        assert s.variant == SwaraType.TIVRA

    def test_swara_from_notation_mandra(self) -> None:
        s = swara_from_notation(".Pa")
        assert s.octave == -1

    def test_swara_from_notation_taar(self) -> None:
        s = swara_from_notation("Sa*")
        assert s.octave == 1


class TestNotation:
    def test_parse_simple(self) -> None:
        seq = SwarNotation.parse("Sa Re Ga Ma Pa")
        assert len(seq) == 5
        assert seq.swaras[0].name == "Sa"
        assert seq.swaras[4].name == "Pa"

    def test_parse_komal(self) -> None:
        seq = SwarNotation.parse("Sa re ga Ma Pa dha ni")
        assert seq.swaras[1].variant == SwaraType.KOMAL
        assert seq.swaras[2].variant == SwaraType.KOMAL

    def test_parse_tivra(self) -> None:
        seq = SwarNotation.parse("Sa Re Ga Ma' Pa")
        assert seq.swaras[3].variant == SwaraType.TIVRA

    def test_render_roundtrip(self) -> None:
        original = "Sa Re Ga Ma Pa Dha Ni"
        seq = SwarNotation.parse(original)
        rendered = SwarNotation.render(seq)
        assert rendered == original

    def test_validate_against_raga(self) -> None:
        seq = SwarNotation.parse("Sa Re Ga Ma Pa")
        allowed = {"Sa", "Re", "Ga", "Ma", "Pa", "Dha", "Ni"}
        violations = SwarNotation.validate_against_raga(seq, allowed)
        assert violations == []

    def test_validate_catches_violation(self) -> None:
        seq = SwarNotation.parse("Sa re Ga Ma Pa")
        allowed = {"Sa", "Re", "Ga", "Ma", "Pa", "Dha", "Ni"}  # no komal Re
        violations = SwarNotation.validate_against_raga(seq, allowed)
        assert len(violations) == 1
