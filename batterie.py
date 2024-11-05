from constants import OFF, ON, TEMPERATURE_MAX
from system_error import SystemError

class Batterie:
    # Classe qui gère la batterie et ses caractéristiques
    def __init__(self):
        # Initialisation des variables de la batterie
        self.state = OFF
        self.temperature = 33.0  # Température initiale fictive

        # Les valeurs d'exemple sont de -35 et 35.
        self.PMaxCh_kW = -35
        self.PMaxDisch_kW = 35

    def start(self):
        # Démarre la batterie si toutes les conditions sont OK
        try:
            if self.temperature > TEMPERATURE_MAX:
                raise SystemError(f"Température trop élevée: {self.temperature}°C")

            self.state = ON
            print("La batterie est démarrée avec succès")
            return True
        except Exception as e:
            print(f"Erreur lors du démarrage de la batterie: {str(e)}")
            return False

    def stop(self):
        # Arrête la batterie normalement
        try:
            self.state = OFF
            self.PMaxCh_kW = 0
            self.PMaxDisch_kW = 0
            print("La batterie est arrêtée normalement")
        except Exception as e:
            print(f"Erreur lors de l'arrêt de la batterie: {str(e)}")
            self.emergency_stop()

    def emergency_stop(self):
        # Arrêt d'urgence de la batterie
        self.state = OFF
        self.PMaxCh_kW = 0
        self.PMaxDisch_kW = 0
        print("ARRÊT D'URGENCE DE LA BATTERIE !")

    def get_state(self):
        # Renvoie l'état actuel de la batterie
        return self.state

    def get_PMaxCh_kW(self):
       # Renvoie la puissance maximale de charge
        return self.PMaxCh_kW

    def get_PMaxDisch_kW(self):
        # Renvoie la puissance maximale de décharge
        return self.PMaxDisch_kW

    def check_temperature(self):
        # Vérifie si la température est dans les limites acceptables
        if self.temperature > TEMPERATURE_MAX:
            raise SystemError(f"Température critique: {self.temperature}°C")