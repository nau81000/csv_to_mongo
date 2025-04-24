
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
USER_ACCOUNTS={'admin': {'hashpw': b'$2b$12$JR304Lni8IuX/34WR4MsXelyDQgvE5wiiXTs2DwuWNC7qk1x8xccy' , 'role': 'admin', 'privileges': 'CRUD'}, 'user': {'hashpw': b'$2b$12$3u87g5okgHgUuOLDbSNHiuJa/4B8D.SuKytzrmiuxYg.OjN/bvYJS', 'role': 'user', 'privileges': 'R'}}

- Lancer le programme avec la commande : **python3 migration.py**

### 4. Déroulement du script:

- Lecture du fichier et construction d'un dataframe avec Pandas
- Les colonnes du dataframe de type string sont converties en mode titre (première lettre de chaque mot en majuscule, les autres en minuscule)
- Les doublons du dataframe sont supprimés
- Les indexes de la collection sont supprimés
- La collection est vidée
- Les enregistrements (documents) venant du ficher CSV sont insérés directement dans la collection avec les indexes précisés

Note:
- Une collection d'utilisateurs est automatiquement créée à partir de la variable d'environnement `USER_ACCOUNTS`. Cette collection peut-être utilisée par une application pour contrôler l'accès à la base de données
- Un hachage du mot de passe de chaque utilisateur est fortement recommandé. L'algorithme BCRYPT peut remplir cette tâche.

Exemple de création d'un mot de passe avec Python:

~~~
import bcrypt 
# example password 
password = 'test'
# converting password to array of bytes 
bytes = password.encode('utf-8') 
# generating the salt 
salt = bcrypt.gensalt() 
# Hashing the password 
hash = bcrypt.hashpw(bytes, salt)
~~~

### 5. Tests:

Lancer la séquence de test avec la commande : **pytest** 
