# 6. Dépannage

[← Utilisation](05-utilisation.md) · [Retour au README](../README.md)

| Symptôme | Cause probable | Action |
|---|---|---|
| Ping 192.168.10.x impossible depuis le poste | Nœud Cloud sur la mauvaise interface, ou IP .100 sur la mauvaise carte | Revoir [la préparation de GNS3](02-preparation-gns3.md) ; tester d'abord depuis un VPCS relié à MGMT-SW |
| Netmiko : erreur d'algorithme SSH | IOS 12.4 ne propose que des algorithmes anciens | Laisser `legacy_rsa: true` dans l'inventaire ; régénérer la clé RSA si besoin |
| `SSHDetect` ne reconnaît pas l'équipement | Bannière ou invite inattendue | Tester `ssh admin@<IP>` à la main ; vérifier `privilege 15` sur le compte |
| VLAN absent sur un switch | Mode `vlan database` non appliqué | Tester à la main : `vlan database`, `vlan 10 name TEST`, `exit`, puis `show vlan-switch` |
| `% Invalid input` dans le journal | Commande non prise en charge par l'image | Lire la ligne dans `logs/`, adapter le gabarit, relancer |
| Pas de voisin OSPF `FULL` | Lien WAN, masque ou aire incohérents | `show ip ospf interface brief` ; relancer après convergence |
| Pas d'Internet depuis les postes | Pas d'adresse DHCP sur FW-DMZ Fa1/0 | `show ip interface brief` sur FW-DMZ ; la GNS3 VM doit avoir Internet |
| GNS3 VM à 100 % de CPU | Idle-PC absent ou mauvais | Nœud arrêté > clic droit > **Idle-PC** > valeur marquée `*` |

## Points à valider lors d'un premier déploiement

Ces points reposent sur la documentation et la pratique courante ; ils dépendent des
versions exactes des images et des bibliothèques :

- création des VLAN en mode `vlan database` sur NM-16ESW / IOS 12.4(15)T ;
- acceptation de `switchport trunk encapsulation dot1q` et de `spanning-tree vlan X priority` sur NM-16ESW ;
- compatibilité SSH entre une version récente de Paramiko et IOS 12.4 ;
- pontage du nœud Cloud sur l'interface de la GNS3 VM.

Les retours d'expérience sont bienvenus : ouvrez une *issue* sur le dépôt.
