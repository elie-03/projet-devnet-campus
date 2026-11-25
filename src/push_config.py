"""Sauvegarde, création des VLAN et envoi de la configuration."""
import logging
from datetime import datetime
from pathlib import Path

log = logging.getLogger(__name__)


def backup_running_config(conn, hostname: str, backup_dir: str = "backups") -> Path:
    """Enregistre le running-config AVANT toute modification (fichier horodaté)."""
    Path(backup_dir).mkdir(parents=True, exist_ok=True)
    output = conn.send_command("show running-config", read_timeout=60)
    path = Path(backup_dir) / f"{hostname}_{datetime.now():%Y%m%d_%H%M%S}.cfg"
    path.write_text(output, encoding="utf-8")
    log.info("%s : sauvegarde -> %s", hostname, path)
    return path


def ensure_vlan(conn, vlan_id: int, vlan_name: str, method: str) -> None:
    """Crée le VLAN selon la méthode supportée par la plate-forme."""
    if method == "vlan_database":
        # EtherSwitch (NM-16ESW) : mode « vlan database » en EXEC, hors mode configuration.
        conn.send_command_timing("vlan database")
        conn.send_command_timing(f"vlan {vlan_id} name {vlan_name}")
        conn.send_command_timing("exit")      # applique les changements
    elif method == "global":
        conn.send_config_set([f"vlan {vlan_id}", f" name {vlan_name}"])
    else:
        raise ValueError(f"Méthode VLAN inconnue : {method}")


def push_configuration(conn, hostname: str, commands: list[str]) -> str:
    """Envoie les commandes, contrôle les erreurs IOS et sauvegarde la configuration."""
    output = conn.send_config_set(commands, read_timeout=60)
    errors = [line for line in output.splitlines() if line.strip().startswith("%")]
    # Les messages « % ... » d'IOS signalent une commande refusée ou incomplète.
    if errors:
        log.warning("%s : messages IOS pendant l'envoi : %s", hostname, " | ".join(errors))
    conn.save_config()
    log.info("%s : %d commandes appliquées et configuration sauvegardée", hostname, len(commands))
    return output
