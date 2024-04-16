# MIDI Tweaker

## Présentation

Application en cours de développement.

MIDI Tweaker est un logiciel qui vise à permettre de modifier et router n'importe quel message MIDI de type channel voice (note, CC, program change...) en temps réel.

## Fonctionnalités prévues

Les fonctionnalités prévues sont (liste non exhaustive) :

- Changer le type d'un message pour un autre
- Modifier les valeurs d'un message (numéro CC, note, vélocité, valeur, pitchbend...)
- Ces valeurs peuvent être modifiées valeur par valeur (ex. 1 -> 10) ou par "fourchette" (range)
- La portée des fourchettes de valeurs modifiées s'adaptent à celle des messages entrant (ex. vélocité de 0 à 127 -> 50 à 100)
- Modifier et router les messages de n'importe quel port MIDI
- Router les messages vers n'importe quel port MIDI
- Créer un port MIDI sortant
- Ces "tables de modifications" s'appellent les "rules"
- Pas de limite de nombre de rules (si ce n'est la performance pour du temps réel)
- Créer des "triggers" pour déclencher l'activation d'une rule sur un message MIDI
- Un "trigger" peut aussi envoyer d'autres messages custom sur n'importe quel port
- ...

## Objectifs

Les possibilités de MIDI Tweaker seront vastes et variées.
Il pourra autant servir, par exemple, à régler finement le comportement d'un clavier MIDI selon ses besoins qu'à multiplier les possibilités natives d'un contrôleur.
Il sera disponible pour Linux et Windows.
