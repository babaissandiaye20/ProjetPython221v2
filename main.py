# main.py

import sys
from Repositories.view import AuthConsole
from Database.mongodb import MongoDB
from Database.redisdb import RedisDB


def verifier_connexions():
    """
    Vérifie les connexions à MongoDB et Redis

    Returns:
        tuple: (mongodb_ok, redis_ok)
    """
    print("Vérification des connexions aux bases de données...")

    # Test MongoDB
    try:
        mongo = MongoDB()
        test_data = {"test": "connexion", "message": "Connexion réussie!"}
        result = mongo.insert("test", test_data)
        mongodb_ok = result is not None
    except Exception as e:
        print(f"Erreur MongoDB: {e}")
        mongodb_ok = False

    # Test Redis
    try:
        redis_db = RedisDB()
        ping = redis_db.ping()
        redis_ok = ping
    except Exception as e:
        print(f"Erreur Redis: {e}")
        redis_ok = False

    return mongodb_ok, redis_ok


def main():
    """Fonction principale de l'application"""
    # Vérifier les connexions aux bases de données
    mongodb_ok, redis_ok = verifier_connexions()

    if not mongodb_ok:
        print("❌ Erreur de connexion à MongoDB. Vérifiez votre configuration.")
        sys.exit(1)

    if not redis_ok:
        print("❌ Erreur de connexion à Redis. Vérifiez votre configuration.")
        sys.exit(1)

    print("✅ Connexions aux bases de données établies avec succès.\n")

    # Démarrer l'application
    auth_console = AuthConsole()
    auth_console.afficher_menu_principal()


if __name__ == "__main__":
    main()