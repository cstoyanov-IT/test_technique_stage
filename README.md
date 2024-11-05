## Structure du Projet

Le projet est structuré en plusieurs fichiers pour une meilleure modularité et maintenabilité :

```
├── constants.py
├── system_error.py
├── batterie.py
├── onduleur.py
├── storage_controller.py
├── demo.py
└── main.py

### Description du Logiciel

Ce logiciel est un Storage Controller qui fait la jonction entre une batterie, un onduleur et l'EMS. Son rôle principal est de transmettre les consignes de l'EMS aux bons éléments (onduleur ou batterie) tout en s’assurant que les contraintes de ces derniers soient bien respectées.

### Fonctionnalités Principales

1. **Gestion de la Batterie**:
   - Démarrage et arrêt de la batterie.
   - Vérification de la température de la batterie.
   - Gestion des puissances maximales de charge et de décharge.

2. **Gestion de l'Onduleur**:
   - Démarrage et arrêt de l'onduleur.
   - Application des consignes de puissance.
   - Gestion des puissances maximales.

3. **Gestion des Commandes de l'EMS**:
   - Traitement des commandes de démarrage et d'arrêt.
   - Application des consignes de puissance en respectant les limites de la batterie et de l'onduleur.

4. **Gestion des Erreurs**:
   - Arrêt d'urgence en cas d'erreur critique.
   - Vérification des conditions de fonctionnement avant l'exécution des commandes.

### Comment Utiliser le Logiciel

1. **Initialisation**:
   - Le logiciel doit être exécuté dans un environnement Python.
   - Le fichier principal à exécuter est `main.py`

2. **Démarrage du Système**:
   - Le système démarre en vérifiant l'état de la batterie et de l'onduleur.
   - Si les conditions sont remplies, le système se met en marche et applique les consignes de puissance.

3. **Simulation de Puissances**:
   - Une fois le système démarré, l'utilisateur peut vérifier si le logiciel a bien pu démarrer avec les valeurs entré dans le fichier. 
   Il peut ensuite entrer en mode simulation pour tester différentes valeurs de puissance présente dans le fichier.
   - Certaines valeurs peuvent provoquer des erreurs intentionnellement pour démontrer la gestion des erreurs.

4. **Arrêt du Système**:
   - L'utilisateur peut choisir d'arrêter le système normalement ou en cas d'urgence.
   - L'arrêt d'urgence est déclenché en cas d'erreur critique.

### Exemple de Démarrage

Pour démarrer le logiciel, exécutez le fichier main.py dans le terminal.

```bash
python main.py
```

### Exemple de Sortie

Lors de l'exécution, le logiciel affichera des informations sur l'état du système, la puissance actuelle, la température de la batterie, et les limites de charge et de décharge. Voici un exemple de sortie:

```
--- Test de démarrage ---
La batterie est démarrée avec succès
L'onduleur est démarré avec succès
État du système: On
Puissance actuelle: 3.0 kW
Température actuelle: 33.0°C
Limite charge: -35 kW
Limite décharge: 35 kW
Le système a démarré avec succès.
Voulez-vous entrer en mode simulation afin d'essayer différentes valeurs avec des erreurs potentielles ? (oui/non/éteindre)
```

En cas de simulation, le logiciel testera différentes valeurs de puissance et affichera les résultats correspondants.

### Conclusion

Ce logiciel est conçu pour gérer efficacement les interactions entre une batterie, un onduleur et un EMS, tout en assurant la sécurité et la fiabilité du système.
```