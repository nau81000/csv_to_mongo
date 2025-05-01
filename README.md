
<h1 style="text-align:center;">Bienvenue dans CSV to Mongo</h1>


## CVS TO MONGO est un script python permettant de migrer un fichier CSV vers une base de données Mongo (NoSQL)

### 1. Prérequis

Le script nécessite l'installation des modules python suivants:

- Python (> 3.6)
- Pandas
- Pymongo
- Dotenv
- Pytest (pour exécuter les tests)

### 2. Installation

- Créer un nouveau dossier dans votre espace de travail
- Entrer dans le dossier nouvellement créer et récupérer le projet en exécutant la commande : git clone https://github.com/nau81000/csv_to_mongo.git

### 3. Configuration

- Copier le fichier templates/.env.template en .env (le .env doit se trouver au même niveau que le script migration.py)
- Editer le fichier .env en spécifiant les valeurs des variables correspondant à votre contexte
- Le caractère & permet de créer un index concaténé (plusieurs colonnes)
- Définir un schéma de données si besoin sinon définir **DB_SCHEMA="{}"**
- Définir les utilisateurs de la base et leur rôle respectif sinon définir **USER_ACCOUNTS="[]"**

### 4. Exemple de configuration

CSV_DATASET_FILENAME=/Users/jdoe/dataset.csv<BR>
DB_SERVER=mongodb://test:test@127.0.0.1:27017/<BR>
DB_NAME=TEST<BR>
COLLECTION_NAME=TEST<BR>
INDEXES=NAME,GENDER,COUNTRY&CITY<BR>
DB_SCHEMA="{'Name': '', 'Age': '', 'Gender': '', 'Blood Type': '', 'Medical Condition': '', 'Insurance Provider': '', 'Hospital': 'Admission', 'Date of Admission': 'Admission', 'Admission Type': 'Admission', 'Doctor': 'Admission', 'Room Number': 'Admission', 'Discharge Date': 'Admission', 'Medication': 'Admission', 'Test Results': 'Admission', 'Billing Amount': 'Admission'}"<BR>
USER_ACCOUNTS="[{'username': 'admin', 'password': 'admin', 'role': 'readWrite'}, {'username': 'user', 'password': 'user', 'role': 'read'}]"<BR>


A partir du schéma de données médicales:

<div style="background-color: #f0f0f0; padding: 5px; border-radius: 5px;">

~~~
{
    "_id"  : "ObjectId",
    "Name" : "string",
    "Age"  : "int",
    "Gender"     : "string",
    "Blood Type" : "string",
    "Medical Condition"  : "string",
    "Insurance Provider" : "string",
    "Admission" : {
        "Date of Admission" : "date",
        "Doctor"            : "string",
        "Hospital"          : "string",
        "Billing Amount"    : "double",
        "Room Number"       : "int",
        "Admission Type"    : "string",
        "Discharge Date"    : "date",
        "Medication"        : "string",
        "Test Results"      : "string"
    }
}
~~~
</div>

### 5. Exécution du script

Lancer le programme avec la commande : **python3 migration.py**

- Lecture du fichier et construction d'un dataframe avec Pandas
- Les colonnes du dataframe de type string sont converties en mode titre (première lettre de chaque mot en majuscule, les autres en minuscule)
- Les doublons du dataframe sont supprimés
- Les indexes de la collection sont supprimés
- La collection est vidée
- Les enregistrements (documents) venant du ficher CSV sont insérés directement dans la collection avec les indexes précisés

Note:
- Une collection d'utilisateurs est automatiquement créée à partir de la variable d'environnement `USER_ACCOUNTS`. Cette collection peut-être utilisée par une application pour contrôler l'accès à la base de données
- Un utilisateur peut avoir un rôle parmi:

| Rôle                   | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `read`                 | Peut lire toutes les collections, **sans écrire**.                          |
| `readWrite`            | Peut lire et écrire dans toutes les collections de la base.                 |
| `readWriteAnyDatabase` | Comme `readWrite`, mais sur **toutes les bases** (doit être assigné sur `admin`). |
| `dbAdmin`              | Gère les index, les statistiques, les validations, etc. (pas les documents).|
| `userAdmin`            | Peut créer, modifier et supprimer les utilisateurs de cette base.          |
| `dbOwner`              | A tous les droits sur la base (`readWrite + dbAdmin + userAdmin`).         |

- Le pré-hachage du mot de passe n'est plus possible avec les versions récentes de MongoDB. Mais si c'était possible, l'algorithme BCRYPT peut remplir cette tâche.

Exemple de création d'un mot de passe avec Python:

```
import bcrypt 
# example password 
password = 'test'
# converting password to array of bytes 
bytes = password.encode('utf-8') 
# generating the salt 
salt = bcrypt.gensalt() 
# Hashing the password 
hash = bcrypt.hashpw(bytes, salt)
```

### 6. Tests

Lancer la séquence de test avec la commande : **pytest** 
