import os
import sys
from dotenv import load_dotenv

# Ajouter le dossier parent au path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from migration import build_df, insert_df_to_mongo, check_indexes

class TestMigration:

    def setup_class(cls):
        """ Initialise l'environnement et le dataframe
        """
        # Chargement de l'environnement
        load_dotenv()
        # Construction du dataframe
        cls.dataframe = build_df(os.getenv('SOURCE_URI'))

    def test_df_valeurs_manquantes(self):
        """ Test qu'il n' y a aucune valeur manquante
        """
        # Test qu'il n' y a aucune valeur manquante
        assert not self.dataframe.isna().any().any()

    def test_mongo_insert(self):
        """ Test de l'insertion du dataframe dans une base Mongo
        """
        # Vérification des MONGO_COLLECTION_INDEXES
        indexes = check_indexes(self.dataframe, os.getenv('MONGO_COLLECTION_INDEXES'))
        # Insertion du dataframe dans une base MongoDB
        result = insert_df_to_mongo(
            self.dataframe, os.getenv('MONGO_SERVER_URI'), os.getenv('MONGO_INITDB_DATABASE'), os.getenv('MONGO_COLLECTION_NAME'), eval(os.getenv('MONGO_COLLECTION_SCHEMA')), indexes
        )
        # Test que le dataframe et la base de données ont le même nombre d'enregistrements
        assert result == len(self.dataframe)
