""" Ce script permet d'importer un fichier CSV dans une base de données MongoDB
"""
import os
import pymongo
import pandas
from dotenv import load_dotenv
from datetime import datetime

def build_df(filename):
    """ Création un dataframe à partir d'un fichier CSV

        Mise en mode titre des colonnes de type string
        Suppression des doublons
    """
    # Construction du dataframe à partir du fichier CSV
    dataframe = pandas.read_csv(filename, delimiter=',')
    # Conversion des colonnes de type string (object) en mode titre (1ère lettre d'un mot en majuscule, les autres en minuscule)
    for col in dataframe.select_dtypes(include='object').columns:
        dataframe[col] = dataframe[col].str.title()
    # Suppression des doublons
    dataframe.drop_duplicates(keep='first', inplace=True)
    # Renvoi du dataframe
    return dataframe

def check_indexes(dataframe, str_indexes):
    """ Vérification que les indexes font partie des colonnes

        Sinon exclusion silencieuse
    """
    indexes = []
    for index1 in str_indexes.split(','):
        # Index combiné ou non ?
        comb_indexes = []
        for index2 in index1.split('&'):
            # Suppression des éventuels espaces
            strip_index = index2.strip()
            for col in dataframe.columns:
                if col.lower() == strip_index.lower():
                    comb_indexes.append((col, pymongo.ASCENDING))
        if comb_indexes:
            indexes.append(comb_indexes)
    print(f"Indexes à créer: {indexes}")
    return indexes

def process_value(value, date_pattern):
    """ Convert some value to the appropriate type

        For example, 2024-10-12 should be a date, not a string
    """
    if date_pattern:
        try:
            value = datetime.strptime(value, date_pattern)
        except Exception:
            pass
    return value
    
def insert_df_to_mongo(dataframe, server, db_name, collection_name, db_schema, indexes, date_pattern):
    """ Insertion des lignes d'un dataframe dans une base de données MongoDB
    """
    # Connexion au serveur MongoDB
    client = pymongo.MongoClient(server)
    inserted_records = 0
    try:
        # Création ou récupération de la base de données 
        db = client[db_name.lower()]
        # Création ou récupération d'une collection
        collection = db[collection_name.lower()]
        # Suppression des indexes
        collection.drop_indexes()
        # Vidage de la collection
        collection.delete_many({})
        # Insertion du dataframe
        inserted_records = 0
        for record in dataframe.to_dict(orient='records'):
            document = {}
            for col in record:
                if db_schema:
                    group = db_schema[col]
                    if group:
                        if group not in document:
                            document[group] = {}
                        document[group][col] = process_value(record[col], date_pattern)
                    else:
                        document[col] = process_value(record[col], date_pattern)
                else:
                    document[col] = process_value(record[col], date_pattern)
            collection.insert_one(document)
            inserted_records += 1
        # Création des indexes
        for index in indexes:
            collection.create_index(index)
    except Exception as e:
        print(str(e))
    finally:
        client.close()
    return inserted_records

def insert_accounts_to_mongo(user_list, server, db_name):
    """ Insertion des comptes utilisateurs dans une base de données MongoDB
    """
    # Connexion au serveur MongoDB
    client = pymongo.MongoClient(server)
    # Création ou récupération de la base de données 
    db = client[db_name.lower()]
    # Supprimer tous les utilisateurs de cette base
    db.command("dropAllUsersFromDatabase")
    # Création ou récupération d'une collection
    for user in user_list:
        db.command("createUser", user['username'], pwd=user['password'], roles=[{"role": user['role'], "db": db_name.lower()}])
    client.close()
    return len(user_list)

def main():
    """ Migration d'un fichier CSV dans une base MongoDB
    """
    # Chargement de l'environnement
    load_dotenv()
    server = os.getenv('DB_SERVER')
    db_name = os.getenv('DB_NAME')
    collection_name = os.getenv('COLLECTION_NAME')
    dataset_filename = os.getenv('CSV_DATASET_FILENAME')
    indexes = os.getenv('INDEXES')
    db_schema = eval(os.getenv('DB_SCHEMA'))
    user_list = eval(os.getenv('USER_ACCOUNTS'))
    date_pattern = os.getenv('DATE_PATTERN')
    # Construction du dataframe 
    dataframe = build_df(dataset_filename)
    # Vérification des indexes en focntion du dataframe
    checked_indexes = check_indexes(dataframe, indexes)
    # Insertion du dataframe dans une base MongoDB
    nb_records = insert_df_to_mongo(dataframe, server, db_name, collection_name, db_schema, checked_indexes, date_pattern)
    # Logger le nombre d'enregistrements écrits
    print(f"{nb_records} enregistrements insérés dans la base {db_name}/{collection_name} sur {server}")
    # Insertion des comptes utilisateurs
    nb_users = insert_accounts_to_mongo(user_list , server, db_name)
    # Logger le nombre d'enregistrements écrits
    print(f"{nb_users} utilisateurs reliés à {server}")

if __name__ == '__main__':
    main()