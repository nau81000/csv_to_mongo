import os
import sys
from dotenv import load_dotenv

# Ajouter le dossier parent au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from migration import build_df, insert_df_to_mongo, check_indexes

class TestMigration:

    def test_df_construction(self):
        """ Test de la bonne construction du dataframe
        """
        # Chargement de l'environnement
        load_dotenv()
        # Construction du dataframe
        build_df(os.getenv('CSV_DATASET_FILENAME'))
        assert True

    def test_df_valeurs_manquantes(self):
        """ Test qu'il n' y a aucune valeur manquante
        """
        # Chargement de l'environnement
        load_dotenv()
        # Construction du dataframe
        dataframe = build_df(os.getenv('CSV_DATASET_FILENAME'))
        # Test qu'il n' y a aucune valeur manquante
        assert not dataframe.isna().any().any()

    def test_mongo_insert(self):
        """ Test de l'insertion du dataframe dans une Mongo
        """
        # Chargement de l'environnement
        load_dotenv()
        # Construction du dataframe
        dataframe = build_df(os.getenv('CSV_DATASET_FILENAME'))
        # Vérification des indexes
        indexes = check_indexes(dataframe, os.getenv('INDEXES'))
        # Insertion du dataframe dans une base MongoDB
        result = insert_df_to_mongo(dataframe, os.getenv('DB_SERVER'), os.getenv('DB_NAME'), os.getenv('COLLECTION_NAME'), indexes)
        # Test que le dataframe et la base de données ont le même nombre d'enregistrements
        assert result == len(dataframe)
