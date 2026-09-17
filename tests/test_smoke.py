"""Smoke test to verify environment, importability, and basic operations."""


def test_imports():
    import astrogit_os

    assert astrogit_os.__version__ == "0.2.0"


def test_hashing_basic():
    from astrogit_os.hashing import generate_state_hash

    sample = {"key": "value"}
    h = generate_state_hash(sample)
    assert isinstance(h, str)
    assert len(h) == 64
