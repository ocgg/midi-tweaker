# TODO

## PRIORITE

- RANGES
- Prise en charge des ranges in/out !!!

- créer un port out virtuel

- supprimer une rule

- FRONT:
- note au user sur l'écriture des ranges
- infobox sur le form & autres
    - ranges sur le label d'attribut
    - textes soulignés/pointillés + curseur hover
- bouton refresh moche (mettre un label)
- ports list plus large, MIDI IN/OUT plus serré (50/50)
- largeur de ports list s'adapte au nom des ports ? on refresh ?
- scroll bar

## PETITES REFACTO

- Bouger les validations dans le modèle Rule
- Refacto les validations

## GROSSES REFACTO

...

## DIVERS

- custom messagebox
- custom ttk.Notebook
- custom infobox (tooltip)

- DONNÉES PERSISTANTES

- ECRIRE DES TESTS

- SHORTCUTS CLAVIER

- choisir d'afficher ou non les MIDI IN & OUT

- menu : Aide, A propos, etc...

- pouvoir choisir tous les ports d'entrée MIDI en même temps

## PLUS TARD (RULES FEATURES)

- GLISSER/DEPOSER les rules
- CRUD sur rules

- pouvoir choisir les inputs de in_msg dans les inputs de out_msg

## PLUS TARD: L'INCROYABLE FEATURE DES TRIGGERS

- ajouter un "trigger" à une rule pour l'activer/désactiver
- donc état is_active d'une rule
- possible à un trigger d'envoyer des messages custom à n'importe quel port
- possible à un trigger de trigger plusieurs rules
- montrer les rules actives

## PLUS TARD (TABS FEATURES)

- tab name : actuellement 2 tabs ne DOIVENT pas avoir le même nom (quoique ça
a l'air de marcher quand même) et _open_tab du menu donne le même nom à tous

- fermer un onglet
- Renommer un onglet
