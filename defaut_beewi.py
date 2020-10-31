#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adresses de capteurs bidons, afin de préserver
la confidentialité sur GitHub
"""
from beewi_smartclim import BeewiSmartClimPoller

CAPTEUR_EXT = BeewiSmartClimPoller("20:20:20:20:20:20")
CAPTEUR_INT = BeewiSmartClimPoller("20:20:20:20:20:21")

# Intervalle entre deux mesures, en secondes :
INTERVALLE = 5*60

# Fichier sonore utilisé pour l'alerte :
SON = '/usr/share/sounds/Oxygen-Sys-Warning.ogg'

# Appareil mobile pour l'alerte :
ID_MOBILE = '20202020202020'
