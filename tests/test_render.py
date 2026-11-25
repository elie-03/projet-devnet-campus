from src.inventory import load_inventory
from src.render import render_config

INV = load_inventory("inventory.yaml")


def test_routeur_site2():
    cfg = render_config(INV, "router", 2)
    assert "interface FastEthernet0/0.20" in cfg
    assert " ip address 10.20.20.1 255.255.255.0" in cfg
    assert " network 10.20.20.0 0.0.0.255 area 0" in cfg


def test_portfast_uniquement_sur_ports_acces():
    cfg = render_config(INV, "access_switch", 1)
    portfast_itf = [cfg[i - 4] for i, line in enumerate(cfg) if line.strip() == "spanning-tree portfast"]
    assert portfast_itf == ["interface FastEthernet1/1", "interface FastEthernet1/2"]
    assert "spanning-tree portfast" not in render_config(INV, "core_switch", 1)


def test_pare_feu_nat_et_zones():
    cfg = render_config(INV, "firewall", None)
    assert " permit 10.0.0.0 0.255.255.255" in cfg
    assert "zone-pair security ZP-INSIDE-VERS-DMZ source INSIDE destination DMZ" in cfg


def test_ajout_site_sans_modifier_le_code():
    inv = {**INV, "sites": {**INV["sites"], 4: {"name": "THIES", "vlan_id": 40, "vlan_name": "USERS-THS",
                                                "lan": "10.40.40.0/24", "gateway": "10.40.40.1",
                                                "wan_ip": "192.168.100.4"}}}
    assert "interface FastEthernet0/0.40" in render_config(inv, "router", 4)
