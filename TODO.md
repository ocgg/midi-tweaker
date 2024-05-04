# TODO

## PRIORITE

- A TESTER: port choice ALL

- créer un port out virtuel

- RANGES: si range out et rien en in, range_in = rangetstar-rangestop

- REECRIRE Rules list plus performant

- FRONT:
- note au user sur l'écriture des ranges
- infobox sur le form & autres
    - ranges sur le label d'attribut
    - textes soulignés/pointillés + curseur hover
- ports list plus large, MIDI IN/OUT plus serré (50/50)
- largeur de ports list s'adapte au nom des ports ? on refresh ?
- scroll bar
- Ne pas afficher control/note, juste CC 10 ou NOTEON 23

## SECONDAIRE

- File/Reset
- Edit rule

## PETITES REFACTO

- Bouger les validations dans le modèle Rule
- Refacto les validations

## GROSSES REFACTO

- VALIDATIONS:
    - D'abord convertir les valeurs (controller)
    - Ensuite valider le bordel (model)

- rules_list_view pour implémenter le module constants -> partie "update list"
- l'implémenter dans les autres vues concernées

## DIVERS

- custom messagebox
- custom ttk.Notebook
- custom infobox (tooltip)

- DONNÉES PERSISTANTES

- ECRIRE DES TESTS

- SHORTCUTS CLAVIER

- menu : Aide, A propos, etc...

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

- traduction FR

- tab name : actuellement 2 tabs ne DOIVENT pas avoir le même nom (quoique ça
a l'air de marcher quand même) et \_open_tab du menu donne le même nom à tous

- fermer un onglet (custom ttk.Notebook)
- Renommer un onglet

## COULD HAVE

- choisir d'afficher ou non les MIDI IN & OUT
