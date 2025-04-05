from Models.Classe import Classe
from Database.mongodb import MongoDB
from Database.redisdb import RedisDB

class ClasseRepository:
    def __init__(self):
        self.mongo = MongoDB()
        self.redis = RedisDB()
        self.collection_name = "classes"

    def creer_classe(self, classe):
        if self.mongo.find(self.collection_name, {"nom": classe.nom}):
            return None

        classe_dict = classe.to_dict()
        result = self.mongo.insert(self.collection_name, classe_dict)
        self.redis.delete("classes:all")
        return result

    def rechercher_par_nom(self, nom):
        cache_key = f"classe:{nom}"
        cached = self.redis.get_cache(cache_key)
        if cached:
            return Classe.from_dict(cached)

        data = self.mongo.find(self.collection_name, {"nom": nom})
        if not data:
            return None

        classe = data[0]
        classe["_id"] = str(classe["_id"])
        self.redis.set_cache(cache_key, classe, expire=3600)
        return Classe.from_dict(classe)

    def lister_toutes(self):
        cache_key = "classes:all"
        cached = self.redis.get_cache(cache_key)
        if cached:
            return [Classe.from_dict(c) for c in cached]

        data = self.mongo.find(self.collection_name, {})
        for c in data:
            c["_id"] = str(c["_id"])
        self.redis.set_cache(cache_key, data, expire=1800)
        return [Classe.from_dict(c) for c in data]

    def ajouter_matiere(self, nom_classe, matiere):
        classe = self.rechercher_par_nom(nom_classe)
        if not classe:
            return False

        if matiere in classe.matieres:
            return True

        result = self.mongo.update(
            self.collection_name,
            {"nom": nom_classe},
            {"$push": {"matieres": matiere}}  # PAS de $set ici !
        )

        self.redis.delete(f"classe:{nom_classe}")
        self.redis.delete("classes:all")

        return result is not None

    def supprimer_matiere(self, nom_classe, matiere):
        result = self.mongo.update(
            self.collection_name,
            {"nom": nom_classe},
            {"$pull": {"matieres": matiere}}
        )
        self.redis.delete(f"classe:{nom_classe}")
        self.redis.delete("classes:all")
        return result is not None

    def modifier_classe(self, nom, nouvelles_donnees):
        result = self.mongo.update(
            self.collection_name,
            {"nom": nom},
            {"$set": nouvelles_donnees}
        )
        self.redis.delete(f"classe:{nom}")
        self.redis.delete("classes:all")
        return result is not None

    def supprimer_classe(self, nom):
        result = self.mongo.delete(self.collection_name, {"nom": nom})
        self.redis.delete(f"classe:{nom}")
        self.redis.delete("classes:all")
        self.redis.delete(f"classe:{nom}:etudiants")
        return result is not None
