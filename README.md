# EDF Tempo screen for RPi-Zero

> A program that fetches **EDF TEMPO** data to sync it on a small E-Ink screen
> 

**N.B.** : Since EDF is French, and only French users can have the Tempo subscription at EDF, the documentation is in French! 🇫🇷

**N.B.** : Puisque le projet est encore en cours, le readme n’est pas encore fini 😉🚧

---

**Tempo For Pi Zero** est un programme Python très simple qui fetch les données Tempo sur [l’API Tempo disponible en libre-service](https://www.api-couleur-tempo.fr/), pour afficher les données sur un écran E-Ink Waveshare de 2.15”.

Photo à venir…

## Avertissement

Ce programme à uniquement été conçu pour l’écran [**Waveshare 2.15inch E-Paper Display (G)**](https://www.waveshare.com/product/raspberry-pi/displays/e-paper/2.15inch-e-paper-hat-plus-g.htm?___SID=U). Il n’a pas été testé sous des versions similaires et antérieures des écrans Waveshare.

Vous pouvez essayer de le faire fonctionner avec d’autres écrans Waveshare, s’il répond à ces conditions : 

- 2.13 ou 2.15 pouces
- Technologie E-Ink à couleurs **rouge**, **jaune**, noir et blanc

Pour les autres écrans, libre à vous de modifier le code pour l’adapter.

## Fonctionnement

Le principe du programme est très simple. Il fetch les données de l’API, et genère une image grâce à la bibliothèque **Pillow** selon les prévisions. Il prend aussi en charge les messages d’erreur.

![Exemple d’image générée](https://github.com/user-attachments/assets/2dd95dfa-6298-4d6d-9f4c-a6a0eab4b2af)


> Même si le texte jaune semble illisible, il l’est beaucoup plus sur l’écran, puisque le blanc de l’image correspond au **fond gris** des écrans E-Ink.
> 

## Pré-requis

Pour faire ce petit appareil chez vous, vous devrez vous munir de :

- Un [**Raspberry Pi Zero WH**](https://www.kubii.com/fr/cartes-nano-ordinateurs/2076-raspberry-pi-zero-wh-kubii-3272496009394.html)
    - Fonctionne aussi avec les Raspberry Pi Zero 2 W, et avec les versions W.
    *Le W est nécéssaire, car il signifie que le Raspberry a une connectivité Wi-Fi.
    Le H quant à lui signifie uniquement que les pins du header sont pré-soudés, cela vous évite du travail.*
- Un [**écran E-Ink Waveshare 2.15 pouces 4 couleurs**](https://www.waveshare.com/product/raspberry-pi/displays/e-paper/2.15inch-e-paper-hat-plus-g.htm?___SID=U) (voir [avertissement](Avertissement))
- Une **carte micro-sd** quelconque pour faire fonctionner le RPi-Zero

## Mise en place


À venir… 🚧
