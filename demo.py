from storage_controller import StorageController
from constants import ON, OFF

def demo_system():
    try:
        # Création du contrôleur
        controller = StorageController()

        # Test de démarrage
        print("\n--- Test de démarrage ---")

        # Use the initial power set in the Onduleur instance
        initial_power = controller.onduleur.get_P_kW()

        if controller.process_ems_command(ON, initial_power):
            # Le test de démarrage a réussi, proposant à l'utilisateur d'entrer en mode simulation
            controller.print_system_info()
            user_input = input(
                "Le système a démarré avec succès.\nVoulez-vous entrer en mode simulation afin d'essayer différentes valeurs avec des erreurs potentielles ? (oui/non/éteindre) "
            )
            if user_input.lower() == "oui":
                # Test de différentes puissances
                print(
                    "\n--- Test de différentes valeurs de puissances dans le but d'une démo et simulation d'erreurs ---"
                )
                test_powers = [
                    -3.0,
                    4.0,
                    -10.0,
                    60.0,
                ]  # Certaines valeurs provoqueront des erreurs
                for power in test_powers:
                    print(f"\nTest avec puissance: {power} kW")
                    controller.process_ems_command(ON, power)
                    print(f"État système: {controller.get_state()}")
                    print(f"Puissance actuelle: {controller.get_P_kW()} kW")
                    print(f"Limite charge: {controller.get_PMaxCh_kW()} kW")
                    print(f"Limite décharge: {controller.get_PMaxDisch_kW()} kW")
            elif user_input.lower() == "eteindre":
                controller._stop_sequence()
                print("Système arrêté normalement.")
            else:
                print("Simulation refusé par l'utilisateur.")
                controller._stop_sequence()
        else:
            print(
                "Échec du test de démarrage, le système n'est pas prêt pour la simulation."
            )

    except Exception as e:
        print(f"Erreur durant la démonstration: {str(e)}")
        controller.emergency_stop()
        print("Le système a été complètement arrêté en raison d'une erreur.")