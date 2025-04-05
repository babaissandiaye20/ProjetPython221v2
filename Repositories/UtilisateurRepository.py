import bcrypt
import json
import uuid
import datetime
from bson import ObjectId
from Models.Utilisateur import Utilisateur
from Database.mongodb import MongoDB
from Database.redisdb import RedisDB

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)

class UtilisateurRepository:
    def __init__(self):
        self.mongo = MongoDB()
        self.redis = RedisDB()
        self.collection_name = "utilisateurs"
        self.session_collection = "sessions"

    def creer_utilisateur(self, utilisateur, role=None):
        if self.mongo.find(self.collection_name, {"email": utilisateur.email}):
            return None

        if self.mongo.find(self.collection_name, {"telephone": utilisateur.telephone}):
            return None

        hashed = bcrypt.hashpw(utilisateur.mot_de_passe.encode('utf-8'), bcrypt.gensalt())
        user_dict = utilisateur.to_dict()
        user_dict["mot_de_passe"] = hashed.decode('utf-8')

        if role and role in Utilisateur.ROLES:
            user_dict["role"] = role

        return self.mongo.insert(self.collection_name, user_dict)

    def authentifier(self, email, mot_de_passe):
        cache_key = f"auth:{email}"
        cached_user = self.redis.get_cache(cache_key)
        if cached_user:
            print("Utilisateur authentifié depuis le cache Redis")
            user = Utilisateur.from_dict(cached_user)
            token = cached_user.get("session_token")
            return user, token

        users = self.mongo.find(self.collection_name, {"email": email})
        if not users:
            return None, None

        user_data = users[0]
        stored_password = user_data["mot_de_passe"].encode('utf-8')

        if bcrypt.checkpw(mot_de_passe.encode('utf-8'), stored_password):
            user = Utilisateur.from_dict(user_data)
            token = str(uuid.uuid4())
            expiration = datetime.datetime.now() + datetime.timedelta(hours=1)

            session_data = {
                "user_id": str(user_data["_id"]),
                "email": email,
                "token": token,
                "expiration": expiration,
                "role": user.role
            }

            self.mongo.insert(self.session_collection, session_data)

            user_data_for_cache = dict(user_data)
            user_data_for_cache["_id"] = str(user_data_for_cache["_id"])
            user_data_for_cache["mot_de_passe"] = "******"
            user_data_for_cache["session_token"] = token

            self.redis.set_cache(cache_key, user_data_for_cache, expire=3600)
            return user, token

        return None, None

    def deconnecter(self, email):
        cache_key = f"auth:{email}"
        self.redis.delete(cache_key)
        self.mongo.delete(self.session_collection, {"email": email})

    def verifier_token(self, token):
        sessions = self.mongo.find(self.session_collection, {"token": token})
        if not sessions:
            return None

        session = sessions[0]
        expiration = session.get("expiration")
        if expiration and datetime.datetime.now() > expiration:
            self.mongo.delete(self.session_collection, {"token": token})
            return None
        return session

    def modifier_mot_de_passe(self, email, ancien_mot_de_passe, nouveau_mot_de_passe):
        users = self.mongo.find(self.collection_name, {"email": email})
        if not users:
            return False

        user_data = users[0]
        stored_password = user_data["mot_de_passe"].encode('utf-8')

        if not bcrypt.checkpw(ancien_mot_de_passe.encode('utf-8'), stored_password):
            return False

        hashed = bcrypt.hashpw(nouveau_mot_de_passe.encode('utf-8'), bcrypt.gensalt())
        result = self.mongo.update(
            self.collection_name,
            {"email": email},
            {"$set": {"mot_de_passe": hashed.decode('utf-8')}}
        )

        self.deconnecter(email)
        return result is not None

    def modifier_role(self, email, nouveau_role):
        if nouveau_role not in Utilisateur.ROLES:
            return False

        result = self.mongo.update(
            self.collection_name,
            {"email": email},
            {"$set": {"role": nouveau_role}}
        )

        self.redis.delete(f"auth:{email}")
        return result is not None

    def rechercher_par_telephone(self, telephone):
        users = self.mongo.find(self.collection_name, {"telephone": telephone})
        if not users:
            return None
        return Utilisateur.from_dict(users[0])
