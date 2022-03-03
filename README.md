# Interprétation statistiques
## Contenu
- [Sommaire](#transferts-du-fichier-xls-vers-mysql-)
- [Transfert](#une-fois-que-les-modules-ont-été-installé-)
- [Présentation du Script d'analyse](#présentation-sommaire-du-script-)

## Transferts du fichier .xls vers MySQL

Tout d'abord, avant de commencer quoi que ce soit il faut installer les modules qui seront utilisés à la lecture des données et au transfert de ces données si ce n'est pas le cas.

Les modules sont les suivants :
  - pymysql -> Module qui permet d'interagir sur la base de données MySQL avec Python
  - xlrd -> Module qui permet d'utiliser les fichiers .xls avec Python
  - typing -> Module supplémentaire pour l'annotation de type

Ces modules seront donc installables avec le gestionnaire de paquets pip via la commande : 
```console
pip install -r requirements.txt
```

> *le fichier se trouve dans le dossier /Scripts/Python*


### Une fois que les modules ont été installé :
il faut configurer la base de données MySQL *(à noter que le client MySQL doit être installé sur votre machine)*
> Toutes les requêtes SQL sont précodées dans /Scripts/SQL/base.sql afin de gagner du temps lors de l'exécution des requêtes, le client exécutera
> donc toutes les requêtes d'un coup... Cela permet également lors du codage des requêtes de pouvoir éviter les erreurs de déclaration et
> de configuration des tables.
1. Il faut se connecter au client MySQL avec son utilisateur favori 😜
2. Entrer la commande :

```SQL
SOURCE chemin_vers_fichier/base.sql
```
*À noter que la base de données utilise le moteur InnoDB (pour la vitesse d'écriture) et utilise l'encodage UTF-8*

### Pour la partie du transfert de fichier : 
#### la liste des imports est la suivante :
```python
import pymysql
import xlrd
import platform
import os
from sys import exit
from typing import Any
```
Il faut ouvrir le fichier `transfert_data.py` qui se trouve dans le dossier `/Scripts/Python`, une fois le fichier ouvert vous trouverez les dictionnaires Python
qui contiennent les arguments pour la base de données à savoir :
```python
DATABASE = {
    'host' : 'localhost',
    'user' : 'my_user',
    'passwd' : 'my_password',
    'db' : 'my_database', 
}
```
*Il y a également un dictionnaire pour le nom du fichier .xls*

*La variable **SUDO_PASSWORD** ne concerne que les utilisateurs Linux*

Il suffit donc d'y renseigner ses informations pour faire fonctionner correctement le script.

> Pour expliquer brièvement les fonctions qui composent le script :
>   - La fonction **`connect_to_database()`** est une fonction comme son nom l'indique de connexion à la base de données en transformant les keys, value du dictionnaire en kwargs, avec en plus une gestion d'erreur pour les utilisateurs Linux qui permet si le service MySQL n'est pas démarré à corriger cette erreur et de démarrer automatiquement le service grâce à votre mot de passe root renseignable dans la variable **SUDO_PASSWORD**
>   - La fonction **`open_xls_sheet()`** reprend le même principe d'ouverture de fichier xls avec une gestion d'erreur si le fichier est introuvable et fera arrêter le programme si une erreur est rencontrée.
>   - Viens ensuite la fonction **`transfert_data()`** qui vient transférer les données .xls vers MySQL (cette partie manque d'optimisation, elle sera corrigée très prochainement.)

Une fois les informations saisies il suffit d'ouvrir terminal et d'exécuter le script, le transfert se fera automatiquement...
Pour vérifier si le transfert a bien été effectuer : utiliser dans le client MySQL la commande : 
```SQL
SELECT country_id, country_name FROM filtred_data;
```
si il y a des données, c'est parfait, le transfert s'est bien exécuté, nous pouvons passer à la suite du programme.

# Interprétations des données avec matplotlib.pyplot
## Présentation sommaire du script
#### La liste des imports est la suivante :
```python
import pymysql
import os
import platform
from sys import exit
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
```
> *Le script se trouve dans le dossier /Script/Python/data_interpretations.py*
> Il reprend les mêmes bases que le précédent pour la connexion MySQL avec la fonction **`connect_to_database()`**

Le script codé en python également permet donc de faire une interprétation sous graphique des données provenant du fichier .xls puis stocké dans une DB (database)

Pour le rendu le script ouvrira donc 3 fenêtres de graphique en simultanées, il suffira donc de choisir entre :
  - figure 1
  - figure 2
  - figure 3

pour comprendre, les graphiques sont classées par ordres décroissants, donc du pays le plus "heureux" au pays le plus "malheureux", les pays qui seront donc sur la fenêtre figure 3 par exemple seront donc les moins bien classés.

## Présentation des fonctions
La fonction
```python
loop_on_query(column_name: str) -> list
```
  - Cette fonction prend donc en paramètre une chaîne de caractères ***(str)*** et retourne une liste ***(list)***
    - Cette chaîne de caractères correspond au nom de la colonne utilisable lors de la requête SQL, car cette fonction permet de boucler autant de fois qu'il y a de ligne dans notre base et de l'ajouter dans une liste pour l'utilisation de ces données.

La fonction :
```python
loop_on_error_value() -> list
```
  - Cette fonction ne prend aucun paramètre mais retourne aussi une liste ***(list)***
    - Cette fonction est spécifique pour l'utilisation des valeurs d'erreur utilisable dans le rendu graphique pour la boîte à moustache avec l'intervalle de confiance à 95%, elle va donc boucle sur deux colonnes spécifiques qui sont directement appelées dans la fonction, elle retournera une liste de listes sous cette forme ;
    ```python
    [[max_value, min_value], [max_value, min_value], ...]
    ```

La fonction : 
```python
plot_format(df: pd.core.frame.DataFrame, country_sum: list, error_value: list) -> Any:
``` 
  - Cette fonction formate donc les plots pour le rendu graphique, elle prend en paramètre `df` qui correspond au dataframe, qui est donc du type de la classe **pd(panda).core.frame.DataFrame**, `country_sum` qui correspond à la somme des valeurs qui seront stockées dans le DataFrame (nous verrons l'utilité plus tard) c'est donc une ***(list)*** et enfin `error_value` qui est une ***(list)*** et qui est simplement la liste des valeurs d'erreurs qui sont retournées lors de l'appel de la fonction `loop_on_error_value()`, et enfin cette fonction retourne ***(Any)*** (une valeur quelconque)
    - Cette fonction permet de rassembler tous les éléments afin de former un rendu graphique convenable avec des données qui lui sont données en paramètre.

La fonction **`manager() -> None:`** :
  - Cette fonction ne prend aucun paramètre et retourne ***(None)*** (rien), elle est là pour appeler tout les fonctions du programme et manager l'ensemble.
    - Cette fonction permet donc d'instancier toutes nos listes depuis les différentes fonctions prévues à cet effet, et de préformer les listes qui seront utilisées dans la fonction de plot_format(), elle sera donc là comme rotule du programme, et elle permet également l'affichage du graphique.

# Rendu final
## Rendu figure 1
![Rendu1](https://cdn.discordapp.com/attachments/837802340802625536/947663004080689174/rendu.png)
## Rendu figure 2
![Rendu2](https://cdn.discordapp.com/attachments/837802340802625536/947673588918534224/rendu2.png)
## Rendu figure 3
![Rendu3](https://cdn.discordapp.com/attachments/837802340802625536/947673602172518440/rendu3.png)
