# 3. Configuration initiale des équipements

[← Préparation de GNS3](02-preparation-gns3.md) · [Étape suivante →](04-poste-automatisation.md)

C'est la **seule configuration saisie à la main**. Elle donne à chaque équipement un nom,
un compte local, une adresse de management et l'accès SSH. Tout le reste est poussé par l'outil.

Remplacer `<MOT_DE_PASSE_ADMIN>` et `<MOT_DE_PASSE_ENABLE>` par vos propres valeurs, identiques
sur tous les équipements. Ne les publiez jamais : l'outil les lit dans des variables d'environnement.

> Le hostname est essentiel : l'outil en déduit le rôle (`R<n>-…` routeur, `SW<n>-CORE`,
> `SW<n>-ACC`, `FW-…` pare-feu) et le numéro de site (le chiffre après R ou SW).

## Routeurs et pare-feu (c7200)

### R1-DKR

```
enable
configure terminal
hostname R1-DKR
no ip domain-lookup
ip domain-name lab.local
username admin privilege 15 secret <MOT_DE_PASSE_ADMIN>
enable secret <MOT_DE_PASSE_ENABLE>
interface FastEthernet1/0
 description OOB-MANAGEMENT
 ip address 192.168.10.1 255.255.255.0
 no shutdown
exit
crypto key generate rsa general-keys modulus 2048
ip ssh version 2
line vty 0 4
 login local
 transport input ssh
 exec-timeout 30 0
end
write memory
```

### R2-ABJ

```
enable
configure terminal
hostname R2-ABJ
no ip domain-lookup
ip domain-name lab.local
username admin privilege 15 secret <MOT_DE_PASSE_ADMIN>
enable secret <MOT_DE_PASSE_ENABLE>
interface FastEthernet1/0
 description OOB-MANAGEMENT
 ip address 192.168.10.2 255.255.255.0
 no shutdown
exit
crypto key generate rsa general-keys modulus 2048
ip ssh version 2
line vty 0 4
 login local
 transport input ssh
 exec-timeout 30 0
end
write memory
```

### R3-SL

```
enable
configure terminal
hostname R3-SL
no ip domain-lookup
ip domain-name lab.local
username admin privilege 15 secret <MOT_DE_PASSE_ADMIN>
enable secret <MOT_DE_PASSE_ENABLE>
interface FastEthernet1/0
 description OOB-MANAGEMENT
 ip address 192.168.10.3 255.255.255.0
 no shutdown
exit
crypto key generate rsa general-keys modulus 2048
ip ssh version 2
line vty 0 4
 login local
 transport input ssh
 exec-timeout 30 0
end
write memory
```

### FW-DMZ

```
enable
configure terminal
hostname FW-DMZ
no ip domain-lookup
ip domain-name lab.local
username admin privilege 15 secret <MOT_DE_PASSE_ADMIN>
enable secret <MOT_DE_PASSE_ENABLE>
interface FastEthernet1/1
 description OOB-MANAGEMENT
 ip address 192.168.10.4 255.255.255.0
 no shutdown
exit
crypto key generate rsa general-keys modulus 2048
ip ssh version 2
line vty 0 4
 login local
 transport input ssh
 exec-timeout 30 0
end
write memory
```

## Switchs (c3725 EtherSwitch)

Clé RSA de 1024 bits : la génération en 2048 bits est très lente sur ce processeur émulé.

### SW1-CORE

```
enable
configure terminal
hostname SW1-CORE
no ip domain-lookup
ip domain-name lab.local
username admin privilege 15 secret <MOT_DE_PASSE_ADMIN>
enable secret <MOT_DE_PASSE_ENABLE>
interface FastEthernet0/0
 description OOB-MANAGEMENT
 ip address 192.168.10.11 255.255.255.0
 no shutdown
exit
crypto key generate rsa general-keys modulus 1024
ip ssh version 2
line vty 0 4
 login local
 transport input ssh
 exec-timeout 30 0
end
write memory
```

### SW1-ACC

