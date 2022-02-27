# Interprétation statistiques

## Transferts du fichier .xls vers MySQL

Tout d'abord, avant de commencer quoi que ce soit il faut importer les modules qui seront utilisé à la lecture des données et au transfert de ces données.

Les modules sont les suivant :
  - pymysql -> Module qui permet d'intéragir sur la base de données MySQL avec Python
  - xlrd -> Module qui permet d'utiliser les fichier .xls avec Python

Ces modules seront donc installables avec le gestionnaire de paquet pip via la commande `pip install -r requirements.txt` 
> *le fichier se trouve dans le dossier /Scripts/Python*


#### Une fois que les modules ont été installé :
il faut configurer la base de données MySQL *(à noter que le client MySQL doit être installé sur votre machine)*
> Toute les requêtes SQL sont pré-codées dans le fichier /Scripts/SQL/base.sql afin de gagner du temps lors de l'éxécution des requêtes, le client exécutera
> donc toute les requêtes d'un coup... Cela permet également lors du codage des requêtes de pouvoir éviter les erreurs de déclaration et
> de configuration des tables.
1. Il faut se connecter au client MySQL avec son utilisateur favori 😜
2. Entrer la commande `SOURCE chemin_vers_fichier/base.sql`
*À noter que la base de données utilise le moteur InnoDB (pour la vitesse d'écriture) et utilise l'encodage UTF-8*

#### Pour la partie du transfert de fichier : 
Il ouvrir le fichier `transfert_data.py` qui se trouve dans le dossier `/Scripts/Python`, une fois le fichier ouvert vous trouverez les dictionnaire Python
qui contiennent les arguments pour la base de données à savoir :
  - L'host
  - L'user (utilisateur)
  - Le password (mot de passe)
  - La database (base de données à utiliser)

Il suffit donc d'y rensegner vos informations pour faire fonctionner correctement le script.
