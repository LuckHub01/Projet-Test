#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Connexion à la base de donnée
#import mysql.connector
import getpass
from sqlite3 import connect

# Fonction pour se connecter à la base de données
def connexion_bd():
    return connect("gestion_taches.db")
    
#    return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="gestion_taches"
#     )


# In[2]:


# Fonction pour vérifier les informations d'identification
def verifier_identifiants(username, password):
    conn = connexion_bd()
    cursor = conn.cursor()
    query = "SELECT * FROM utilisateur WHERE username = ? AND password = ?"
    cursor.execute(query, (username, password))
   
    utilisateur = cursor.fetchone()
    cursor.close()
    conn.close()
    return utilisateur


# In[3]:


def afficher_options_admin():
    print("Options disponibles :")
    print("1. Voir les tâches de l'équipe")
    print("2. Créer une tâche")
    print("3. Modifier une tâche")
    print("4. Supprimer une tâche")
    print("5. Notifier une tâche")
    print("6. Inscrire un utilisateur")
    print("7. Statistiques")
    print("0. Quitter l'application")
    
def afficher_options_super_admin():
    print("Options disponibles :")
    print("1. Voir les tâches: ")
    print("2. Créer une tâche")
    print("3. Modifier une tâche")
    print("4. Supprimer une tâche")
    print("5. Notifier une tâche")
    print("6. Inscrire un utilisateur")
    print("7. Statistiques")
    print("0. Quitter l'application")

def afficher_options_utilisateur():
    print("Options disponibles :")
    print("1. Voir mes tâches")
    print("2. Créer une tâche")
    print("3. Modifier une tâche")
    print("4. Notifier si une tâche est terminée")
    print("5. Statistiques")
    print("0. Quitter l'application")
    

def traiter_choix_admin(choix, administrateur):
    print(administrateur)
    
    if choix == "1":
        try:
            afficher_taches_equipe(administrateur)
        except Exception as e:
            print("Une erreur s'est produite lors de l'affichage des tâches de l'équipe :", e)
  
    elif choix == "2":
        creer_tache(administrateur)
    elif choix == "3":
        modifier_tache(administrateur)
    elif choix == "4":
        supprimer_tache(administrateur)
    elif choix=="5":
        notifier_tache(administrateur)
    elif choix == "6":
        inscrire_utilisateur(administrateur)
    elif choix=="7":
        statistiques(administrateur)
    elif choix == "0":
        print("Quit")
    else:
        print("Option invalide.")
        

def traiter_choix_super_admin(choix, administrateur):
    print(administrateur)
    
    if choix == "1":
        try:
            super_afficher_taches_equipe(administrateur)
        except Exception as e:
            print("Une erreur s'est produite lors de l'affichage des tâches de l'équipe :", e)
  
    elif choix == "2":
        super_creer_tache(administrateur)
    elif choix == "3":
        super_modifier_tache(administrateur)
    elif choix == "4":
        super_supprimer_tache(administrateur)
    elif choix=="5":
        super_notifier_tache(administrateur)
    elif choix == "6":
        super_inscrire_utilisateur(administrateur)
    elif choix=="7":
        super_statistiques(administrateur)
    elif choix == "0":
        print("Quit")
    else:
        print("Option invalide.")



# Exemple de fonctions pour chaque option à implémenter
def creer_tache(administrateur):
    
    conn = connexion_bd()
    cursor = conn.cursor()
# Demander les détails de la nouvelle tâche à l'utilisateur
    type_tache = input("Entrez le type de la nouvelle tâche : ")
    titre = input("Entrez le titre de la nouvelle tâche : ")
    description = input("Entrez la description de la nouvelle tâche : ")
    equipe =   administrateur[5]# Assurez-vous de valider l'équipe de quelque manière que ce soit
    createur=administrateur[1]
    
    print(createur)

    # Exécuter la requête SQL pour insérer la nouvelle tâche dans la base de données
    query = "INSERT INTO tache (type_tache, titre, description, equipe, createur) VALUES (?, ?, ?, ?,?)"
    values = (type_tache, titre, description, equipe, createur)
    cursor.execute(query, values)
    conn.commit()  # Valider la transaction

    print("La tâche a été créée avec succès !")
    
    
    
    



    


def traiter_choix_utilisateur(choix, utilisateur):
    if choix == "1":
        afficher_mes_taches(utilisateur)
    elif choix == "2":
        creer_ma_tache(utilisateur)
    elif choix == "3":
        modifier_ma_tache(utilisateur)
    elif choix == "4":
        notifier_ma_tache(utilisateur)
    elif choix=="5":
        mes_statistiques(utilisateur)
    elif choix == "0":
        print("Quit")
    else:
        print("Option invalide.")

