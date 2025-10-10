
<h1 style="text-align:center;">Bienvenue dans CSV to Mongo</h1>


## CVS TO MONGO est un script python permettant de migrer un fichier CSV vers une base de données Mongo (NoSQL)

### 1. Prérequis

Le script nécessite l'installation des modules python suivants:

- Python (> 3.6)
- Pandas
- Pymongo
- Dotenv
- Pytest (pour exécuter les tests)

### 2. Structure principale du projet

```
├── migration.py             # Script d'initialisation de la base de données
├── results.pdf              # Résultats d'analyse
```

### 3. Installation

- Créer un nouveau dossier dans votre espace de travail
- Entrer dans le dossier nouvellement créer et récupérer le projet en exécutant la commande : git clone https://github.com/nau81000/csv_to_mongo.git

### 4. Configuration

- Copier le fichier .env.template en .env (le .env doit se trouver au même niveau que le script migration.py)
- Editer le fichier .env en spécifiant les valeurs des variables correspondant à votre contexte
- Le caractère & permet de créer un index concaténé (plusieurs colonnes)
- Définir un schéma de données si besoin sinon définir **MONGO_COLLECTION_SCHEMA="{}"**. Pour chaque colonne, vous pouvez définir un groupe, ou non. Voir exemple un peu plus loin
- Définir les utilisateurs de la base et leur rôle respectif sinon définir **USER_ACCOUNTS="[]"**

Note:

**IL EST TRÈS FORTEMENT RECOMMANDÉ DE CONTRÔLER ET SÉCURISER LES ACCÈS À LA BASE DE DONNÉES.**

### 5. Système d'authentification

Mongo DB utilise le processus d'authentification SCRAM (Salted Challenge Response Authentication Mechanism) par défaut.

À la création de l'utilisateur:

- Le driver (côté client) effectue localement le hachage SCRAM-SHA-256 du mot de passe fourni en clair avec le sel fourni par le serveur (challenge)
- Le mot de passe n’est jamais envoyé en clair sur le réseau
- Le serveur MongoDB stocke une version dérivée et salée du mot de passe, pas le mot de passe brut

Même principe à l'usage:

- Le mot de passe est passé en clair au driver (côté client) 
- Le mot de passe n’est jamais envoyé en clair sur le réseau
- Après un échange client-serveur (envoi de preuve cryptographique), l'utilisateur est authentifié ou non

### 6. Exemple de configuration

```
MONGO_COLLECTION_NAME=test
MONGO_COLLECTION_INDEXES=NAME,GENDER,COUNTRY&CITY
MONGO_COLLECTION_SCHEMA="{'Name': '', 'Age': '', 'Gender': '', 'Blood Type': '', 'Medical Condition': '', 'Insurance Provider': '', 'Hospital': 'Admission', 'Date of Admission': 'Admission', 'Admission Type': 'Admission', 'Doctor': 'Admission', 'Room Number': 'Admission', 'Discharge Date': 'Admission', 'Medication': 'Admission', 'Test Results': 'Admission', 'Billing Amount': 'Admission'}"
MONGO_INITDB_DATABASE=test
MONGO_INITDB_ROOT_USERNAME=root
MONGO_INITDB_ROOT_PASSWORD=root
MONGO_SERVER_URI=mongodb://root:root@mongo_db:27017
SOURCE_URI=https://www.kaggle.com/datasets/prasad22/healthcare-dataset/data?select=healthcare_dataset.csv
USER_ACCOUNTS="[{'username': 'admin', 'password': 'admin', 'role': 'readWrite'}, {'username': 'user', 'password': 'user', 'role': 'read'}]"
```

A partir du schéma de données médicales:

```
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
```

### 7. Exécution du script

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


### 8. Tests

Lancer la séquence de test avec la commande : 

```
pytest
```

Note:

La variable d'environnement MONGO_SERVER_URI est initialement positionnée pour atteindre un serveur Mongo dans un environnement Docker. Si vous lancez les tests dans une console de la machine hôte, il faut faire correspondre le serveur à l'adresse 127.0.0.1

Exemple d'une ligne à rajouter dans /etc/hosts (MacOS ou Linux):

```
127.0.0.1 mongo_db
```

### 9. Déploiement avec Docker et Docker-compose

Docker-compose permet de créer automatiquement l'environnement de travail (création de la base et migration des données).

- Construction de l'environnement avec la commande:

```
docker-compose up -d
```

- Visualisation des logs avec les commandes:

```
docker logs mongo_db
```

```
docker logs mongo_migration
```

- Destruction de l'environnement avec la commande:

```
docker-compose down -v
```
