# TODO

## PRIORITE

- tab name : actuellement 2 tabs ne DOIVENT pas avoir le même nom (quoique ça
a l'air de marcher quand même) et _open_tab du menu donne le même nom à tous

- fermer un onglet
- Renommer un onglet

- créer un port out virtuel

- Bouton 'back' dans rule form

- form validation

## PETITES REFACTO

...

## GROSSES REFACTO

- RULE FORM
- rendre l'affichage du midi learn performant en ne recréant pas les
widgets tout le temps
- mieux structurer le bordel. Le nom des clés d'un midi_msg ne doit changer
qu'une seule fois
- etc...

## DIVERS

- custom messagebox

- DONNÉES PERSISTANTES

- ECRIRE DES TESTS

- Shortcuts clavier

- choisir d'afficher ou non les MIDI IN & OUT

## PLUS TARD (RULES FEATURES)

- changer l'ordre des rules (glisser/déposer)
- CRUD sur rules

- pouvoir choisir les inputs de in_msg dans les inputs de out_msg

- TRIGGERS
- ajouter un "trigger" à une rule pour l'activer/désactiver
- donc état is_active d'une rule
- possible à un trigger d'envoyer des messages custom à n'importe quel port