def gestion_options(utilisateur):
    
    while True:
        if utilisateur[4] == 1:  # Vérifier si l'utilisateur est un administrateur
            afficher_options_admin()
            choix = input("Choisissez une option : ")
            traiter_choix_admin(choix, utilisateur)
            if choix == "0":
                quit=input("Voulez vous vraiment quitter? Y/N").lower()
                if quit=="y":
                    print("Au revoir !")
                    break
        elif utilisateur[4]==2:  # Utilisateur standard
            afficher_options_super_admin()
            choix = input("Choisissez une option : ")

            traiter_choix_super_admin(choix, utilisateur)
            if choix == "0":
                quit=input("Voulez vous vraiment quitter? Y/N").lower()
                if quit=="y":
                    print("Au revoir !")
                    break
            
        else:  # Utilisateur standard
            afficher_options_utilisateur()
            choix = input("Choisissez une option : ")

            traiter_choix_utilisateur(choix, utilisateur)
            if choix == "0":
                quit=input("Voulez vous vraiment quitter? Y/N").lower()
                if quit=="y":
                    print("Au revoir !")
                    break

# Fonction principale pour la connexion
def connexion():
    print("Connexion à l'application de gestion de tâches")
    username = input("Nom d'utilisateur : ")
    username="adminInfo"
    password = getpass.getpass("Mot de passe : ")  # Utilisation de getpass pour masquer le mot de passe
    password="admin"
    conn = connexion_bd()
    cursor = conn.cursor()

    utilisateur = verifier_identifiants(username, password)
    if utilisateur:
        print("Connexion réussie.")
        print("Bienvenue,", utilisateur[1]) 
        #gestion_options(utilisateur)
    else:
        print("Nom d'utilisateur ou mot de passe incorrect.")
        return None
    cursor.close()
    conn.close()
    


# In[4]:


def afficher_taches_equipe(administrateur):
    
    conn = connexion_bd()
    cursor = conn.cursor()
    

    # Récupérer l'équipe de l'administrateur
    equipe_admin = administrateur[5]  # Supposons que le champ d'équipe est à l'index 4
    
    print(administrateur)
    print(equipe_admin)

    # Sélectionner les tâches de l'équipe de l'administrateur
    query = "SELECT id, titre, description, type_tache, etat_fin FROM tache WHERE equipe = ?"
    cursor.execute(query, (equipe_admin,))
    taches_equipe = cursor.fetchall()
    #print(taches_equipe)

    # Afficher les titres des tâches de l'équipe
    if taches_equipe:
        print("Tâches de l'équipe :", equipe_admin)
        for tache in taches_equipe:
            id, titre, description, type_tache, etat_fin = tache
            print("Numero de la tache: ",id)
            print("Titre de la tâche : ", titre)
            print("Description de la tâche : ", description)
            print("Type de la tâche :", type_tache)
            if etat_fin==0:
                print("Tâche non terminée")
            else:
                print("Tâche terminée")
            
            print()
          # Supposons que le titre de la tâche est à l'index 0
    else:
        print("Aucune tâche trouvée pour l'équipe :", equipe_admin)

    cursor.close()
    conn.close()
    


# In[5]:


def modifier_tache(administrateur):
    conn = connexion_bd()
    cursor = conn.cursor()
    # Demander à l'utilisateur l'identifiant de la tâche à modifier
    tache_id = int(input("Entrez l'identifiant de la tâche à modifier : "))
    id_sql="SELECT id FROM tache WHERE equipe = ?"
    cursor.execute(id_sql, (administrateur[5],))
    id_mes_taches = cursor.fetchall()
    print(administrateur[5])

    # Extraire les identifiants des tâches dans une liste
    liste_id_taches = [tache[0] for tache in id_mes_taches]

    # Afficher la liste des identifiants des tâches de l'utilisateur
    print("Liste des identifiants des tâches de l'équipe :", liste_id_taches)
    if tache_id in liste_id_taches:
        # Sélectionner la tâche à partir de la base de données en fonction de son identifiant
        query = "SELECT * FROM tache WHERE id = ?"
        cursor.execute(query, (tache_id,))
        tache = cursor.fetchone()

        # Vérifier si la tâche existe
        if tache:
            # Afficher les détails de la tâche à modifier
            print("Ancienne valeur de la tâche :")
            print("Type :", tache[1])
            print("Titre :", tache[2])
            print("Description :", tache[3])
            print("Équipe :", tache[4])
            print("Createur :", tache[5])
            if tache[6]==0:
                print("Tâche non terminée")
            else:
                print("Tâche terminée")


            # Demander à l'utilisateur d'entrer les nouvelles valeurs pour les champs de la tâche
             # Demander à l'utilisateur d'entrer les nouvelles valeurs pour les champs de la tâche
            print("Entrez les nouvelles valeurs pour chaque champ (laissez vide pour conserver l'ancienne valeur) :")

            nouveau_titre = input("Entrez le nouveau titre de la tâche : ")  or tache[1]
            nouvelle_description = input("Entrez la nouvelle description de la tâche : ")  or tache[2]
            nouveau_type_tache = input("Entrez le nouveau type de la tâche : ")  or tache[3]
            #nouvelle_equipe = input("Entrez la nouvelle équipe de la tâche : ")
            nouvel_etat=int(input("Tache terminée? Entrez 0 pour non terminée et 1 pour terminée"))

            # Exécuter une requête SQL de mise à jour pour modifier les champs de la tâche
            query = "UPDATE tache SET titre = ?, description = ?, type_tache = ?, etat_fin =? WHERE id = ?"
            values = (nouveau_titre, nouvelle_description, nouveau_type_tache, nouvel_etat, tache_id)
            cursor.execute(query, values)
            conn.commit()  # Valider la transaction

            print("La tâche a été modifiée avec succès !")
        else:
            print("La tâche avec l'identifiant spécifié n'existe pas.")


    


