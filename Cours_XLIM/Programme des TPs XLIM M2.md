# Liste des TPs 

### Durée : 9h
----------

# Pre requis
#### Connaissances nécéssaires à obtenir en amont des TPs
Fournir donc les indications sur ces connaissances
Voir les cours pour la partie théorique

#### Langages et outils: Python, numpy, scipy, Jupyter, Git

-------

# TP.1 : Simple Side Channel Analysis

### 1. Manipulation des traces (30 min)
- recuperer un ou des fichiers de traces
- apprendre à le(s) charger
- afficher les valeurs et identifier leur type
- afficher les traces avec matplotlib par exemple

Matériel: 
- fichier npy et npz: apprendre a utiliser python et numpy pour le manipuler 
- fichier des DPA contests: python

### 2. Reconnaissance d'algo, identifier les rondes et les operations dans l'AES (30 min)
- rester sur des traces en npy et npz: les mêmes que 1. = AES
- les afficher cf. 1.
- analyser les traces: faire un peu de signal processing
--- executer les cellules fournies
--- coder les fonctions
--- Mix des deux
Cette partie servira aussi pour retrouver le(s) exposant(s) dans la trace RSA SFM (RSA CRT) cf. partie 3

- Identifier dans la trace : les rondes, les compter, les operations dans une ronde
- Voyez vous qque chose de particulier dans la derniere ronde: pas de MixColumn

Benoit: regarder si il y a de meilleures traces pour cet exercice sur un AES.

### 3. Retrouver un exposant secret d'un RSA non CRT dans une seule trace (1h)

Input
- trace du RSA, modulus N
- un couple (plaintext, signature)
- L'algo d'exponentiation utilisé est un S&M left right ou right left
- RSA = exponentiation modulaire S&M 1024 bits

- combien de pattern identifiez vous?
- donc que peuvent etre ces patterns?
- ce ne sont pas des squares et des multiply mais des squares et des squares-et-multiply
- Retrouver les 4 exposants possibles: en python ou en numpy
- tester les 4 hypotheses et vérifier avec le couple plaintext/signature fournie quel est l'exposant secret?
- Conclure sur l'algorithme utilisé

Guider le raisonnement.
Expliquer pkoi un pic de S&M est plus long qu'un simple square: la durée du calcul inférieure dans le square et forcement plus courte que square + multiply  !!!!

### Optionnel long: Reproduire l'attaque 3. avec du clustering (1h)
- Traces d'un RSA S&M always
- L'attaque 3.1 ne permet plus de retrouver le secret: expliquer pkoi
- Par contre dans la trace la valeur du bit fuit mais de maniere non visible par des analyses classiques


### Optionnel court: donner un autre exemple avec un RSA CRT S&M ou on a un pattern pour le square et un pattern pour le multiply (15-30 min)

Generer une trace de RSA SFM our de RSA CRT avec un Square Plus rapide que le multiply
Utiliser Balthazar


Expliquer pkoi un pic de S&M est plus haut qu'un square: la durée du calcul inférieure dans le square !!!!
--> Ramener à la comprehension de l'implementation d'un square vs. un multiply pour expliquer des différence potentielles d'amplitude d'amplitude et de durée.
il peut y avoir plusieurs raisons.

### Optionnel court: SPA sur ECC Double and Add ? Trouver une courbe !

-------------------

# TP.2 Caracterisation des fuites potentielles et attaques

Objectifs: 

### A : sur jeu de traces AES-Set1
Traces synchronisé, clef et plaintext connu

Option 1: traces AES simulés
Option preferentielle 2: traces AES du ChipWhisperer
est ce que ces traces du ChipW sont facile a resynchroniser, presence de patterns ou pas?
Option 3: prendre d'autres d'AES type challenge CHES AES ou autres sur le net et avoir un set synchronisé et créer un set désynchronisé facile à resynchroniser avec des clefs différentes.

- Caracterisation des traces pour identifier la presence de fuites potentielle (30 min)
Utiliser et coder le t test de Welch
Analyser les resultats?
Etes vous capable de dire ce qui fuit?
Quelle ronde?
Quelle fonction?

Optionel (à vérifier qu'on peut avoir ce set de traces): Peut etre rajouter le t test sur un set de trace avec une seule fuite, type DPA contest V2 sur AES

- Faire du reverse ( à clef connu) pour identifier la cause la fuite (1h)
Choix du distinguisher: CPA en python/numpy
implementer la CPA
Implementer une fonction de selection: à définir suivant les traces qu'on a

- Réaliser des attaques et analyser le nombre de traces (1h)
Implémenter la CPA pour tous les guesses
La fonction de selection pour tous les guesses
Tester tous les guess et regarder le nombre de traces necessaires pour que l'attaque marche
(sauver les résultats)

- Optionnel 1 (15-30 min): 
rajouter la convergence

-------------------

# TP.3 : Side Channel et au delà: traiter les cas difficiles
sur jeu de traces AES-Set2
Objectif: Montrer l'importance de la synchronization des traces dans les attaques

Traces désynchronisés, clef inconnu et plaintext connu: retrouver la clef
L'attaque ne doit pas marcher.
Que faire? Pkoi ca marche plus alors que la source des traces est la meme.
Observer que les traces sont désynchronisés.

- Implémenter la resynchronisation des traces (1h)
Nous: Génerer le set de traces resynchronisé
Relancer l'attaque et retrouver la clef

**--> L'attaque permet de dechiffrer le lieu et la date de la prochaine reunions des SLT contre mes mega bassines en auvergne.**

- Le modele de fuite est en distance (30-45 min) 
Donner le set de traces DPA contest AES V2 
Faire les attaques HW dessus: pas de résultat
"Déduire" que le modele est pas bon 
Implémenter la fonction de selection DeltaLastRound
Relancer l'attaque et retrouver la clef

- La fuite est d'ordre supérieur ! (1h30)
Implémenter les fonctions de reverse pour SBox xor mask, pour mask
Implémenter l'attaque ordre 2 


Remarque: si traces ChipWhisperer pas ok pour resynchroniser, prendre un autre set de traces et l' avoir en synchronisé et en désychronisé

Appendix

- Utiliser les traces ASCAD ? 


Aparthé:
- cours Christophe: attaque (reverse) DPA pour chaque bit en distance de Hamming --> la polarité des pics de chaque attaque par bit donne la valeur bit par bit de la constante 


--------------
---------------

# Open points
- change the target frequency?
- could allow to capture more cycles
- can we insert a delay after the trig to capture later points?

# Plotting on traces
- look on power traces to see more variations are on the area where the variance has peaks

# MBEDTLS
- check the code to fit with vertical variance trace
- locate operations on the trace

# Ds le TP2 
- leur faire coder distinguisher et fct de selection pour l'attaque
- cf TP AES sur Balthazar

# Ds le DPA contest V2 tester leakage en 8, 16, 32, 64, 128 etc pour expliquer les niveaux de correlation partiels ou full
- ds certain cas la valeur de reference est une constante, la chercher peut etre utile pour améliorer ou faire marcher l'attaque !

exple: attaquer en CPA monobit peut donner en fct de la polarité les valeurs bit a bit de la constante de reference (utiliser Balthazar?)