# MIDI Tweaker

- Choisir un port MIDI parmi tous ceux disponibles

- Voir les messages entrants en temps réel (canal/type/valeur, SysHex/non pris en charge)

- Créer une ou plusieurs "table de modification":

    - Choisir FILTRE: quels messages entrants modifier (par canal, type et/ou valeur)
        - MUST: Par canal: choisir un canal
        - MUST: Par type: NOTE (noteon & noteoff), NOTEON, NOTEOFF ou CC
        - COULD: Par valeur: choisir valeur, min (< à), max (> à) ou range

    - Choisir quelles modifications appliquer pour le message de sortie:
        - MUST: Changer canal — choisir canal de sortie
        - MUST: Changer valeur de sortie:
            - Valeur fixe
            - Range (min/max) — calculer la range proportionnelle
            - Différence (+/-) (ex. potard 'SEL') — choisir la valeur de + et -
            - Offset — additionner ou soustraire une valeur
        - COULD: Changer type — choisir type de sortie (différencier NOTEOFF, NOTEON et NOTE tout court)

- Donner un nom à la table de modification

- Choisir le port de sortie du message modifié

- Sauvegarder ses tables (DB ou fichiers ?)
    - avantage des fichiers : partageable

- Charger des réglages