# In[6]:


def supprimer_tache(administrateur):
    conn = connexion_bd()
    cursor = conn.cursor()
    # Demander à l'utilisateur l'identifiant de la tâche à supprimer
    
    
    id_sql="SELECT id FROM tache WHERE equipe = ?"
    cursor.execute(id_sql, (administrateur[5],))
    id_mes_taches = cursor.fetchall()
    #print("id_mes_taches: ", id_mes_taches)

    # Extraire les identifiants des tâches dans une liste
    liste_id_taches = [tache[0] for tache in id_mes_taches]

    # Afficher la liste des identifiants des tâches de l'utilisateur
    print("Liste des identifiants des tâches de l'equipe :", liste_id_taches)
    tache_id = int(input("Entrez l'identifiant de la tâche à supprimer : "))
    
    if tache_id in liste_id_taches:
        # Vérifier si la tâche existe
        query = "SELECT * FROM tache WHERE id = ?"
        cursor.execute(query, (tache_id,))
        tache = cursor.fetchone()

        if tache:
            # Confirmer la suppression avec l'utilisateur
            confirmation = input("Êtes-vous sûr de vouloir supprimer cette tâche ? (Oui/Non) : ").lower()
            if confirmation == "oui":
                # Exécuter la requête SQL de suppression de la tâche
                query = "DELETE FROM tache WHERE id = ?"
                cursor.execute(query, (tache_id,))
                conn.commit()  # Valider la transaction

                print("La tâche a été supprimée avec succès !")
            else:
                print("Suppression annulée.")
        else:
            print("La tâche avec l'identifiant spécifié n'existe pas.")
    else:
            print("La tâche avec l'identifiant spécifié n'existe pas.")
    


# In[7]:


def inscrire_utilisateur(administrateur):
    conn = connexion_bd()
    cursor = conn.cursor()
    # Demander à l'utilisateur les informations pour l'inscription
    username = input("Nom d'utilisateur : ")
    password = getpass.getpass("Mot de passe : ")
    email = input("Adresse email : ")
    type_compte = input("Type de compte (0 pour utilisateur standard, 1 pour administrateur) : ")
    equipe = administrateur[5]
    

    # Vérifier si l'utilisateur existe déjà dans la base de données
    query = "SELECT * FROM utilisateur WHERE username = ?"
    cursor.execute(query, (username,))
    utilisateur = cursor.fetchone()

    if utilisateur:
        print("Un utilisateur avec ce nom d'utilisateur existe déjà.")
    else:
        # Insérer le nouvel utilisateur dans la base de données
        query = "INSERT INTO utilisateur (username, password, email, type_compte, equipe) VALUES (?, ?, ?, ?, ?)"
        values = (username, password, email, type_compte, equipe)
        cursor.execute(query, values)
        conn.commit()  # Valider la transaction

        print("Nouvel utilisateur inscrit avec succès !")


# In[8]:


