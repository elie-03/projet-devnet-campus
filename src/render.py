"""Génération des configurations à partir des gabarits Jinja2 et de l'inventaire."""
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from .utils import network_parts

TEMPLATE_DIR = Path(__file__).resolve().parent.parent / "templates"


def _env() -> Environment:
    # StrictUndefined : une variable oubliée lève une erreur au lieu de produire une config vide.
    return Environment(loader=FileSystemLoader(TEMPLATE_DIR), undefined=StrictUndefined,
                       trim_blocks=True, lstrip_blocks=True)


def build_context(inventory: dict, role: str, site_id: int | None) -> dict:
    """Assemble les variables dont le gabarit du rôle a besoin."""
    wan_net, wan_mask, wan_wild = network_parts(inventory["wan"]["network"])
    context = {
        "itf": inventory["interfaces"][role],
        "wan": {**inventory["wan"], "address": wan_net, "mask": wan_mask, "wildcard": wan_wild},
    }
    if role == "firewall":
        fw = inventory["firewall"]
        dmz_net, dmz_mask, dmz_wild = network_parts(fw["dmz_network"])
        context["fw"] = {**fw, "dmz_address": dmz_net, "dmz_mask": dmz_mask, "dmz_wildcard": dmz_wild,
                         "nat": [network_parts(n) for n in fw["nat_sources"]]}
        return context

    if site_id not in inventory["sites"]:
        raise KeyError(f"Site {site_id} absent de l'inventaire")
    site = inventory["sites"][site_id]
    lan_net, lan_mask, lan_wild = network_parts(site["lan"])
    context["site"] = {**site, "id": site_id, "address": lan_net, "mask": lan_mask, "wildcard": lan_wild}
    return context


def render_config(inventory: dict, role: str, site_id: int | None) -> list[str]:
    """Renvoie la configuration du rôle sous forme de liste de commandes (lignes non vides)."""
    text = _env().get_template(f"{role}.j2").render(**build_context(inventory, role, site_id))
    return [line.rstrip() for line in text.splitlines() if line.strip()]
