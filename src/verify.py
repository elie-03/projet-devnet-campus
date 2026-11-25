"""Vérifications post-déploiement : on interroge l'équipement et on compare à l'attendu."""
import logging

log = logging.getLogger(__name__)


def _check(conn, command: str, expected: str) -> dict:
    output = conn.send_command(command, read_timeout=30)
    return {"command": command, "expected": expected, "ok": expected in output}


def verify_device(conn, role: str, inventory: dict, site_id: int | None) -> list[dict]:
    """Renvoie la liste des contrôles réalisés avec leur résultat (ok True/False)."""
    checks = []
    if role in ("core_switch", "access_switch"):
        vlan_id = str(inventory["sites"][site_id]["vlan_id"])
        vlan_cmd = ("show vlan-switch brief" if inventory["switch_vlan_method"] == "vlan_database"
                    else "show vlan brief")
        checks.append(_check(conn, vlan_cmd, vlan_id))
        checks.append(_check(conn, "show interfaces trunk", "trunking"))
    elif role == "router":
        checks.append(_check(conn, "show ip ospf neighbor", "FULL"))
        checks.append(_check(conn, "show ip route ospf", "O"))
    elif role == "firewall":
        checks.append(_check(conn, "show zone-pair security", "ZP-INSIDE-VERS-OUTSIDE"))
        checks.append(_check(conn, "show ip ospf neighbor", "FULL"))
        checks.append(_check(conn, "show ip route", "Gateway of last resort is"))
    for item in checks:
        log.log(logging.INFO if item["ok"] else logging.WARNING,
                "Contrôle « %s » : %s", item["command"], "OK" if item["ok"] else "ÉCHEC")
    return checks