#Code utilisateur simple
def afficher_mes_taches(utilisateur):
    
    conn = connexion_bd()
    cursor = conn.cursor()
    

    # Récupérer l'équipe de l'administrateur
    username = utilisateur[1]  # Supposons que le champ d'équipe est à l'index 4
    


    # Sélectionner les tâches de l'équipe de l'administrateur
    query = "SELECT id, type_tache, titre, description, etat_fin FROM tache WHERE createur = ?"
    cursor.execute(query, (username,))
    mes_taches = cursor.fetchall()
    #print(taches_equipe)

    # Afficher les titres des tâches de l'équipe
    if mes_taches:
        print("Mes Tâches :")
        for tache in mes_taches:
            id, titre, description, type_tache, etat_fin = tache
            print("Numero de la tache: ",id)
            print("Titre de la tâche :", titre)
            print("Description de la tâche :", description)
            print("Type de la tâche :", type_tache)
            if etat_fin==0:
                print("Tâche non terminée")
            else:
                print("Tâche terminée")
            
            print()
          # Supposons que le titre de la tâche est à l'index 0
    else:
        print("Aucune tâche trouvée ")

    cursor.close()
    conn.close()
    


# In[9]:


def creer_ma_tache(utilisateur):
    
    conn = connexion_bd()
    cursor = conn.cursor()
# Demander les détails de la nouvelle tâche à l'utilisateur
    type_tache = input("Entrez le type de la nouvelle tâche : ")
    titre = input("Entrez le titre de la nouvelle tâche : ")
    description = input("Entrez la description de la nouvelle tâche : ")
    equipe =   utilisateur[5]# Assurez-vous de valider l'équipe de quelque manière que ce soit
    createur=utilisateur[1]
    
    print(createur)

    # Exécuter la requête SQL pour insérer la nouvelle tâche dans la base de données
    query = "INSERT INTO tache (type_tache, titre, description, equipe, createur) VALUES (?, ?, ?, ?,?)"
    values = (type_tache, titre, description, equipe, createur)
    cursor.execute(query, values)
    conn.commit()  # Valider la transaction

    print("Votre tâche a été créée avec succès !")


# In[10]:


def modifier_ma_tache(utilisateur):
    conn = connexion_bd()
    cursor = conn.cursor()
    # Demander à l'utilisateur l'identifiant de la tâche à modifier
    tache_id = int(input("Entrez l'identifiant de la tâche à modifier : "))
    
    id_sql="SELECT id FROM tache WHERE createur = ?"
    cursor.execute(id_sql, (utilisateur[1],))
    id_mes_taches = cursor.fetchall()
    #print("id_mes_taches: ", id_mes_taches)

    # Extraire les identifiants des tâches dans une liste
    liste_id_taches = [tache[0] for tache in id_mes_taches]

    # Afficher la liste des identifiants des tâches de l'utilisateur
    print("Liste des identifiants des tâches de l'utilisateur :", liste_id_taches)
    if tache_id in liste_id_taches:
         # Sélectionner la tâche à partir de la base de données en fonction de son identifiant
        query = "SELECT * FROM tache WHERE id = ?"
        cursor.execute(query, (tache_id,))
        tache = cursor.fetchone()

        # Vérifier si la tâche existe
        if tache:
            # Afficher les détails de la tâche à modifier
            print("Ancienne valeur de la tâche :")
            print("Type :", tache[1])
            print("Titre :", tache[2])
            print("Description de la tâche :", tache[3])
            print("Équipe :", tache[4])
            print("Createur :", tache[5])
            if tache[6]==0:
                print("Tâche non terminée")
            else:
                print("Tâche terminée")


            # Demander à l'utilisateur d'entrer les nouvelles valeurs pour les champs de la tâche
             # Demander à l'utilisateur d'entrer les nouvelles valeurs pour les champs de la tâche
            print("Entrez les nouvelles valeurs pour chaque champ (laissez vide pour conserver l'ancienne valeur) :")

            nouveau_titre = input("Entrez le nouveau titre de la tâche : ")  or tache[1]
            nouvelle_description = input("Entrez la nouvelle description de la tâche : ")  or tache[2]
            nouveau_type_tache = input("Entrez le nouveau type de la tâche : ")  or tache[3]
            #nouvelle_equipe = input("Entrez la nouvelle équipe de la tâche : ")
            nouvel_etat=int(input("Tache terminée? Entrez 0 pour non terminée et 1 pour terminée"))

            # Exécuter une requête SQL de mise à jour pour modifier les champs de la tâche
            query = "UPDATE tache SET titre = ?, description = ?, type_tache = ?, etat_fin =? WHERE id = ?"
            values = (nouveau_titre, nouvelle_description, nouveau_type_tache, nouvel_etat, tache_id)
            cursor.execute(query, values)
            conn.commit()  # Valider la transaction

            print("Votre tâche a été modifiée avec succès !")
        else:
            print("La tâche avec l'identifiant spécifié n'existe pas.")

    else:
        print("La tâche liée à cet identifiant n'existe pas")
        

   


# In[11]:


