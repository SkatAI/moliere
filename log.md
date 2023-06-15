### take 3
problem: chnk 2: losing 2 lines towards the end:
=> reduce chunk from
    {'acte': 1, 'scene': 1, 'verse_id_start':  14, 'verse_id_end': 30},
to
    {'acte': 1, 'scene': 1, 'verse_id_start':  14, 'verse_id_end': 24},
    {'acte': 1, 'scene': 1, 'verse_id_start':  24, 'verse_id_end': 30},
au niveau de "la famille"

*prompt*
Le texte suivant est extrait de la pièce de théatre 'Le Médecin Malgré Lui' de Molière.
Réecris ce texte en français, utilise un vocabulaire simple et moderne, garde chaque ligne du dialogue

_result_

=> le # de lignes est conservé
nouvelle traduction de
```
donne leur le fouet``` => ```Donne-leur une fessée.
```

mais
```
MARTINE: J'ai quatre pauvres petits enfants sur les bras.
SGANARELLE: Mets-les à terre.
```
devient

```
MARTINE: J'ai quatre petits enfants qui dépendent de moi.
SGANARELLE: Laisse-les jouer par terre.
```

scene 2 au debut. perte de ligne
```
MARTINE: De quoi vous mêlez-vous?

M. ROBERT: J'ai tort.

MARTINE: Est-ce là votre affaire?

M. ROBERT: Vous avez raison.
```

devient
```
MARTINE: Qu'est-ce que ça peut vous faire?

M. ROBERT: Vous avez raison, ce n'est pas mon affaire.
```

### take 2
problem: chnk 1: losing 2 lines towards the end:
    tokens: 257 verses:  13
    tokens: 169 verses:  11
add" "garde chaque ligne du dialogue"

*prompt*
Le texte suivant est extrait de la pièce de théatre 'Le Médecin Malgré Lui' de Molière.
Réecris ce texte en français, utilise un vocabulaire simple et moderne, garde chaque ligne du dialogue

_result_
- conservation du # de lignes dans le chunk 1

- contre sens
```
    MARTINE: Qu'appelles-tu bien heureuse de te trouver?
```

```
    MARTINE: Pourquoi es-tu si heureux de te trouver ici?
```


- mais pas dans le chunk 2, qui est plus long. il aggrege les 2 vers

```
    MARTINE: J'ai quatre pauvres petits enfants sur les bras.

    SGANARELLE: Mets-les à terre.

    MARTINE: Qui me demandent à toute heure du pain.
```
```
    MARTINE: J'ai quatre petits enfants qui ont faim tout le temps.
```


-----
#
# pas mal mais trop proche parfois du texte original.
if False:
    prompt =  f'''Le texte suivant est extrait de la pièce de théatre 'Le Médecin Malgré Lui' de Molière.
    Réecris ce texte en français, utilise un vocabulaire simple et moderne de niveau lycée.

    Le texte à réécrire est: \n{text}'''

if False:
    prompt =  f'''Le texte suivant est extrait de la pièce de théatre 'Le Médecin Malgré Lui' de Molière.
    Simplifie ce texte en français moderne, utilise un vocabulaire simple de niveau CM2.

    Le texte à réécrire est: \n{text}'''

# pas mal: potiion magique, mais supprime des echanges (20 -> 14)
if False:
    prompt =  f'''Le texte suivant est extrait de la pièce de théatre 'Le Médecin Malgré Lui' de Molière.
    Écrit ce texte en français moderne, simplifie les phrases, utilise un vocabulaire simple, garde tout les détails.

    Le texte à réécrire est: \n{text}'''


if False:
    prompt =  f'''Le texte suivant est extrait de la pièce de théatre 'Le Médecin Malgré Lui' de Molière.
    Voici tes instructions:
    - écrit ce texte en français moderne,
    - utilise un vocabulaire simple,
    Il faut conserver
    - le dialogue entre les personnages
    - les détails

    Le texte à réécrire est: \n{text}'''

if False:
    prompt =  f'''Le texte suivant est extrait de la pièce de théatre 'Le Médecin Malgré Lui' de Molière.
    Réécrit ce texte en français moderne: niveau de langue facile, vocabulaire simple
    Le texte à réécrire est: \n{text}'''

# good  one: remede miracle,
if False:
    prompt =  f'''Le texte suivant est extrait de la pièce de théatre 'Le Médecin Malgré Lui' de Molière.
    Voici tes instructions:
    - écrit ce texte en français moderne,
    - simplifie les phrases,
    - utilise un vocabulaire simple,

    Le texte à réécrire est: \n{text}'''

# good  one: remede miracle,
# Il s'agit d'un dialogue entre MARTINE, VALÈRE et LUCAS.
if False:
    prompt =  f'''Le texte suivant est extrait de la pièce de théatre 'Le Médecin Malgré Lui' de Molière.
    Il s'agit d'un dialogue entre M. ROBERT et MARTINE.

    Voici tes instructions:
    - Réécrit ce texte en français moderne,
    - simplifie les phrases,
    - utilise un vocabulaire simple,
    - conserve la structure du dialogue

    Le texte à réécrire est: \n{text}'''
