
<h1 style="text-align:center;">Bienvenue dans CSV to Mongo</h1>


## CVS TO MONGO est un script python permettant de migrer un fichier CSV vers une base de données Mongo (NoSQL)

### 1. Prérequis: 

Le script nécessite l'installation des modules python suivants:

- Pandas
- Pymongo

### 2. Installation:

- Créer un nouveau dossier dans votre espace de travail
- Entrer dans le dossier nouvellement créer et récupérer le projet en exécutant la commande : git clone https://github.com/nau81000/csv_to_mongo.git

### 3. Utilisation:

- Copier ou renommer le fichier .env.template en .env
- Editer le fichier .env en spécifiant les valeurs des variables correspondant à votre contexte
- Le caractère & permet de créer un index concaténé (plusieurs colonnes)

Ex:

CSV_DATASET_FILENAME=/Users/jdoe/dataset.csv<BR>
DB_SERVER=mongodb://test:test@127.0.0.1:27017/<BR>
DB_NAME=TEST<BR>
COLLECTION_NAME=TEST<BR>
INDEXES=NAME,GENDER,COUNTRY&CITY

- Lancer le programme avec la commande : **python3 migration.py**

### 3. Déroulement du script:

- Lecture du fichier et construction d'un dataframe avec Pandas
- Les colonnes du dataframe de type string sont converties en mode titre (première lettre de chaque mot en majuscule, les autres en minuscule)
- Les doublons du dataframe sont supprimés
- Les indexes de la collection sont supprimés
- La collection est vidée
- Les enregistrements (documents) sont insérés directement dans la collection sans création d'indexes

### 4. Tests:

Lancer la séquence de test avec la commande : **pytest** 
