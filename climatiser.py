#!/usr/bin/env python3
'''
Vincent MAGNIN, 20-09-2020, modifié le 16-06-2021
Un script python utilisant deux capteurs de température/humidité BeeWi SmartClim
pour comparer les températures intérieure et extérieure, avec alerte quand les
deux sont égales (utile lors des canicules).
* Testé avec Python 3.9.5 sous Kubuntu 21.04
* pylint *.py : 5.81/10
* Dépendances :
$ sudo apt install espeak-ng mbrola-fr1 kdeconnect sox
$ pip3 install beewi-smartclim
* https://github.com/alemuro/beewi_smartclim
'''

import locale
import time
import csv
import os
import subprocess

# On essaie de charger votre fichier perso_beewi.py qui contient vos paramètres
# sinon on se rabat sur le fichier par défaut publié sur GitHub :
try:
    from perso_beewi import CAPTEUR_EXT, CAPTEUR_INT, SON, INTERVALLE, ID_MOBILE
except ImportError:
    print("Identifiants de capteurs par défaut")
    from defaut_beewi import CAPTEUR_EXT, CAPTEUR_INT, SON, INTERVALLE, ID_MOBILE


def lecture(capteur):
    """
    Lit et renvoie les données d'un
    capteur BeeWii Smartclim
    """
    capteur.update_sensor()

    temperature = capteur.get_temperature()
    humidite = capteur.get_humidity()
    batterie = capteur.get_battery()

    return temperature, humidite, batterie

#*******************************************************************************
# Programme principal
#*******************************************************************************

# Variables d'environnement pour le synthétiseur vocal espeak-ng :
MON_ENV = os.environ
MON_ENV.update({"AUDIODRIVER":"alsa"})

# Pour l'affichage des dates :
locale.setlocale(locale.LC_ALL, 'fr_FR.utf8')

# On efface le précédent fichier CSV :
NOM_FICHIER = "climatiser.csv"
mon_csv = open(NOM_FICHIER, "w")
mon_csv.close()

atteint = False
iteration = 0

# Boucle infinie à stopper avec CTRL+C :
while True:
    # Quelle heure est-il ?
    jour = time.strftime("%x")
    heure = time.strftime("%X")
    t_epoch = time.time()

    # On récupère les mesures des deux capteurs :
    T_ext, H_ext, B_ext = lecture(CAPTEUR_EXT)
    T_int, H_int, B_int = lecture(CAPTEUR_INT)

    if iteration == 0:
        print("Batteries : Ext=", B_ext, "%    Int=", B_int, "%")
        # Le téléphone portable est-il connecté ?
        ps = subprocess.run(["kdeconnect-cli", "--ping", "--device", ID_MOBILE, "2>", "/dev/null"])
        if ps.returncode != 0:
            print(">>> mobile non connecté...")

    print("%4d)"%iteration, heure, "| Ext", "%.1f°C"%T_ext, H_ext, "%", "| Int", "%.1f°C"%T_int, H_int, "%")

    # De temps en temps on envoie les températures sur le téléphone :
    if iteration%3 == 0:
        message = "Ext=" + "%.1f°C"%T_ext + " ; Int=" + "%.1f°C"%T_int
        ps = subprocess.run(["kdeconnect-cli", "--device", ID_MOBILE, "--ping-msg", message])

    # On ajoute ces mesures à la fin du fichier CSV
    mon_csv = open(NOM_FICHIER, "a")
    fichier = csv.writer(mon_csv, delimiter=";")
    fichier.writerow([jour, heure, t_epoch, T_ext, H_ext, B_ext, T_int, H_int, B_int])
    # Le fermer à chaque fois permet de surveiller son contenu 
    # dans une autre application :
    mon_csv.close()

    # On détecte le moment où les températures vont se croiser :
    if ((not atteint) and (abs(T_ext-T_int) <= 0.1)):
        atteint = True

        message = ">>> Température cible atteinte ! " + "%.1f°C"%T_ext
        print(message)

        if ps.returncode == 0:
            ps = subprocess.run(["kdeconnect-cli", "--device", ID_MOBILE, "--ping-msg", message])
            ps = subprocess.run(["kdeconnect-cli", "--device", ID_MOBILE, "--ring"])
        else:
            print(">>> mobile non connecté...")

        # Alertes sonores sur le PC :
        for i in range(1, 3):
            ps = subprocess.run(["play", "-q", SON], env=MON_ENV)
            ps = subprocess.run(["espeak-ng", "-v", "french-mbrola-1", "-s", "125", message])

    time.sleep(INTERVALLE)
    iteration = iteration + 1
