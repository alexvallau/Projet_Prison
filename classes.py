# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 14:48:03 2023

@author: user
"""
import sqlite3

def connect_database(database_path):
    return sqlite3.connect(database_path)




###############################################################
class Prison:
    
     def getAllPrisons():
        conn =connect_database('goodDB.db')
        cursor = conn.cursor()
        prisons=cursor.execute("SELECT * FROM prison").fetchall()
        return prisons
    
     def getIdFromPrisonName(prison_name):
        conn=connect_database('goodDB.db')
        cursor = conn.cursor()
        query = "SELECT id FROM prison WHERE name_prison = ?"
        cursor.execute(query, (prison_name,))
        result = cursor.fetchone()
        return result

    
     def __init__(self, name_prison, oblast, number_of_prisoners, capacity_prison, prison_type):
        self.name_prison = name_prison
        self.oblast = oblast
        self.number_of_prisoners = number_of_prisoners
        self.capacity_prison = capacity_prison
        self.prison_type = prison_type

###############################################################

class Personne:
    def __init__(self, Prenom, Nom, birthday):
        self.Prenom = Prenom
        self.Nom = Nom
        self.birthday = birthday

class Employe(Personne):
    def __init__(self, Prenom, Nom, birthday, status):
        super().__init__(Prenom, Nom, birthday)
        self.status = status

class Prisonnier(Personne):
    def __init__(self, Prenom, Nom, birthday, type_de_peine, collaborateur, prison_id, image):
        super().__init__(Prenom, Nom, birthday)
        self.type_de_peine = type_de_peine
        self.collaborateur = collaborateur
        self.prison_id = prison_id
        self.image=image

    def getPrisonner(id):
        conn=connect_database('goodDB.db')
        cursor = conn.cursor()
        query = "SELECT * FROM prisonners WHERE id = ?"
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        prisonnier=Prisonnier(result[1], result[2], result[3], result[3], result[4], result[5], result[7])
        conn.close()
        return prisonnier


    
    def getAllPrisonners():
        conn = connect_database('goodDB.db')
        cursor = conn.cursor()
        # Modifiez la requête pour inclure le nom de la prison en utilisant une jointure
        query = """
        SELECT prisonners.id, prisonners.prenom, prisonners.nom, prisonners.type_de_peine,
               prisonners.collaborateur, prison.name_prison
        FROM prisonners
        JOIN prison ON prisonners.prison_id = prison.id
        """
        prisonners = cursor.execute(query).fetchall()
        conn.close()  # N'oubliez pas de fermer la connexion après utilisation
        return prisonners
    
    ##Renvoi les prisonniers qui correspondent à une certaine prison
    def getPrisonnersFilteredByPrison(prisonName):
        prisonId=Prison.getIdFromPrisonName(prisonName)
        conn=connect_database('goodDB.db')
        cursor = conn.cursor()
        query = "SELECT * from prisonners WHERE prison_id = ?"
        cursor.execute(query,(prisonId))
        result = cursor.fetchall()
        conn.close()
        return result
        
    
        
    def ajoute_prisonnier(self):
        try:
            conn =connect_database('goodDB.db')
            cursor = conn.cursor()
            # Insérer le prisonnier dans la table prisonners
            cursor.execute("""
                INSERT INTO prisonners (prenom, nom, type_de_peine, collaborateur, prison_id, image)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (self.Prenom, self.Nom,self.type_de_peine, self.collaborateur,self.prison_id, self.image))
            conn.commit()
        finally:
            # Fermer la connexion dans tous les cas (même en cas d'exception)
            conn.close()

###############################################################

class Peine:
    def __init__(self, user_id, type_de_peine,  entry_date, out_door):
     
        self.user_id = user_id
        self.type_de_peine = type_de_peine
        self.entry_date = entry_date
        self.out_door = out_door



    def getPeineFromUserID(prsionnerId):
        
     
        conn=connect_database('goodDB.db')
        cursor = conn.cursor()
        query = "SELECT * from peine WHERE user_id = ?"
        cursor.execute(query,(prsionnerId))
        result = cursor.fetchone()
        peine=Peine(result[1], result[2], result[4], result[5])
        
        conn.close()

        
        return peine





###############################################################