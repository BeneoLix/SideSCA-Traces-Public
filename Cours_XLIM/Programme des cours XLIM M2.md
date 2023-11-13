# Cours sur l'Embarqué

### Durée totale: 9h

-----------
#  Cours 1 : An Introduction to Physical Security

Les slides actuels de cette presentation sont fait pour au moins 3h. Il y a au moins 68 slides.

### Modifications: 

##### Dans la partie 3 de la presentation , rajouter les differentes methodes d'exponentiation LtoR, RtoLeft, SMAlways etc .. necessaire à la fin du TP.1

##### enlever les sections sur la DFA et la DPA qui seront faites dans la seconde scéance de cours.

##### Garder dans le cours la partie SPA sur DES car ils feront l'AES et leur rappeller la structure de l'AES et les regles d'implementation sur l'AES: 
- la multiplication xtimes: comment la faire efficace: tables, decalage de 1 uniquement etc ...
- precalcul ou pas des sous clefs ou key schedule à la volée pour préserver la mémoire
- on peut se passer du shiftrow
- Implementations avec T tables

##### SPA sur RSA et l'exponentiation
- expliquer l'attaque de base
- Lister les autres attaques existantes sans les expliquer, donner les références: S&M always collision attacks

------------------------
#  Cours 2 : 

- reprendre DPA / CPA des slides actuels du cours #1

- Rajouter les explications sur le t-test

- Parler des différents distinguishers: DPA, CPA, 
à rajouter MIA (Christophe), NICV (Benoit), ANOVA (Benoit)

- Il faut que les étudiants comprennent que dans la vraie vie l'attaquant ne connait pas la clef: key ranking needed pour retrouver la clef.
- Rajouter les Templates

- Expliquer les techniques de masquage symétriques : exple sur AES (voire DES)

- Puis expliquer les  attaques second ordre

- Parler des contre-mesures d'ordre d pour resister aux attaques d'ordre supérieur d-1

- Une solution: techniques de masquage multiplicatif qui se prémunisent des attaques au zéro (zero value attacks)

- Attaques avec les moments d'ordre supérieurs: expliquer à quoi elles servent

- Lister les autres attaques existantes sans les expliquer, donner les références: collision attacks

------------------------
#  Cours 3 : 

Cours actuel sur la PK détaillé.

------------------------
#  Cours Benoit : 

Durée: 3h

- Reprendre les slides actuels
- Retirer le second order qui a été vu dans le cours 2
- Garder les attaques invasives et hardwares sur les composants.

Ajouts potentiels:
- Parler de machine learning supervised et un-supervised.
- Attaques à messages choisis pour attaquer en fin de ronde 1 de l'AES
- Attaques à messages choisis sur exponentiation ou scalar multiplication

- Il faudrait parler des attaques en faute de type SIFA mais bon plus tard.