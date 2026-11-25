import pytest

from src.utils import clean_prompt, network_parts, role_from_hostname, site_from_hostname


@pytest.mark.parametrize("hostname, role", [
    ("R1-DKR", "router"), ("R3-SL#", "router"), ("SW2-CORE", "core_switch"),
    ("sw1-acc>", "access_switch"), ("FW-DMZ", "firewall"), ("SW1-CORE(config)#", "core_switch"),
])
def test_role_from_hostname(hostname, role):
    assert role_from_hostname(hostname) == role


@pytest.mark.parametrize("hostname", ["Router", "SW1", "CORE-SW1", ""])
def test_role_inconnu_leve_une_erreur(hostname):
    with pytest.raises(ValueError):
        role_from_hostname(hostname)


def test_site_from_hostname():
    assert site_from_hostname("R2-ABJ") == 2
    assert site_from_hostname("SW3-ACC#") == 3
    assert site_from_hostname("FW-DMZ") is None


def test_clean_prompt():
    assert clean_prompt("SW1-CORE(vlan)#") == "SW1-CORE"


def test_network_parts():
    assert network_parts("10.10.10.0/24") == ("10.10.10.0", "255.255.255.0", "0.0.0.255")
    assert network_parts("10.0.0.0/8") == ("10.0.0.0", "255.0.0.0", "0.255.255.255")
