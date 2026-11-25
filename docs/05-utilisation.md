# 5. Utilisation, vérifications et retour arrière

[← Poste d'automatisation](04-poste-automatisation.md) · [Étape suivante →](06-depannage.md)

## 1. Tests unitaires (sans lab)

```powershell
pytest -v
```

Attendu : **17 tests réussis**. Ils vérifient la détection des rôles et des sites, les
calculs d'adresses, le contenu des gabarits, l'absence de *portfast* sur les trunks et
l'ajout d'un 4e site sans modifier le code.

## 2. Génération à blanc

```powershell
python run.py --dry-run
Get-ChildItem output
Get-Content output\FW-DMZ.txt
```

Relire les fichiers du dossier `output/` : c'est exactement ce qui sera envoyé.

## 3. Déploiement

```powershell
python run.py
```

Lecture de la synthèse finale :

| État | Signification |
|---|---|
| `OK` | Configuration appliquée et contrôles réussis |
| `À VÉRIFIER` | Configuration appliquée, un contrôle a échoué (souvent OSPF pas encore convergé) : relancer |
| `ÉCHEC` | Équipement non traité : cause dans `logs/` |

Les commandes IOS étant idempotentes, relancer `run.py` ne change rien aux équipements
déjà configurés. Les sauvegardes prises avant modification sont dans `backups/`.

## 4. Vérifications sur les équipements

| Équipement | Commande | Attendu |
|---|---|---|
| SWx-ACC / SWx-CORE | `show vlan-switch brief` | VLAN du site présent |
| SWx-ACC / SWx-CORE | `show interfaces trunk` | Liens montants en *trunking* |
| SWx-CORE | `show spanning-tree vlan <id>` | « This bridge is the root » |
| Rx | `show ip ospf neighbor` | 3 voisins `FULL` |
| Rx | `show ip route ospf` | LAN distants, DMZ, `O*E2 0.0.0.0/0` |
| FW-DMZ | `show zone-pair security` | Deux paires de zones |
| FW-DMZ | `show ip nat translations` | Traductions après un ping vers Internet |

## 5. Tests de bout en bout (VPCS)

| Test | Commande | Attendu |
|---|---|---|
| Intra-VLAN | PC1-DKR : `ping 10.10.10.20` | Succès |
| Inter-sites | PC1-DKR : `ping 10.20.20.10` et `ping 10.30.30.10` | Succès |
| Vers la DMZ | PC1-DKR : `ping 192.168.200.10` | Succès |
| Vers Internet | PC1-DKR : `ping 8.8.8.8` | Succès |
| DMZ vers sites | SRV-DMZ : `ping 10.10.10.10` | **Échec attendu** (isolement de la DMZ) |

## 6. Retour arrière

| Périmètre | Méthode |
|---|---|
| Lab complet | **Edit > Manage snapshots** > restaurer `BOOTSTRAP` |
| Un équipement | Réappliquer le fichier de `backups/` après `erase startup-config` et `reload` |
| Poste Windows | `Remove-NetIPAddress -IPAddress 192.168.10.100 -Confirm:$false` |
| Code | `git revert <commit>` ou `git checkout <commit>` |

## 7. Ajouter un site

Ajouter un bloc dans `sites:` de `inventory.yaml`, par exemple :

```yaml
  4:
    name: THIES
    vlan_id: 40
    vlan_name: USERS-THS
    lan: 10.40.40.0/24
    gateway: 10.40.40.1
    wan_ip: 192.168.100.4
```

puis les adresses de management de R4-…, SW4-CORE et SW4-ACC dans `devices:`.
Aucune modification du code n'est nécessaire.