def notifier_ma_tache(utilisateur):
    conn = connexion_bd()
    cursor = conn.cursor()
    # Demander à l'utilisateur l'identifiant de la tâche à modifier
    tache_id = int(input("Entrez l'identifiant de la tâche à notifier : "))
    
    id_sql="SELECT id FROM tache WHERE createur = ?"
    cursor.execute(id_sql, (utilisateur[1],))
    id_mes_taches = cursor.fetchall()
    liste_id_taches = [tache[0] for tache in id_mes_taches]
   

    # Afficher la liste des identifiants des tâches de l'utilisateur
    print("Liste des identifiants des tâches de l'utilisateur :", liste_id_taches)
    if tache_id in liste_id_taches:
         # Sélectionner la tâche à partir de la base de données en fonction de son identifiant
        query = "SELECT * FROM tache WHERE id = ?"
        cursor.execute(query, (tache_id,))
        tache = cursor.fetchone()

        # Vérifier si la tâche existe
        if tache:
            # Afficher les détails de la tâche à modifier
            print("Ancienne valeur de la tâche :")
            print("Titre :", tache[1])
            print("Description :", tache[2])
            print("Type de tâche :", tache[3])
            print("Équipe :", tache[4])
            #print("Createur :", tache[5])
            if tache[6]==0:
                print("Tâche non terminée")
            else:
                print("Tâche terminée")


            # Demander à l'utilisateur d'entrer les nouvelles valeurs pour les champs de la tâche
             # Demander à l'utilisateur d'entrer les nouvelles valeurs pour les champs de la tâche
            print("Entrez les nouvelles valeurs pour chaque champ (laissez vide pour conserver l'ancienne valeur) :")


            nouvel_etat=int(input("Tache terminée? Entrez 0 pour non terminée et 1 pour terminée")) or tache[6]

            # Exécuter une requête SQL de mise à jour pour modifier les champs de la tâche
            query = "UPDATE tache SET  etat_fin =? WHERE id = ?"
            values = ( nouvel_etat, tache_id)
            cursor.execute(query, values)
            conn.commit()  # Valider la transaction

            print("Votre tâche a été notifiée avec succès !")
        else:
            print("La tâche avec l'identifiant spécifié n'existe pas.")


# In[12]:


def mes_statistiques(utilisateur):
    conn = connexion_bd()
    cursor = conn.cursor()
    # Demander à l'utilisateur l'identifiant de la tâche à modifier
    #tache_id = input("Entrez l'identifiant de la tâche à modifier : ")
    
    id_sql="SELECT id FROM tache WHERE createur = ?"
    cursor.execute(id_sql, (utilisateur[1],))
    id_mes_taches = cursor.fetchall()
    #print("id_mes_taches: ", id_mes_taches)

    # Extraire les identifiants des tâches dans une liste
    liste_id_taches = [tache[0] for tache in id_mes_taches]
    
    query="SELECT id FROM tache WHERE createur = ? AND etat_fin=?"
    cursor.execute(query, (utilisateur[1],1,))
    nb_taches_terminees = cursor.fetchall()
    liste_taches_terminees = [tache[0] for tache in nb_taches_terminees]
    nb_taches=len(liste_id_taches)
    nb_taches_terminees=len(liste_taches_terminees)

    # Afficher la liste des identifiants des tâches de l'utilisateur
    print("Nombre de tâches crées: ", nb_taches)
    print("Nombre de tâches terminées: ", nb_taches_terminees )
    print("Pourcentage de taches terminées: ", (nb_taches_terminees/nb_taches)*100, "%")
    
        

   


# In[13]:


def statistiques(administrateur):
    conn = connexion_bd()
    cursor = conn.cursor()
    # Demander à l'utilisateur l'identifiant de la tâche à modifier
    #tache_id = input("Entrez l'identifiant de la tâche à modifier : ")
    
    id_sql="SELECT id FROM tache WHERE equipe = ?"
    cursor.execute(id_sql, (administrateur[5],))
    id_mes_taches = cursor.fetchall()
    #print("id_mes_taches: ", id_mes_taches)

    # Extraire les identifiants des tâches dans une liste
    liste_id_taches = [tache[0] for tache in id_mes_taches]
    
    query="SELECT id FROM tache WHERE etat_fin=?"
    cursor.execute(query, (1,))
    nb_taches_terminees = cursor.fetchall()
    liste_taches_terminees = [tache[0] for tache in nb_taches_terminees]
    nb_taches=len(liste_id_taches)
    nb_taches_terminees=len(liste_taches_terminees)

    # Afficher la liste des identifiants des tâches de l'utilisateur
    print("Nombre de tâches crées: ", nb_taches)
    print("Nombre de tâches terminées: ", nb_taches_terminees) 
    print("Pourcentage de taches terminées: ", (nb_taches_terminees/nb_taches)*100, "%")
    
        

   


