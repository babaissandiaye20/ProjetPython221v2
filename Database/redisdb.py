# database/redisdb.py

import redis
import json
from bson import ObjectId
import hashlib
from config import REDIS_HOST, REDIS_PORT, REDIS_DB


# JSON Encoder personnalisé pour gérer les ObjectId de MongoDB
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(JSONEncoder, self).default(obj)


class RedisDB:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisDB, cls).__new__(cls)
            cls._instance.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
        return cls._instance

    def ping(self):
        return self.r.ping()

    def set_cache(self, key, value, expire=None):
        # Utiliser l'encodeur personnalisé pour gérer les ObjectId
        value_str = json.dumps(value, cls=JSONEncoder)
        self.r.set(key, value_str, ex=expire)

    def get_cache(self, key):
        value = self.r.get(key)
        if value:
            return json.loads(value)
        return None

    def delete(self, key):
        return self.r.delete(key)

    def find_with_cache(self, collection_name, query, mongo_instance, expire=60):
        """
        Requête MongoDB avec cache automatique.
        """
        # Utiliser l'encodeur personnalisé pour gérer les ObjectId dans la query
        query_str = json.dumps(query, sort_keys=True, cls=JSONEncoder)
        key_hash = hashlib.sha256(query_str.encode()).hexdigest()
        redis_key = f"{collection_name}:{key_hash}"

        cached_result = self.get_cache(redis_key)
        if cached_result:
            print("✅ Données depuis le cache Redis")
            return cached_result

        print("🔄 Données depuis MongoDB")
        result = mongo_instance.find(collection_name, query)
        self.set_cache(redis_key, result, expire=expire)

        return result