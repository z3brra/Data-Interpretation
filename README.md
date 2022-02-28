# Interprétation statistiques

## Transferts du fichier .xls vers MySQL

Tout d'abord, avant de commencer quoi que ce soit il faut installer les modules qui seront utilisé à la lecture des données et au transfert de ces données si ce n'est pas le cas.

Les modules sont les suivant :
  - pymysql -> Module qui permet d'intéragir sur la base de données MySQL avec Python
  - xlrd -> Module qui permet d'utiliser les fichier .xls avec Python
  - typing -> Module supplémentaire pour l'annotations de type

Ces modules seront donc installables avec le gestionnaire de paquet pip via la commande `pip install -r requirements.txt` 
> *le fichier se trouve dans le dossier /Scripts/Python*


### Une fois que les modules ont été installé :
il faut configurer la base de données MySQL *(à noter que le client MySQL doit être installé sur votre machine)*
> Toute les requêtes SQL sont pré-codées dans le fichier /Scripts/SQL/base.sql afin de gagner du temps lors de l'éxécution des requêtes, le client exécutera
> donc toute les requêtes d'un coup... Cela permet également lors du codage des requêtes de pouvoir éviter les erreurs de déclaration et
> de configuration des tables.
1. Il faut se connecter au client MySQL avec son utilisateur favori 😜
2. Entrer la commande `SOURCE chemin_vers_fichier/base.sql`
*À noter que la base de données utilise le moteur InnoDB (pour la vitesse d'écriture) et utilise l'encodage UTF-8*

### Pour la partie du transfert de fichier : 
#### La liste des import sont les suivants :
```python
import pymysql
import xlrd
import platform
import os
from sys import exit
from typing import Any
```
Il ouvrir le fichier `transfert_data.py` qui se trouve dans le dossier `/Scripts/Python`, une fois le fichier ouvert vous trouverez les dictionnaire Python
qui contiennent les arguments pour la base de données à savoir :
  - L'host
  - L'user (utilisateur)
  - Le password (mot de passe)
  - La database (base de données à utiliser)

*Il y a également un dictionnaire pour le nom du fichier .xls*

*La variable **SUDO_PASSWORD** ne concerne que les utilisateurs Linux*

Il suffit donc d'y rensegner vos informations pour faire fonctionner correctement le script.

> Pour expliquer brièvement les fonctions qui composent le script :
>   - La fonction **`connect_to_database()`** est une fonction comme son nom l'indique de connexion à la base de données en transformant les key, value du dictionnaire en kwargs, avec en plus une gestion d'erreur pour les utilisateurs Linux qui permet si le service MySQL n'est pas démarré de corriger cette erreur et de démarrer automatiquement le service grâce à votre mot de passe root renseignable dans la variable **SUDO_PASSWORD**
>   - La fonction **`open_xls_sheet()`** reprend le même principe d'ouvertur de fichier xls avec une gestion d'erreur si le fichier est introuvable et fera arrêter le programme si une erreur est rencontrée.
>   - Viens ensuite la fonction **`transfert_data()`** qui vient transferer les données .xls vers MySQL (cette partie manque d'optimisation, elle sera corrigée très prochainement.)

Une fois les informations saisie ouvrez votre terminal et éxecutez le script, le transfert se fera automatiquement..
Pour vérifier si le transfert à bien été effectuer : utilisez dans le client MySQL la commande : 
```SQL
SELECT country_id, country_name FROM filtred_data;
```
si vous obtenez des données, c'est parfait, le transfert s'est bien exécuté, nous pouvons passer à la suite du programme.

# Interprétations des données avec matplotlib.pyplot
## Présentation sommaire du script
#### La liste des imports sont les suivants :
```python
from typing import Any
import numpy as np
import pymysql
import os
import platform
from sys import exit

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
```
> *Le script se trouve dans le dossier /Script/Python/data_interpretations.py*
> Il reprend les mêmes bases que le précédent pour la connexion MySQL avec la fonction **`connect_to_database()`**

Le script codé en python également permet donc de faire une interprétation sous graphique des données provenant du fichier .xls puis stockées dans une DB (database)

Pour le rendu le script ouvrira donc 3 fenêtres de graphique en simultanées, il suffira donc de choisir entre :
  - figure 1
  - figure 2
  - figure 3

pour comprendre, les graphiques sont classée par ordre décroissant, donc du pays le plus "heureux" au pays le plus "malheureux", les pays qui seront donc sur la fenêtre figure 3 par exemple seront donc les moins bien classés.

## Présentation des fonctions
La fonction **`loop_on_query(column_name: str) -> list`** :
  - Cette fonction prend donc en paramètre une chaîne de caractère ***(str)*** et retourne une liste ***(list)***
    - Cette chaîne de caractère correspond au nom de la colonne utilisable lors de la requête SQL, car cette fonction permet de boucler autant de fois qu'il y a de ligne dans notre base et de l'ajouter dans une liste pour l'utilisation de ces données.

La fonction **`loop_on_error_value() -> list`** :
  - Cette fonction ne prend aucun paramètre mais retourne aussi une liste ***(list)***
    - Cette fonction est spécifique pour l'utilisation des valeurs d'erreur utilisable dans le rendu graphique pour la boîte à moustache avec l'intervalle de confiance à 95%, elle vas donc boucle sur deux colonnes spécifique qui sont directement appelée dans la fonction, elle retournera une liste de listes sous cette forme `[[max_value, min_value], [max_value, min_value], ...]`

La fonction **`plot_format(df: pd.core.frame.DataFrame, country_sum: list, error_value: list) -> Any:`** : 
  - Cette fonction formatte donc les plot pour le rendu graphique, elle prend en paramètre `df` qui correspond au dataframe, qui est donc du type de la classe **pd(panda).core.frame.DataFrame**, `country_sum` qui correspond à la somme des valeurs qui seront stockés dans le DataFrame (nous verrons l'utilité plus tard) c'est donc une **list**, et enfin `error_value` qui est une **list** et qui est simplement la liste des valeurs d'erreurs qui sont retournées lors de l'appel de la fonction `loop_on_error_value()`, et enfin cette fonction retourne **Any** (une valeur quelconque)
    - Cette fonction permet de rassemebler tout les éléments afin de former un rendu graphique convenable avec des données qui lui sont données en paramètre.

La fonction **`manager() -> None:`** :
  - Cette fonction ne prend aucun paramètre et retourne **None** (rien), elle est là pour appeler tout les fonctions du programme et manager l'ensemble.
    - Cette fonctione permet donc d'intancier toute nos liste depuis les différentes fonctions prévues à cet effet, et de pré-former les listes qui seront utilisées dans la fonction de plot_format(), elle sera donc là comme rotule du programme, et elle permet également l'affichage du graphique.