# In[14]:


def notifier_tache(administrateur):
    conn = connexion_bd()
    cursor = conn.cursor()
   
    id_sql="SELECT id FROM tache WHERE equipe = ?"
    cursor.execute(id_sql, (administrateur[5],))
    id_mes_taches = cursor.fetchall()
    liste_id_taches = [tache[0] for tache in id_mes_taches]

    # Afficher la liste des identifiants des tâches de l'utilisateur
    print("Liste des identifiants des tâches de l'équipe :", liste_id_taches)
     # Demander à l'utilisateur l'identifiant de la tâche à modifier
    tache_id = int(input("Entrez l'identifiant de la tâche à notifier : "))
    if tache_id in liste_id_taches:
         # Sélectionner la tâche à partir de la base de données en fonction de son identifiant
        query = "SELECT * FROM tache WHERE id = ?"
        cursor.execute(query, (tache_id,))
        tache = cursor.fetchone()

        # Vérifier si la tâche existe
        if tache:
            # Afficher les détails de la tâche à modifier
            print("Ancienne valeur de la tâche :")
            print("Titre :", tache[1])
            print("Description :", tache[2])
            print("Type de tâche :", tache[3])
            print("Équipe :", tache[4])
            #print("Createur :", tache[5])
            if tache[6]==0:
                print("Tâche non terminée")
            else:
                print("Tâche terminée")


            # Demander à l'utilisateur d'entrer les nouvelles valeurs pour les champs de la tâche
             # Demander à l'utilisateur d'entrer les nouvelles valeurs pour les champs de la tâche
            print("Entrez les nouvelles valeurs pour chaque champ (laissez vide pour conserver l'ancienne valeur) :")


            nouvel_etat=int(input("Tache terminée? Entrez 0 pour non terminée et 1 pour terminée")) or tache[6]

            # Exécuter une requête SQL de mise à jour pour modifier les champs de la tâche
            query = "UPDATE tache SET  etat_fin =? WHERE id = ?"
            values = ( nouvel_etat, tache_id)
            cursor.execute(query, values)
            conn.commit()  # Valider la transaction

            print("Votre tâche a été notifiée avec succès !")
        else:
            print("La tâche avec l'identifiant spécifié n'existe pas.")


# In[15]:


def super_creer_tache(administrateur):
    
    conn = connexion_bd()
    cursor = conn.cursor()
# Demander les détails de la nouvelle tâche à l'utilisateur
    type_tache = input("Entrez le type de la nouvelle tâche : ")
    titre = input("Entrez le titre de la nouvelle tâche : ")
    description = input("Entrez la description de la nouvelle tâche : ")
    equipe =   input("Entrez l'équipe  : ")# Assurez-vous de valider l'équipe de quelque manière que ce soit
    createur=administrateur[1]
    
    print(createur)

    # Exécuter la requête SQL pour insérer la nouvelle tâche dans la base de données
    query = "INSERT INTO tache (type_tache, titre, description, equipe, createur) VALUES (?, ?, ?, ?,?)"
    values = (type_tache, titre, description, equipe, createur)
    cursor.execute(query, values)
    conn.commit()  # Valider la transaction

    print("La tâche a été créée avec succès !")


# In[16]:


def super_afficher_taches_equipe(administrateur):
    
    conn = connexion_bd()
    cursor = conn.cursor()
    

    # Récupérer l'équipe de l'administrateur
    #equipe_admin = administrateur[5]  # Supposons que le champ d'équipe est à l'index 4
    
    print(administrateur)
    #print(equipe_admin)

    # Sélectionner les tâches de l'équipe de l'administrateur
    query = "SELECT id, type_tache, titre, description, equipe, etat_fin FROM tache "
    cursor.execute(query)
    taches_equipe = cursor.fetchall()
    #print(taches_equipe)

    # Afficher les titres des tâches de l'équipe
    if taches_equipe:
        #print("Tâches de l'équipe :", equipe_admin)
        for tache in taches_equipe:
            id, titre, description, type_tache, equipe, etat_fin = tache
            print("Numero de la tache: ",id)
            print("Titre de la tâche : ", titre)
            print("Description de la tâche : ", description)
            print("Type de la tâche :", type_tache)
            print("Equipe concernée :", equipe)
            if etat_fin==0:
                print("Tâche non terminée")
            else:
                print("Tâche terminée")
            
            print()
          # Supposons que le titre de la tâche est à l'index 0
    else:
        print("Aucune tâche trouvée")

    cursor.close()
    conn.close()
    


# In[17]:


