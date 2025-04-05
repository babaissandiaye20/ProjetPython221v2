# view/ConsoleManager.py

import os
import time


class ConsoleManager:
    """
    Classe pour gérer l'affichage des consoles en fonction du rôle de l'utilisateur
    """

    @staticmethod
    def clear_screen():
        """Nettoie l'écran de la console"""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_header(title):
        """
        Affiche un en-tête formaté pour la console

        Args:
            title (str): Titre à afficher
        """
        ConsoleManager.clear_screen()
        print("=" * 60)
        print(f"{title:^60}")
        print("=" * 60)
        print()

    @staticmethod
    def print_menu(options):
        """
        Affiche un menu avec des options numérotées

        Args:
            options (list): Liste de tuples (numéro, description)
        """
        for num, description in options:
            print(f"{num}. {description}")
        print()

    @staticmethod
    def get_user_choice(min_value, max_value):
        """
        Récupère le choix de l'utilisateur et le valide

        Args:
            min_value (int): Valeur minimale acceptée
            max_value (int): Valeur maximale acceptée

        Returns:
            int: Choix de l'utilisateur
        """
        while True:
            try:
                choice = int(input("Votre choix: "))
                if min_value <= choice <= max_value:
                    return choice
                print(f"Veuillez entrer un nombre entre {min_value} et {max_value}.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")

    @staticmethod
    def print_message(message, success=True):
        """
        Affiche un message avec formatage

        Args:
            message (str): Message à afficher
            success (bool): True si c'est un message de succès, False sinon
        """
        prefix = "✅" if success else "❌"
        print(f"\n{prefix} {message}")
        time.sleep(1.5)  # Pause pour permettre la lecture