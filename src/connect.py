"""Connexion SSH : détection automatique du type d'équipement puis ouverture de session."""
import logging

from netmiko import ConnectHandler, SSHDetect

log = logging.getLogger(__name__)


def _base_params(host: str, creds: dict, ssh_cfg: dict) -> dict:
    params = {
        "host": host,
        "username": creds["username"],
        "password": creds["password"],
        "secret": creds["secret"],
        "timeout": ssh_cfg.get("timeout", 20),
    }
    if ssh_cfg.get("legacy_rsa"):
        # Anciens IOS : n'acceptent que la signature ssh-rsa (SHA-1).
        params["disabled_algorithms"] = {"pubkeys": ["rsa-sha2-256", "rsa-sha2-512"]}
    return params


def detect_device_type(host: str, creds: dict, ssh_cfg: dict) -> str:
    """Interroge l'équipement (SSHDetect) pour connaître son device_type Netmiko."""
    detector = SSHDetect(device_type="autodetect", **_base_params(host, creds, ssh_cfg))
    device_type = detector.autodetect()
    detector.connection.disconnect()
    if not device_type:
        raise RuntimeError(f"{host} : type d'équipement non reconnu par SSHDetect")
    log.info("%s : device_type détecté = %s", host, device_type)
    return device_type


def open_connection(host: str, creds: dict, ssh_cfg: dict, device_type: str):
    """Ouvre une session Netmiko et passe en mode privilégié si nécessaire."""
    conn = ConnectHandler(device_type=device_type, **_base_params(host, creds, ssh_cfg))
    if not conn.check_enable_mode():
        conn.enable()
    return conn
