from constants import OFF, ON, POWER_LIMIT_MIN, POWER_LIMIT_MAX
from system_error import SystemError

class Onduleur:
    # Classe qui gère l'onduleur et la conversion de puissance
    def __init__(self):
        self.state = OFF
        self.PMax_kW = 35.0  # Puissance maximale
        self.P_kW = 3.0  # Défini la valeur initiale de 3.0 Kw

    def start(self):
        # Démarre l'onduleur si les conditions sont OK
        try:
            self.state = ON
            print("L'onduleur est démarré avec succès")
            return True
        except Exception as e:
            print(f"Erreur lors du démarrage de l'onduleur: {str(e)}")
            return False

    def stop(self):
        # Arrête l'onduleur normalement ou appelle l'état d'urgence en cas de bug d'arrêt
        try:
            self.state = OFF
            self.P_kW = 0
            print("L'onduleur est arrêté normalement")
        except Exception as e:
            print(f"Erreur lors de l'arrêt de l'onduleur: {str(e)}")
            self.emergency_stop()

    def emergency_stop(self):
        # Arrêt d'urgence de l'onduleur
        self.state = OFF
        self.P_kW = 0
        print("ARRÊT D'URGENCE DE L'ONDULEUR !")

    def set_power_setpoint(self, power):
        # Définit la puissance demandée avec vérifications de sécurité
        try:
            # Vérifie que la puissance demandée est dans les limites absolues fixées par le système.
            if not POWER_LIMIT_MIN <= power <= POWER_LIMIT_MAX:
                raise SystemError(f"Puissance demandée ({power} kW) hors limites")

            # Vérifie que la puissance ne dépasse pas la capacité de l'onduleur
            if abs(power) <= self.PMax_kW:
                self.P_kW = power
            else:
                raise SystemError(f"Puissance demandée trop élevée: {power} kW")

        except Exception as e:
            print(f"Erreur lors du réglage de la puissance: {str(e)}")
            return False
        return True

    def get_state(self):
        # Renvoie l'état actuel de l'onduleur
        return self.state

    def get_PMax_kW(self):
        # Renvoie la puissance maximale de l'onduleur
        return self.PMax_kW

    def get_P_kW(self):
        # Renvoie la puissance actuelle fournie
        return self.P_kW