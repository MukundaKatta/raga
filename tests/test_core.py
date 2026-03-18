"""Tests for Raga."""
from src.core import Raga
def test_init(): assert Raga().get_stats()["ops"] == 0
def test_op(): c = Raga(); c.generate(x=1); assert c.get_stats()["ops"] == 1
def test_multi(): c = Raga(); [c.generate() for _ in range(5)]; assert c.get_stats()["ops"] == 5
def test_reset(): c = Raga(); c.generate(); c.reset(); assert c.get_stats()["ops"] == 0
def test_service_name(): c = Raga(); r = c.generate(); assert r["service"] == "raga"
