""" Ce script permet d'importer un fichier CSV dans une base de données MongoDB
"""
import os
import pymongo
import pandas
from dotenv import load_dotenv

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
            if strip_index in dataframe.columns:
                comb_indexes.append(strip_index)
        if comb_indexes:
            indexes.append(comb_indexes)
    return indexes

def insert_df_to_mongo(dataframe, server, db_name, collection_name, indexes):
    """ Insertion des lignes d'un dataframe dans une base de données MongoDB
    """
    # Connexion au serveur MongoDB
    client = pymongo.MongoClient(server)
    # Création ou récupération de la base de données 
    db = client[db_name]
    # Création ou récupération d'une collection
    collection = db[collection_name]
    # Suppression des indexes
    collection.drop_indexes()
    # Vidage de la collection
    collection.delete_many({})
    # Insertion du dataframe
    result = collection.insert_many(dataframe.to_dict(orient='records'))
    # Création des indexes
    for index in indexes:
        collection.create_index(index)
    client.close()
    return len(result.inserted_ids)

def main():
    """ Migration d'un fichier CSV dans une base MongoDB
    """
    # Chargement de l'environnement
    load_dotenv()
    # Construction du dataframe 
    dataframe = build_df(os.getenv('CSV_DATASET_FILENAME'))
    # Vérification des indexes
    indexes = check_indexes(dataframe, os.getenv('INDEXES'))
    # Insertion du dataframe dans une base MongoDB
    insert_df_to_mongo(dataframe, os.getenv('DB_SERVER'), os.getenv('DB_NAME'), os.getenv('COLLECTION_NAME'), indexes)
    # Insertion du dataframe dans une base MongoDB
    server = os.getenv('DB_SERVER')
    db_name = os.getenv('DB_NAME')
    collection_name = os.getenv('COLLECTION_NAME')
    nb_records = insert_df_to_mongo(dataframe, os.getenv('DB_SERVER'), os.getenv('DB_NAME'), os.getenv('COLLECTION_NAME'), indexes)
    # Logger le nombre d'enregistrements écrits
    print(f"{nb_records} enregistrements insérés dans la base {db_name}/{collection_name} sur {server}")


if __name__ == '__main__':
    main()