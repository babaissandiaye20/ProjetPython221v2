import json
from bson import ObjectId
from Models.Etudiant import Etudiant
from Database.mongodb import MongoDB
from Database.redisdb import RedisDB

class EtudiantRepository:
    def __init__(self):
        self.mongo = MongoDB()
        self.redis = RedisDB()
        self.collection_name = "etudiants"

    def creer_etudiant(self, etudiant):
        existing = self.mongo.find(self.collection_name, {"telephone": etudiant.telephone})
        if existing:
            return None

        if etudiant.notes:
            for note in etudiant.notes.values():
                if not (0 <= note <= 20):
                    return None

        etudiant_dict = etudiant.to_dict()
        result = self.mongo.insert(self.collection_name, etudiant_dict)

        if result:
            etudiant_dict["_id"] = str(result)
            self.redis.set_cache(f"etudiant:{etudiant.telephone}", etudiant_dict, expire=3600)

        return result

    def creer_depuis_utilisateur(self, utilisateur, classe=None):
        if utilisateur.role != "etudiant":
            return None

        etudiant = Etudiant(
            nom=utilisateur.nom,
            prenom=utilisateur.prenom,
            telephone=utilisateur.telephone,
            email=utilisateur.email,
            classe=classe
        )
        return self.creer_etudiant(etudiant)

    def rechercher_par_telephone(self, telephone):
        cache_key = f"etudiant:{telephone}"
        cached = self.redis.get_cache(cache_key)
        if cached:
            return Etudiant.from_dict(cached)

        data = self.mongo.find(self.collection_name, {"telephone": telephone})
        if not data:
            return None

        etudiant_data = data[0]
        etudiant_data["_id"] = str(etudiant_data["_id"])
        self.redis.set_cache(cache_key, etudiant_data, expire=3600)
        return Etudiant.from_dict(etudiant_data)

    def rechercher_par_nom_prenom(self, nom, prenom=None):
        query = {"nom": {"$regex": nom, "$options": "i"}}
        if prenom:
            query["prenom"] = {"$regex": prenom, "$options": "i"}

        data = self.redis.find_with_cache(self.collection_name, query, self.mongo, expire=600)
        return [Etudiant.from_dict(d) for d in data]

    def rechercher_par_classe(self, classe):
        cache_key = f"classe:{classe}:etudiants"
        cached = self.redis.get_cache(cache_key)
        if cached:
            return [Etudiant.from_dict(d) for d in cached]

        data = self.mongo.find(self.collection_name, {"classe": classe})
        for e in data:
            e["_id"] = str(e["_id"])
        self.redis.set_cache(cache_key, data, expire=1800)
        return [Etudiant.from_dict(d) for d in data]

    def lister_tous(self):
        cache_key = "etudiants:all"
        cached = self.redis.get_cache(cache_key)
        if cached:
            return [Etudiant.from_dict(d) for d in cached]

        data = self.mongo.find(self.collection_name, {})
        for e in data:
            e["_id"] = str(e["_id"])
        self.redis.set_cache(cache_key, data, expire=1800)
        return [Etudiant.from_dict(d) for d in data]

    def ajouter_note(self, telephone, matiere, note):
        if not (0 <= note <= 20):
            return False

        result = self.mongo.update(
            self.collection_name,
            {"telephone": telephone},
            {"$set": {f"notes.{matiere}": note}}
        )

        self.redis.delete(f"etudiant:{telephone}")
        self.redis.delete("etudiants:all")
        return result is not None

    def modifier_etudiant(self, telephone, nouvelles_donnees):
        if "notes" in nouvelles_donnees:
            for note in nouvelles_donnees["notes"].values():
                if not (0 <= note <= 20):
                    return False

        result = self.mongo.update(
            self.collection_name,
            {"telephone": telephone},
            {"$set": nouvelles_donnees}
        )

        cache_keys = [f"etudiant:{telephone}", "etudiants:all"]
        if "classe" in nouvelles_donnees:
            cache_keys.append(f"classe:{nouvelles_donnees['classe']}:etudiants")

        for key in cache_keys:
            self.redis.delete(key)

        return result is not None

    def supprimer_etudiant(self, telephone):
        etudiant = self.rechercher_par_telephone(telephone)
        if not etudiant:
            return False

        result = self.mongo.delete(self.collection_name, {"telephone": telephone})

        cache_keys = [f"etudiant:{telephone}", "etudiants:all"]
        if etudiant.classe:
            cache_keys.append(f"classe:{etudiant.classe}:etudiants")

        for key in cache_keys:
            self.redis.delete(key)

        return result is not None

    def trier_par_moyenne(self, classe=None, limit=None):
        etudiants = self.rechercher_par_classe(classe) if classe else self.lister_tous()
        triés = sorted(
            [(e, e.calculer_moyenne()) for e in etudiants],
            key=lambda x: x[1], reverse=True
        )
        if limit:
            triés = triés[:limit]
        return [e for e, _ in triés]

    def calculer_moyenne_classe(self, classe):
        etudiants = self.rechercher_par_classe(classe)
        if not etudiants:
            return 0.0
        total = sum(e.calculer_moyenne() for e in etudiants)
        return round(total / len(etudiants), 2)
