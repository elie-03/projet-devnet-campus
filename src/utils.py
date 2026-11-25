"""Fonctions communes et pures (sans réseau) : rôles, sites, calculs IP, journalisation."""
import ipaddress
import logging
import re
from datetime import datetime
from pathlib import Path

# Ordre important : le premier motif qui correspond l'emporte.
ROLE_PATTERNS = [
    (re.compile(r"^R\d+-[A-Z0-9]+$", re.IGNORECASE), "router"),
    (re.compile(r"^SW\d+-CORE$", re.IGNORECASE), "core_switch"),
    (re.compile(r"^SW\d+-ACC$", re.IGNORECASE), "access_switch"),
    (re.compile(r"^FW-[A-Z0-9]+$", re.IGNORECASE), "firewall"),
]


def clean_prompt(prompt: str) -> str:
    """Transforme un prompt Cisco ('SW1-CORE#', 'R1-DKR(config)#') en hostname."""
    name = prompt.strip()
    name = re.sub(r"\(.*\)", "", name)      # retire (config), (vlan)...
    return name.rstrip("#>").strip()


def role_from_hostname(hostname: str) -> str:
    """Déduit le rôle d'un équipement à partir de son hostname réel."""
    name = clean_prompt(hostname)
    for pattern, role in ROLE_PATTERNS:
        if pattern.match(name):
            return role
    raise ValueError(f"Rôle inconnu pour le hostname '{hostname}'")


def site_from_hostname(hostname: str) -> int | None:
    """Renvoie le numéro de site (R2-ABJ -> 2). None pour un équipement sans site (FW)."""
    match = re.match(r"^[A-Z]+(\d+)-", clean_prompt(hostname), re.IGNORECASE)
    return int(match.group(1)) if match else None


def network_parts(cidr: str) -> tuple[str, str, str]:
    """'10.10.10.0/24' -> ('10.10.10.0', '255.255.255.0', '0.0.0.255')."""
    net = ipaddress.ip_network(cidr, strict=True)
    return str(net.network_address), str(net.netmask), str(net.hostmask)


def setup_logging(log_dir: str = "logs", level: int = logging.INFO) -> Path:
    """Journalise à la fois dans la console et dans un fichier horodaté."""
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_file = Path(log_dir) / f"run_{datetime.now():%Y%m%d_%H%M%S}.log"
    fmt = logging.Formatter("%(asctime)s | %(levelname)-7s | %(name)s | %(message)s")

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    for handler in (logging.StreamHandler(), logging.FileHandler(log_file, encoding="utf-8")):
        handler.setFormatter(fmt)
        root.addHandler(handler)
    # Paramiko est très bavard : on ne garde que ses avertissements.
    logging.getLogger("paramiko").setLevel(logging.WARNING)
    return log_file
