from pathlib import Path


SCRIPT = Path(__file__).with_name("capture_production_readback.sh").read_text(encoding="utf-8")


def test_phase4_domain_counter_uses_deployed_domains_table() -> None:
    assert '"domains": "SELECT count(*) FROM domains WHERE tenant_id' in SCRIPT
    assert 'FROM domain_mappings WHERE tenant_id' not in SCRIPT


def test_phase4_cleanup_requires_every_counter_to_be_a_zero_integer() -> None:
    assert 'not isinstance(value, bool) and value == 0' in SCRIPT
