# climatiser.py

Un script python utilisant deux capteurs de température/humidité BeeWi SmartClim pour comparer les températures intérieure et extérieure, avec alerte quand les deux sont égales (utile lors des canicules). Vous pouvez trouver ces capteurs pour environ 23 € pièce. Ils fonctionnent avec deux piles AAA.

Le script affiche les données des deux capteurs à intervalles réguliers et les enregistre dans un fichier au format CSV.

## Installation

Clonez le dépôt GitHub ou téléchargez et extrayez le zip dans un répertoire.

Installez la dépendance principale permettant d'accéder aux capteurs :

```bash
$ pip3 install beewi-smartclim
```
Pour profiter pleinement des fonctionnalités d'alerte du script, il vous faudra installer les paquets suivants (commande pour Ubuntu) :

```bash
$ sudo apt install espeak-ng mbrola-fr1 kdeconnect sox
```
* eSpeak NG et MBROLA sont utilisés pour la synthèse vocale.
* La commande `play` permettant de jouer un son fait partie de SoX.
* KDE Connect permet de lancer des alertes sur votre mobile. Il vous faudra pour cela aussi installer l'application KDE Connect sur votre mobile à partir de l'un de ces dépôts  puis à partir de celle-ci associer votre mobile et votre ordinateur :
    * https://play.google.com/store/apps/details?id=org.kde.kdeconnect_tp&hl=fr_FR
    * https://f-droid.org/fr/packages/org.kde.kdeconnect_tp/
* Il est également possible de lancer des alertes par email. Il vous faudra installer et configurer un serveur SMTP, par exemple ssmtp.

Vous pouvez bien sûr également supprimer ces commandes si vous ne souhaitez pas installer certains paquets : en particulier, si vous n'êtes pas sous KDE, vous pouvez par exemple ne pas souhaiter installer KDE Connect et ses nombreuses dépendances.

Références :

* https://github.com/espeak-ng/espeak-ng
* http://sox.sourceforge.net/
* https://kdeconnect.kde.org/


## Configuration

Créez un fichier `perso_beewi.py` sur le modèle de `defaut_beewi.py` et paramétrez-le :

* `INTERVALLE` : intervalle en secondes entre les mesures.
* `ID_MOBILE` : identifiant KDE Connect de votre téléphone portable ou tablette. Vous pouvez l'obtenir avec la commande `kdeconnect-cli -l`
* `SON` : chemin du fichier son à utiliser pour l'alerte sur ordinateur.
* `CAPTEUR_EXT` et `CAPTEUR_INT` : adresses MAC des deux capteurs Bluetooth, que vous pouvez obtenir avec la commande :

```bash
$ bluetoothctl
[*] [bluetooth]# devices
Device 26:E2:48:48:E2:E2 BeeWi SmartClim
Device D2:7F:B9:23:19:D0 BeeWi SmartClim
...
```

## Utilisation

Une fois définie votre configuration, n'oubliez pas d'apairer les deux capteurs BeeWi SmartClim avec votre ordinateur. Si vous voulez être alerté par votre mobile, n'oubliez pas d'y lancer au préalable l'application KDE Connect.

Il n'y a alors plus qu'à lancer le script dans un terminal :

```bash
$ ./climatiser.py
Batteries : Ext= 100 %    Int= 100 %
   0) 16:04:42 | Ext 22.2°C 65 % | Int 21.9°C 63 %
   1) 16:05:12 | Ext 22.2°C 65 % | Int 21.9°C 63 %
   2) 16:05:32 | Ext 22.2°C 65 % | Int 21.9°C 63 %
   3) 16:05:49 | Ext 22.2°C 65 % | Int 21.9°C 63 %
   4) 16:06:06 | Ext 22.2°C 65 % | Int 21.9°C 63 %
```

Le fichier `climatiser.csv` contient quelques informations supplémentaires telles que la date, l'heure depuis l'epoch, le niveau des batteries :

```csv
31/10/2020;16:04:42;1604156682.8563292;22.2;65;100;21.9;63;100
31/10/2020;16:05:12;1604156712.794185;22.2;65;100;21.9;63;100
31/10/2020;16:05:32;1604156732.8461037;22.2;65;100;21.9;63;100
31/10/2020;16:05:49;1604156749.4508488;22.2;65;100;21.9;63;100
31/10/2020;16:06:06;1604156766.0521727;22.2;65;100;21.9;63;100
```
On pourra l'utiliser pour tracer les courbes de température et d'humidité à l'aide d'une application telle que LibreOffice ou gnuplot.

## Où placer les capteurs BeeWi ?

Mesurer une température est moins simple qu'il n'y paraît. En intérieur, on placera idéalement le capteur loin du sol et des murs qui peuvent avoir emmagasiné de la chaleur, et à une hauteur d'environ 1,50 m, loin bien sûr de toute source de chaleur et sans exposition possible au soleil.

En extérieur, les capteurs doivent être idéalement loin des murs et des sols bétonnés, donc des habitations, et loin des arbres. On pourra s'inspirer des [abris Stevenson](https://fr.wikipedia.org/wiki/Abri_Stevenson) utilisés pour les mesures météorologiques. Ces abris sont peints en blanc et protègent les instruments à la fois du soleil et des intempéries, tout en laissant circuler l'air à travers des doubles persiennes. La porte est orientée vers le nord. Et les thermomètres doivent être à une hauteur comprise entre 1,25 et 2 m.

Voir également : https://www.canada.ca/fr/environnement-changement-climatique/services/meteo-a-oeil/visite-instruments-meteo/thermometres-thermistors.html

## Aspects techniques

### Options des commandes

#### play

* `-q` : supprime l'affichage *(quiet).*

#### espeak-ng

* `-v` : nom de la voix utilisée. Nous utilisons ici les voix MBROLA qui sonnent beaucoup moins synthétiques que la voix robotique de espeak-ng.
* `-s` : vitesse en mots par minute.

#### kdeconnect-cli

* `--refresh` : cherche les périphériques disponibles et rétablit les connexions.
* `--device` : identifiant du périphérique.
* `--ping-msg` : message textuel à envoyer.
* `--ping` : envoie d'un ping.
* `--ring` : fait sonner le mobile.

## Pour aller plus loin

Ce petit projet a été inspiré par l'article suivant, qui va beaucoup plus loin :

  * Colas Sébastien, "Créer sa station météo à l’aide du Raspberry Pi et de son écran 3.5’’ ", ***Linux Pratique,*** n°109, septembre 2018, https://connect.ed-diamond.com/Linux-Pratique/LP-109/Creer-sa-station-meteo-a-l-aide-du-Raspberry-Pi-et-de-son-ecran-3.5

## Références

* Notice des capteurs BeeWi SmartClim : https://www.otio.com/produits/otiohome/environnement1/capteur-de-temperature-et-dhumidite-connecte/#support
* La librairie utilisée pour lire les capteurs : https://github.com/alemuro/beewi_smartclim
* Un autre projet similaire, multi-langages : https://github.com/enrimilan/BeeWi-BBW200-Reader
* Sur la commande `bluetoothctl` : https://www.linux-magazine.com/Issues/2017/197/Command-Line-bluetoothctl
* Ubuntu et le bluetooth :
    * https://doc.ubuntu-fr.org/bluetooth
    * https://core.docs.ubuntu.com/en/stacks/bluetooth/bluez/docs/