def super_modifier_tache(administrateur):
    conn = connexion_bd()
    cursor = conn.cursor()
    # Demander à l'utilisateur l'identifiant de la tâche à modifier
    id_sql="SELECT id FROM tache"
    cursor.execute(id_sql)
    id_mes_taches = cursor.fetchall()
    #print(administrateur[5])

    # Extraire les identifiants des tâches dans une liste
    liste_id_taches = [tache[0] for tache in id_mes_taches]

    # Afficher la liste des identifiants des tâches de l'utilisateur
    print("Liste des identifiants des tâches :", liste_id_taches)
    tache_id = int(input("Entrez l'identifiant de la tâche à modifier : "))
    
    if tache_id in liste_id_taches:
        # Sélectionner la tâche à partir de la base de données en fonction de son identifiant
        query = "SELECT * FROM tache WHERE id = ?"
        cursor.execute(query, (tache_id,))
        tache = cursor.fetchone()

        # Vérifier si la tâche existe
        if tache:
            # Afficher les détails de la tâche à modifier
            print("Ancienne valeur de la tâche :")
            print("Titre :", tache[1])
            print("Description :", tache[2])
            print("Type de tâche :", tache[3])
            print("Équipe :", tache[4])
            print("Createur :", tache[5])
            if tache[6]==0:
                print("Tâche non terminée")
            else:
                print("Tâche terminée")


            # Demander à l'utilisateur d'entrer les nouvelles valeurs pour les champs de la tâche
             # Demander à l'utilisateur d'entrer les nouvelles valeurs pour les champs de la tâche
            print("Entrez les nouvelles valeurs pour chaque champ (laissez vide pour conserver l'ancienne valeur) :")

            nouveau_titre = input("Entrez le nouveau titre de la tâche : ")  or tache[1]
            nouvelle_description = input("Entrez la nouvelle description de la tâche : ")  or tache[2]
            nouveau_type_tache = input("Entrez le nouveau type de la tâche : ")  or tache[3]
            nouvelle_equipe = input("Entrez la nouvelle équipe de la tâche : ")
            nouvel_etat=int(input("Tache terminée? Entrez 0 pour non terminée et 1 pour terminée"))

            # Exécuter une requête SQL de mise à jour pour modifier les champs de la tâche
            query = "UPDATE tache SET titre = ?, description = ?, type_tache = ?, equipe=?, etat_fin =? WHERE id = ?"
            values = (nouveau_titre, nouvelle_description, nouveau_type_tache, nouvelle_equipe, nouvel_etat, tache_id)
            cursor.execute(query, values)
            conn.commit()  # Valider la transaction

            print("La tâche a été modifiée avec succès !")
        else:
            print("La tâche avec l'identifiant spécifié n'existe pas.")
            
    else:
            print("La tâche avec l'identifiant spécifié n'existe pas.")


    


# In[18]:


def super_supprimer_tache(administrateur):
    conn = connexion_bd()
    cursor = conn.cursor()
    # Demander à l'utilisateur l'identifiant de la tâche à supprimer
    
    
    id_sql="SELECT id FROM tache"
    cursor.execute(id_sql)
    id_mes_taches = cursor.fetchall()
    #print("id_mes_taches: ", id_mes_taches)

    # Extraire les identifiants des tâches dans une liste
    liste_id_taches = [tache[0] for tache in id_mes_taches]

    # Afficher la liste des identifiants des tâches de l'utilisateur
    print("Liste des identifiants des tâches de l'equipe :", liste_id_taches)
    tache_id = int(input("Entrez l'identifiant de la tâche à supprimer : "))
    
    if tache_id in liste_id_taches:
        # Vérifier si la tâche existe
        query = "SELECT * FROM tache WHERE id = ?"
        cursor.execute(query, (tache_id,))
        tache = cursor.fetchone()

        if tache:
            # Confirmer la suppression avec l'utilisateur
            confirmation = input("Êtes-vous sûr de vouloir supprimer cette tâche ? (Oui/Non) : ").lower()
            if confirmation == "oui":
                # Exécuter la requête SQL de suppression de la tâche
                query = "DELETE FROM tache WHERE id = ?"
                cursor.execute(query, (tache_id,))
                conn.commit()  # Valider la transaction

                print("La tâche a été supprimée avec succès !")
            else:
                print("Suppression annulée.")
        else:
            print("La tâche avec l'identifiant spécifié n'existe pas.")
    else:
            print("La tâche avec l'identifiant spécifié n'existe pas.")
    


# In[19]:


def super_inscrire_utilisateur(administrateur):
    conn = connexion_bd()
    cursor = conn.cursor()
    # Demander à l'utilisateur les informations pour l'inscription
    username = input("Nom d'utilisateur : ")
    password = getpass.getpass("Mot de passe : ")
    email = input("Adresse email : ")
    type_compte = input("Type de compte (0 pour utilisateur standard, 1 pour administrateur) : ")
    equipe = input("Nom de l'équipe: ")
    

    # Vérifier si l'utilisateur existe déjà dans la base de données
    query = "SELECT * FROM utilisateur WHERE username = ?"
    cursor.execute(query, (username,))
    utilisateur = cursor.fetchone()

    if utilisateur:
        print("Un utilisateur avec ce nom d'utilisateur existe déjà.")
    else:
        # Insérer le nouvel utilisateur dans la base de données
        query = "INSERT INTO utilisateur (username, password, email, type_compte, equipe) VALUES (?, ?, ?, ?, ?)"
        values = (username, password, email, type_compte, equipe)
        cursor.execute(query, values)
        conn.commit()  # Valider la transaction

        print("Nouvel utilisateur inscrit avec succès !")


# In[20]:


def super_notifier_tache(administrateur):
    conn = connexion_bd()
    cursor = conn.cursor()
    # Demander à l'utilisateur l'identifiant de la tâche à modifier
    
    id_sql="SELECT id FROM tache"
    cursor.execute(id_sql)
    id_mes_taches = cursor.fetchall()
    liste_id_taches = [tache[0] for tache in id_mes_taches]

    # Afficher la liste des identifiants des tâches de l'utilisateur
    print("Liste des identifiants des tâches de l'équipe :", liste_id_taches)
    tache_id = int(input("Entrez l'identifiant de la tâche à notifier : "))
    
    if tache_id in liste_id_taches:
         # Sélectionner la tâche à partir de la base de données en fonction de son identifiant
        query = "SELECT * FROM tache WHERE id = ?"
        cursor.execute(query, (tache_id,))
        tache = cursor.fetchone()

        # Vérifier si la tâche existe
        if tache:
            # Afficher les détails de la tâche à modifier
            print("Ancienne valeur de la tâche :")
            print("Titre :", tache[1])
            print("Description :", tache[2])
            print("Type de tâche :", tache[3])
            print("Équipe :", tache[4])
            #print("Createur :", tache[5])
            if tache[6]==0:
                print("Tâche non terminée")
            else:
                print("Tâche terminée")


            # Demander à l'utilisateur d'entrer les nouvelles valeurs pour les champs de la tâche
             # Demander à l'utilisateur d'entrer les nouvelles valeurs pour les champs de la tâche
            print("Entrez les nouvelles valeurs pour chaque champ (laissez vide pour conserver l'ancienne valeur) :")


            nouvel_etat=int(input("Tache terminée? Entrez 0 pour non terminée et 1 pour terminée")) or tache[6]

            # Exécuter une requête SQL de mise à jour pour modifier les champs de la tâche
            query = "UPDATE tache SET  etat_fin =? WHERE id = ?"
            values = ( nouvel_etat, tache_id)
            cursor.execute(query, values)
            conn.commit()  # Valider la transaction

            print("Votre tâche a été notifiée avec succès !")
        else:
            print("La tâche avec l'identifiant spécifié n'existe pas.")
    else:
            print("La tâche avec l'identifiant spécifié n'existe pas.")


# In[24]:


def super_statistiques(administrateur):
    conn = connexion_bd()
    cursor = conn.cursor()
    # Demander à l'utilisateur l'identifiant de la tâche à modifier
    #tache_id = input("Entrez l'identifiant de la tâche à modifier : ")
    
    id_sql="SELECT id FROM tache "
    cursor.execute(id_sql)
    id_mes_taches = cursor.fetchall()
    #print("id_mes_taches: ", id_mes_taches)

    # Extraire les identifiants des tâches dans une liste
    liste_id_taches = [tache[0] for tache in id_mes_taches]
    
    query="SELECT id FROM tache WHERE etat_fin=?"
    cursor.execute(query, (1,))
    nb_taches_terminees = cursor.fetchall()
    liste_taches_terminees = [tache[0] for tache in nb_taches_terminees]
    nb_taches=len(liste_id_taches)
    nb_taches_terminees=len(liste_taches_terminees)

    # Afficher la liste des identifiants des tâches de l'utilisateur
    print("Nombre de tâches crées: ", nb_taches)
    print("Nombre de tâches terminées: ", nb_taches_terminees) 
    print("Pourcentage de taches terminées: ", (nb_taches_terminees/nb_taches)*100, "%")
    
        

   


# In[ ]:


# Exemple d'utilisation
if __name__ == "__main__":
     connexion()
  


# In[ ]:





# In[ ]:




