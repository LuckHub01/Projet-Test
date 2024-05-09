import unittest
from unittest.mock import ANY, MagicMock, call, patch
from io import StringIO
import sys
import getpass
from Projet_Test import verifier_identifiants, connexion_bd, connexion, creer_tache, afficher_taches_equipe, modifier_tache, supprimer_tache, inscrire_utilisateur, notifier_tache

class TestConnexion(unittest.TestCase):
    
    # Test lorsque l'authentification réussit
    @patch('builtins.input', side_effect=['adminInfo', 'admin'])
    def test_admin_connexion_success(self, mock_input):
        with patch('getpass.getpass', return_value='admin'):
            captured_output = StringIO()
            sys.stdout = captured_output
            connexion()
            sys.stdout = sys.__stdout__
            output = captured_output.getvalue()
            
            self.assertIn("Connexion réussie.", output)
            self.assertIn("Bienvenue, admin", output)

    # Test lorsque l'authentification échoue
    # @patch('builtins.input', side_effect=['wronguser', 'wrongpassword'])
    # def test_admin_connexion_failure(self, mock_input):
    #     with patch('getpass.getpass', return_value='wrongpassword'):
    #         captured_output = StringIO()
    #         sys.stdout = captured_output
    #         connexion()
    #         sys.stdout = sys.__stdout__
    #         output = captured_output.getvalue()
            
    #         self.assertIn("Nom d'utilisateur ou mot de passe incorrect.", output)
    #         self.assertNotIn("Connexion réussie.", output)
    #         self.assertNotIn("Bienvenue,", output)

    # Test de la création d'une tâche
    @patch('builtins.input', side_effect=['test_type', 'test_title', 'test_description'])
    def test_creer_tache(self, mock_input):
        with patch('Projet_Test.connexion_bd') as mock_connexion_bd:
            mock_cursor = mock_connexion_bd.return_value.cursor.return_value
            mock_administrateur = (1, 'adminInfo', 'admin', 'admin@info.com', 1, 'Info')
            
            creer_tache(mock_administrateur)
            
            mock_cursor.execute.assert_called_once_with(
                ANY,  # La requête SQL peut être n'importe quelle chaîne
                ('test_type', 'test_title', 'test_description', 'Info', 'adminInfo')  # Les valeurs des arguments
            )



    @patch('sys.stdout', new_callable=StringIO)
    def test_afficher_taches_equipe(self, mock_stdout):
        # Créer un administrateur avec une équipe
        administrateur = (1, 'adminInfo', 'admin', 'admin@info.com', 1, 'Info')

        # Créer un mock pour le curseur et la connexion
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor

        # Définir le comportement attendu de la requête SQL et des résultats
        mock_cursor.fetchall.return_value = [
            (3, 'Nouveau Type', 'Nouveau Titre', 'Nouvelle Description', 1),
            (4, 'rapport', 'rapport test', 'rapport test', 0),
            (10, 'rapport', 'rapport', 'rapport', 0),
            (11, 'presentation lo', 'presentation', 'presentation loup', 1),
            (12, 'rapport', 'rapport', 'rapport', 1)
            
            
        ]

        # Appeler la fonction à tester
        afficher_taches_equipe(administrateur)

        # Capturer la sortie standard
        output = mock_stdout.getvalue()

        # Vérifier si les résultats sont correctement affichés
        self.assertIn("Tâches de l'équipe : Info", output)
        self.assertIn("Numero de la tache:  3", output)
        self.assertIn("Titre de la tâche :  Nouveau Titre", output)
        self.assertIn("Description de la tâche :  Nouvelle Description", output)
        self.assertIn("Type de la tâche : Nouveau Type", output)
        self.assertIn("Tâche terminée", output)
        self.assertIn("Numero de la tache:  4", output)
        self.assertIn("Titre de la tâche :  rapport", output)
        self.assertIn("Description de la tâche :  rapport test", output)
        self.assertIn("Type de la tâche : rapport", output)
        self.assertIn("Tâche non terminée", output)
        self.assertIn("Numero de la tache:  10", output)
        self.assertIn("Titre de la tâche :  rapport", output)
        self.assertIn("Description de la tâche :  rapport", output)
        self.assertIn("Type de la tâche : rapport", output)
        self.assertIn("Tâche non terminée", output)
        self.assertIn("Numero de la tache:  11", output)
        self.assertIn("Titre de la tâche :  presentation", output)
        self.assertIn("Description de la tâche :  presentation loup", output)
        self.assertIn("Type de la tâche : presentation lo", output)
        self.assertIn("Tâche terminée", output)
        self.assertIn("Numero de la tache:  12", output)
        self.assertIn("Titre de la tâche :  rapport", output)
        self.assertIn("Description de la tâche :  rapport", output)
        self.assertIn("Type de la tâche : rapport", output)
        self.assertIn("Tâche terminée", output)
        

        # Ajoutez d'autres tests pour d'autres fonctions si nécessaire
    
    
    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=["3", "Nouveau Titre", "Nouvelle Description", "Nouveau Type", "1"])
    def test_modifier_tache(self, mock_input, mock_stdout):
        # Créer un mock pour le curseur et la connexion
        mock_cursor = MagicMock()
        mock_conn = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        
        # Définir le comportement attendu de la requête SQL pour récupérer les identifiants des tâches de l'équipe
        mock_cursor.fetchall.return_value = [(3,), (4,), (10,), (11,), (12,)]
        
        # Définir le comportement attendu de la requête SQL pour récupérer les détails de la tâche
        mock_cursor.fetchone.return_value = ("Nouveau Type", "Nouveau Titre", "Nouvelle Description", "Info", "adminInfo", 1)
        
        # Appelez la fonction à tester
        modifier_tache(("1", "adminInfo", "admin", "admin@info.com", "1", "Info"))
        
        # Capture de la sortie standard
        output = mock_stdout.getvalue()
        
        # Vérification des sorties attendues
        self.assertIn("Ancienne valeur de la tâche :", output)
        self.assertIn("Type : Nouveau Type", output)
        self.assertIn("Titre : Nouveau Titre", output)
        self.assertIn("Description : Nouvelle Description", output)
        self.assertIn("Équipe : Info", output)
        self.assertIn("Createur : adminInfo", output)
        self.assertIn("Tâche terminée", output)
        self.assertIn("Entrez les nouvelles valeurs pour chaque champ", output)
        self.assertIn("La tâche a été modifiée avec succès !", output)
        
        # Vérification des appels à input pour chaque champ
        mock_input.assert_any_call("Entrez l'identifiant de la tâche à modifier : ")
        mock_input.assert_any_call("Entrez le nouveau titre de la tâche : ")
        mock_input.assert_any_call("Entrez la nouvelle description de la tâche : ")
        mock_input.assert_any_call("Entrez le nouveau type de la tâche : ")
        mock_input.assert_any_call("Tache terminée? Entrez 0 pour non terminée et 1 pour terminée")