```
enable
configure terminal
hostname SW1-ACC
no ip domain-lookup
ip domain-name lab.local
username admin privilege 15 secret <MOT_DE_PASSE_ADMIN>
enable secret <MOT_DE_PASSE_ENABLE>
interface FastEthernet0/0
 description OOB-MANAGEMENT
 ip address 192.168.10.12 255.255.255.0
 no shutdown
exit
crypto key generate rsa general-keys modulus 1024
ip ssh version 2
line vty 0 4
 login local
 transport input ssh
 exec-timeout 30 0
end
write memory
```

### SW2-CORE

```
enable
configure terminal
hostname SW2-CORE
no ip domain-lookup
ip domain-name lab.local
username admin privilege 15 secret <MOT_DE_PASSE_ADMIN>
enable secret <MOT_DE_PASSE_ENABLE>
interface FastEthernet0/0
 description OOB-MANAGEMENT
 ip address 192.168.10.13 255.255.255.0
 no shutdown
exit
crypto key generate rsa general-keys modulus 1024
ip ssh version 2
line vty 0 4
 login local
 transport input ssh
 exec-timeout 30 0
end
write memory
```

### SW2-ACC

```
enable
configure terminal
hostname SW2-ACC
no ip domain-lookup
ip domain-name lab.local
username admin privilege 15 secret <MOT_DE_PASSE_ADMIN>
enable secret <MOT_DE_PASSE_ENABLE>
interface FastEthernet0/0
 description OOB-MANAGEMENT
 ip address 192.168.10.14 255.255.255.0
 no shutdown
exit
crypto key generate rsa general-keys modulus 1024
ip ssh version 2
line vty 0 4
 login local
 transport input ssh
 exec-timeout 30 0
end
write memory
```

### SW3-CORE

```
enable
configure terminal
hostname SW3-CORE
no ip domain-lookup
ip domain-name lab.local
username admin privilege 15 secret <MOT_DE_PASSE_ADMIN>
enable secret <MOT_DE_PASSE_ENABLE>
interface FastEthernet0/0
 description OOB-MANAGEMENT
 ip address 192.168.10.15 255.255.255.0
 no shutdown
exit
crypto key generate rsa general-keys modulus 1024
ip ssh version 2
line vty 0 4
 login local
 transport input ssh
 exec-timeout 30 0
end
write memory
```

### SW3-ACC

```
enable
configure terminal
hostname SW3-ACC
no ip domain-lookup
ip domain-name lab.local
username admin privilege 15 secret <MOT_DE_PASSE_ADMIN>
enable secret <MOT_DE_PASSE_ENABLE>
interface FastEthernet0/0
 description OOB-MANAGEMENT
 ip address 192.168.10.16 255.255.255.0
 no shutdown
exit
crypto key generate rsa general-keys modulus 1024
ip ssh version 2
line vty 0 4
 login local
 transport input ssh
 exec-timeout 30 0
end
write memory
```

## Postes VPCS

```
# PC1-DKR / PC2-DKR
ip 10.10.10.10/24 10.10.10.1
ip 10.10.10.20/24 10.10.10.1
# PC1-ABJ / PC2-ABJ
ip 10.20.20.10/24 10.20.20.1
ip 10.20.20.20/24 10.20.20.1
# PC1-SL / PC2-SL
ip 10.30.30.10/24 10.30.30.1
ip 10.30.30.20/24 10.30.30.1
# SRV-DMZ
ip 192.168.200.10/24 192.168.200.254
# puis, sur chaque VPCS :
save
```

## Vérification de l'accès SSH

```powershell
1..4 + 11..16 | ForEach-Object {
  Test-NetConnection "192.168.10.$_" -Port 22 | Select-Object RemoteAddress, TcpTestSucceeded }
```

Attendu : `TcpTestSucceeded = True` pour les 10 équipements.

## Point de remise à zéro

Une fois les 10 équipements joignables : **Edit > Manage snapshots > Create**, nom
`BOOTSTRAP`. Restaurer cet instantané avant chaque nouvel essai permet de repartir d'un
lab « management uniquement ».
