"""Point d'entrée : déploie la configuration sur tous les équipements de l'inventaire.

Exemples :
    python run.py --dry-run          # génère les configs dans output/ sans se connecter
    python run.py                    # déploiement réel
"""
import argparse
import logging
import sys
from pathlib import Path

from src.inventory import InventoryError, load_credentials, load_inventory
from src.render import render_config
from src.utils import role_from_hostname, setup_logging, site_from_hostname

log = logging.getLogger("run")

# Ordre de déploiement : la couche 2 d'abord, puis le routage, puis le pare-feu.
ROLE_ORDER = {"access_switch": 0, "core_switch": 1, "router": 2, "firewall": 3}


def dry_run(inventory: dict) -> None:
    """Génère la config de chaque rôle/site sans aucune connexion (utile pour relire)."""
    out = Path("output")
    out.mkdir(exist_ok=True)
    jobs = [("firewall", None, "FW-DMZ")]
    for site_id in inventory["sites"]:
        jobs += [("router", site_id, f"R{site_id}"), ("core_switch", site_id, f"SW{site_id}-CORE"),
                 ("access_switch", site_id, f"SW{site_id}-ACC")]
    for role, site_id, name in jobs:
        lines = render_config(inventory, role, site_id)
        (out / f"{name}.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        log.info("Config générée : output/%s.txt (%d lignes)", name, len(lines))


def process_device(host: str, inventory: dict, creds: dict) -> dict:
    """Traite un équipement de bout en bout. Toute erreur est capturée par l'appelant."""
    from src.connect import detect_device_type, open_connection
    from src.push_config import backup_running_config, ensure_vlan, push_configuration
    from src.verify import verify_device

    ssh_cfg = inventory.get("ssh", {})
    device_type = detect_device_type(host, creds, ssh_cfg)
    conn = open_connection(host, creds, ssh_cfg, device_type)
    try:
        hostname = conn.find_prompt().rstrip("#>")
        role = role_from_hostname(hostname)
        site_id = site_from_hostname(hostname)
        log.info("%s : hostname=%s rôle=%s site=%s", host, hostname, role, site_id)

        backup_running_config(conn, hostname)
        if role in ("core_switch", "access_switch"):
            site = inventory["sites"][site_id]
            ensure_vlan(conn, site["vlan_id"], site["vlan_name"], inventory["switch_vlan_method"])
        push_configuration(conn, hostname, render_config(inventory, role, site_id))
        checks = verify_device(conn, role, inventory, site_id)
        return {"host": host, "hostname": hostname, "role": role,
                "status": "OK" if all(c["ok"] for c in checks) else "À VÉRIFIER"}
    finally:
        conn.disconnect()


def main() -> int:
    parser = argparse.ArgumentParser(description="Automatisation du lab 3 sites + DMZ")
    parser.add_argument("--inventory", default="inventory.yaml")
    parser.add_argument("--dry-run", action="store_true", help="génère les configs sans se connecter")
    args = parser.parse_args()

    log_file = setup_logging()
    log.info("Journal : %s", log_file)
    try:
        inventory = load_inventory(args.inventory)
        if args.dry_run:
            dry_run(inventory)
            return 0
        creds = load_credentials(inventory)
    except InventoryError as exc:
        log.error("%s", exc)
        return 2

    results = []
    for host in inventory["devices"]:
        try:
            results.append(process_device(host, inventory, creds))
        except Exception as exc:          # un équipement en échec ne bloque pas les autres
            log.error("%s : échec -> %s: %s", host, type(exc).__name__, exc)
            results.append({"host": host, "hostname": "?", "role": "?", "status": "ÉCHEC"})

    log.info("===== SYNTHÈSE =====")
    for r in sorted(results, key=lambda r: ROLE_ORDER.get(r["role"], 9)):
        log.info("%-15s %-10s %-14s %s", r["host"], r["hostname"], r["role"], r["status"])
    return 0 if all(r["status"] == "OK" for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
