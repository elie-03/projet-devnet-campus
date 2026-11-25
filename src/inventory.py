"""Chargement et validation de l'inventaire YAML et des identifiants."""
import os
from pathlib import Path

import yaml

REQUIRED_KEYS = ["credentials", "interfaces", "wan", "sites", "firewall", "devices"]


class InventoryError(Exception):
    """Inventaire invalide ou identifiants manquants."""


def load_inventory(path: str | Path) -> dict:
    """Lit l'inventaire et vérifie la présence des sections obligatoires."""
    path = Path(path)
    if not path.is_file():
        raise InventoryError(f"Inventaire introuvable : {path}")
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        raise InventoryError(f"Sections manquantes dans l'inventaire : {', '.join(missing)}")
    if not data["devices"]:
        raise InventoryError("La liste « devices » est vide")
    for site_id, site in data["sites"].items():
        for key in ("vlan_id", "vlan_name", "lan", "gateway", "wan_ip"):
            if key not in site:
                raise InventoryError(f"Site {site_id} : clé « {key} » manquante")
    return data


def load_credentials(inventory: dict) -> dict:
    """Lit les identifiants dans les variables d'environnement (jamais dans le code)."""
    cfg = inventory["credentials"]
    username = os.getenv(cfg["username_env"])
    password = os.getenv(cfg["password_env"])
    if not username or not password:
        raise InventoryError(
            f"Variables d'environnement {cfg['username_env']} / {cfg['password_env']} non définies"
        )
    return {
        "username": username,
        "password": password,
        "secret": os.getenv(cfg.get("secret_env", ""), "") or password,
    }
