# 2. Préparation de GNS3

[← Architecture](01-architecture.md) · [Étape suivante →](03-configuration-initiale.md)

## Images retenues

| Rôle | Image | RAM / nœud | Pourquoi |
|---|---|---|---|
| Routeurs et pare-feu | c7200 – IOS 15.2(4)S (Advanced Enterprise) | 512 Mo | Sous-interfaces 802.1Q, OSPF, ZBF, NAT, SSH v2 |
| Switchs (×6) | c3725 + module NM-16ESW – IOS 12.4(15)T | 128 Mo | VLAN, trunk 802.1Q, STP par VLAN, *portfast*, très léger |
| Postes et serveur | VPCS (intégré à GNS3) | négligeable | Tests de connectivité |
| Backbone et management | Switch Ethernet intégré | négligeable | Simple segment de couche 2 |
| Internet | Nœud NAT de GNS3 | négligeable | Adresse DHCP et accès réel |

Consommation totale : environ **3 Go de RAM**. Une GNS3 VM à 8 Go et 4 vCPU suffit.

> Les images Cisco ne sont pas fournies : elles sont soumises à licence.
> Pour passer à des images plus récentes (IOSvL2, IOL-L2 dans Cisco Modeling Labs),
> il suffit de régler `switch_vlan_method: global` dans `inventory.yaml`.

## Modèle de routeur c7200

1. **Edit > Preferences > Dynamips > IOS routers > New**, serveur : GNS3 VM.
2. Sélectionner l'image c7200 et accepter sa décompression.
3. RAM 512 Mo ; slot 0 : **C7200-IO-2FE** ; slot 1 : **PA-2FE-TX**.
4. Cliquer sur **Idle-PC finder** et valider la valeur proposée.

## Modèle de switch c3725 EtherSwitch

1. **Dynamips > IOS routers > New**, serveur : GNS3 VM, image c3725.
2. Cocher **This is an EtherSwitch router** : GNS3 ajoute le module NM-16ESW.
3. RAM 128 Mo, puis **Idle-PC finder**.

> **Idle-PC est indispensable** : sans cette valeur, chaque nœud Dynamips consomme
> 100 % d'un cœur, même inactif. Contrôle : `top` sur la GNS3 VM doit montrer les
> processus `dynamips` sous 10 à 20 % au repos.

## Câblage – production

| Extrémité A | Extrémité B | Fonction |
|---|---|---|
| PC1-DKR e0 · PC2-DKR e0 | SW1-ACC Fa1/1 · Fa1/2 | Accès VLAN 10 |
| SW1-ACC Fa1/0 | SW1-CORE Fa1/1 | Trunk |
| SW1-CORE Fa1/0 | R1-DKR Fa0/0 | Trunk (*router-on-a-stick*) |
| R1-DKR Fa0/1 | WAN-BACKBONE port 1 | Backbone |
| Sites 2 et 3 | Même schéma, WAN ports 2 et 3 | VLAN 20 et 30 |
| FW-DMZ Fa0/0 | WAN-BACKBONE port 4 | Zone INSIDE |
| FW-DMZ Fa0/1 | SRV-DMZ e0 | Zone DMZ |
| FW-DMZ Fa1/0 | INTERNET nat0 | Zone OUTSIDE |

## Câblage – management

Le switch MGMT-SW doit avoir au moins 12 ports (clic droit > **Configure**).

| Équipement | Interface | MGMT-SW |
|---|---|---|
| R1-DKR · R2-ABJ · R3-SL | Fa1/0 | ports 0 · 1 · 2 |
| FW-DMZ | Fa1/1 | port 3 |
| SW1-CORE … SW3-ACC | Fa0/0 | ports 4 à 9 |
| MGMT-CLOUD | eth0 de la GNS3 VM | port 10 |

## Relier le management au poste Windows

1. Identifier la carte VMware qui partage le sous-réseau de la GNS3 VM :
   ```powershell
   Get-NetIPAddress -AddressFamily IPv4 | Where-Object IPAddress -like "192.168.18.*" |
     Select-Object InterfaceAlias, IPAddress
   ```
   (adapter `192.168.18.*` à l'adresse affichée par la GNS3 VM)
2. Nœud **MGMT-CLOUD** > **Configure** > **Show special Ethernet interfaces** > `eth0` > **Add**.
3. Ajouter une adresse de management à la carte Windows (PowerShell administrateur) :
   ```powershell
   New-NetIPAddress -InterfaceAlias "VMware Network Adapter VMnet1" `
     -IPAddress 192.168.10.100 -PrefixLength 24
   ```
   Retour arrière : `Remove-NetIPAddress -IPAddress 192.168.10.100 -Confirm:$false`

> Selon la configuration de la GNS3 VM, l'interface à utiliser peut être `eth1` :
> en cas d'échec, vérifier avec `ip addr` sur la VM.