#Je met sa en commentaire car sa supprime l'élement et sa se repercute sur les autres tests
    # @patch('builtins.input', side_effect=["15", "oui"])
    # @patch('sys.stdout', new_callable=StringIO)
    # def test_supprimer_tache(self, mock_stdout, mock_input):
    #     # Créer un mock pour le curseur et la connexion
    #     mock_cursor = MagicMock()
    #     mock_conn = MagicMock()
    #     mock_conn.cursor.return_value = mock_cursor
        
    #     # Définir le comportement attendu de la requête SQL pour récupérer les identifiants des tâches de l'équipe
    #     mock_cursor.fetchall.return_value = [ (15,),(16,)]
        
    #     # Capture de la sortie standard avant l'appel de la fonction à tester
    #     output_before = mock_stdout.getvalue()
        
    #     # Appelez la fonction à tester
    #     supprimer_tache(("1", "adminTelecom", "admin", "admin@telecom.com", "1", "Telecom"))
        
    #     # Capture de la sortie standard après l'appel de la fonction à tester
    #     output = mock_stdout.getvalue()
    
    #     # Vérification des sorties attendues
    #     self.assertIn("Liste des identifiants des tâches de l'equipe :", output)
    #     self.assertIn("La tâche a été supprimée avec succès !", output)
        
    #     # Vérification que la méthode execute n'a pas été appelée pour la suppression
    #     mock_cursor.execute.assert_not_called()
        
    #     # Vérification des appels à input pour chaque champ
    #     mock_input.assert_any_call("Entrez l'identifiant de la tâche à supprimer : ")
    #     mock_input.assert_any_call("Êtes-vous sûr de vouloir supprimer cette tâche ? (Oui/Non) : ")


#Inscription
    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=["user123", "password123", "user123@example.com", "0"])
    @patch('getpass.getpass', return_value="password123")
    def test_inscrire_utilisateur(self, mock_getpass, mock_input, mock_stdout):
        inscrire_utilisateur(("1", "adminTelecom", "admin", "admin@telecom.com", "1", "Telecom"))
        output = mock_stdout.getvalue()
        #self.assertIn("Un utilisateur avec ce nom d'utilisateur existe déjà", output)
        self.assertIn("Nouvel utilisateur inscrit avec succès !", output)
        
        
    # @patch('sys.stdout', new_callable=StringIO)
    # @patch('builtins.input', side_effect=[
    #     "user123",  # Simulation d'un utilisateur existant
    #     "password123",
    #     "user123@example.com",
    #     "0",
    #     "user123",  # Simulation d'un nouvel utilisateur
    #     "password123",
    #     "user123@example.com",
    #     "0"
    # ])
    # @patch('getpass.getpass', return_value="password123")
    # def test_inscrire_utilisateur(self, mock_getpass, mock_input, mock_stdout):
    #     # Préparer le mock de la base de données pour simuler un utilisateur existant
    #     mock_cursor = MagicMock()
    #     mock_conn = MagicMock()
    #     mock_conn.cursor.return_value = mock_cursor
    #     mock_cursor.fetchone.return_value = ("user123",)  # Simuler un utilisateur existant

    #     inscrire_utilisateur(("1", "adminTelecom", "admin", "admin@telecom.com", "1", "Telecom"))

    #     output = mock_stdout.getvalue()
    #     self.assertIn("Un utilisateur avec ce nom d'utilisateur existe déjà", output)

    #     # Réinitialiser le mock de la base de données
    #     mock_cursor.fetchone.return_value = None  # Simuler aucun utilisateur existant

    #     inscrire_utilisateur(("1", "adminTelecom", "admin", "admin@telecom.com", "1", "Telecom"))

    #     output = mock_stdout.getvalue()
    #     self.assertIn("Nouvel utilisateur inscrit avec succès !", output)

#Notification

    @patch('sys.stdout', new_callable=StringIO)
    @patch('builtins.input', side_effect=["16", "0"])
    def test_notifier_tache(self, mock_input, mock_stdout):
        notifier_tache(("16", "adminTelecom", "admin", "admin@telecom.com", "1", "Telecom"))
        output = mock_stdout.getvalue()
        self.assertIn("Votre tâche a été notifiée avec succès !", output)
        self.assertIn("Ancienne valeur de la tâche :", output)
        self.assertIn("Tâche terminée", output)




if __name__ == '__main__':
    unittest.main()
