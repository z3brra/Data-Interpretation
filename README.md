# Interprétation statistiques

## Transferts du fichier .xls vers MySQL

Tout d'abord, avant de commencer quoi que ce soit il faut importer les modules qui seront utilisé à la lecture des données et au transfert de ces données.

Les modules sont les suivant :
  - pymysql -> Module qui permet d'intéragir sur la base de données MySQL avec Python
  - xlrd -> Module qui permet d'utiliser les fichier .xls avec Python

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
>   - La fonction `connect_to_database()` est une fonction comme son nom l'indique de connexion à la base de données en transformant les key, value du dictionnaire en kwargs, avec en plus une gestion d'erreur pour les utilisateurs Linux qui permet si le service MySQL n'est pas démarré de corriger cette erreur et de démarrer automatiquement le service grâce à votre mot de passe root renseignable dans la variable **SUDO_PASSWORD**
>   - La fonction `open_xls_sheet()` reprend le même principe d'ouvertur de fichier xls avec une gestion d'erreur si le fichier est introuvable et fera arrêter le programme si une erreur est rencontrée.
>   - Viens ensuite la fonction `transfert_data()` qui vient transferer les données .xls vers MySQL (cette partie manque d'optimisation, elle sera corrigée très prochainement.

Une fois les informations saisie ouvrez votre terminal et éxecutez le script, le transfert se fera automatiquement..
Pour vérifier si le transfert à bien été effectuer : utilisez dans le client MySQL la commande : `SELECT country_id, country_name FROM filtred_data;`
si vous obtenez des données, c'est parfait, le transfert s'est bien exécuté, nous pouvons passer à la suite du programme.

