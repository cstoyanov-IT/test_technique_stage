from constants import OFF, ON
from system_error import SystemError
from batterie import Batterie
from onduleur import Onduleur

class StorageController:
    # Classe principale qui gère tout le système
    def __init__(self):
        self.batterie = Batterie()
        self.onduleur = Onduleur()
        self.command = OFF
        self.PSetpoint_kW = 0
        self.system_ok = True  # Indicateur d'état du système

    def process_ems_command(self, command, PSetpoint_kW):
        # Traite les commandes venant de l'EMS avec vérifications
        try:
            # Vérifie que le système est en bon état
            if not self.system_ok:
                raise SystemError("Système en état d'erreur")

            self.command = command
            self.PSetpoint_kW = PSetpoint_kW

            # Gestion du démarrage
            if command == ON and self.get_state() == OFF:
                if not self._start_sequence():
                    raise SystemError("Échec de la séquence de démarrage")

            # Gestion de l'arrêt
            elif command == OFF and self.get_state() == ON:
                self._stop_sequence()

            # Application de la puissance si le système est ON
            if self.get_state() == ON:
                if not self._apply_power_setpoint(PSetpoint_kW):
                    raise SystemError("Échec de l'application de la puissance")

        except Exception as e:
            print(f"Erreur système: {str(e)}")
            self.emergency_stop()
            return False
        return True

    def _start_sequence(self):
        # Séquence de démarrage sécurisée
        try:
            print("Démarrage du système...")

            # 1. Démarrage batterie
            if not self.batterie.start():
                return False

            # 2. Vérification batterie avant démarrage onduleur
            if self.batterie.get_state() == ON:
                if not self.onduleur.start():
                    return False
                return True
            return False

        except Exception as e:
            print(f"Erreur sequence démarrage: {str(e)}")
            self.emergency_stop()
            return False

    def _stop_sequence(self):
        # Séquence d'arrêt
        try:
            print("Arrêt du système...")
            self.onduleur.stop()
            if self.onduleur.get_state() == OFF:
                self.batterie.stop()
        except Exception as e:
            print(f"Erreur sequence arrêt: {str(e)}")
            self.emergency_stop()

    def emergency_stop(self):
        # Arrêt d'urgence du système complet
        if self.system_ok:
            print("LANCEMENT D'ARRÊT D'URGENCE DU SYSTÈME !")
            self.system_ok = False
            self.onduleur.emergency_stop()
            self.batterie.emergency_stop()
            self.command = OFF
            self.PSetpoint_kW = 0

    def _apply_power_setpoint(self, PSetpoint_kW):
        # Applique la consigne de puissance avec vérifications
        try:
            # Calcul des limites de puissance
            max_charge = max(
                -min(abs(self.batterie.PMaxCh_kW), self.onduleur.PMax_kW),
                -self.onduleur.PMax_kW,
            )

            max_discharge = min(
                self.batterie.PMaxDisch_kW, self.onduleur.PMax_kW
            )

            # Vérification des limites
            if not (max_charge <= PSetpoint_kW <= max_discharge):
                raise SystemError(
                    f"Puissance {PSetpoint_kW} hors limites [{max_charge}, {max_discharge}]"
                )

            # Application de la puissance limitée
            limited_power = max(min(PSetpoint_kW, max_discharge), max_charge)
            return self.onduleur.set_power_setpoint(limited_power)

        except Exception as e:
            print(f"Erreur application puissance: {str(e)}")
            return False

    def get_state(self):
        # État global du système
        if self.batterie.get_state() == ON and self.onduleur.get_state() == ON:
            return ON
        return OFF

    def get_PMaxCh_kW(self):
        # Puissance maximale de charge du système
        if self.get_state() == OFF:
            return 0
        return max(
            -min(abs(self.batterie.PMaxCh_kW), self.onduleur.PMax_kW),
            -self.onduleur.PMax_kW,
        )

    def get_PMaxDisch_kW(self):
        # Puissance maximale de décharge du système
        if self.get_state() == OFF:
            return 0
        return min(self.batterie.PMaxDisch_kW, self.onduleur.PMax_kW)

    def get_P_kW(self):
        # Puissance actuelle du système
        return self.onduleur.get_P_kW()

    def print_system_info(self):
        # Affiche les informations actuelles du système
        print(f"État du système: {self.get_state()}")
        print(f"Puissance actuelle: {self.get_P_kW()} kW")
        print(f"Température actuelle: {self.batterie.temperature}°C")
        print(f"Limite charge: {self.get_PMaxCh_kW()} kW")
        print(f"Limite décharge: {self.get_PMaxDisch_kW()} kW")
