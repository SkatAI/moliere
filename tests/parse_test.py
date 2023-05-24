import pytest
import logging
import os

from parse import Verse

def test_remove_brackets():
    original = "first verse line[1]\nsecond verse line.[2]\n\n"
    expected = "first verse line\nsecond verse line.\n\n"

    vrs = Verse(original)
    transformed = vrs.remove_brackets()

    assert transformed == expected

def test_character_name():
    original = "CHARACTER.\n\nCAPS, first verse line\nsecond verse line.\n\n"
    expected = "CHARACTER: CAPS, first verse line\nsecond verse line.\n\n"

    vrs = Verse(original)
    transformed = vrs.character_name()

    assert transformed == expected

def test_remove_lr_within():
    original = "first verse line\nsecond verse line.\n\n"
    expected = "first verse line second verse line.\n\n"

    vrs = Verse(original)
    transformed = vrs.remove_lr_within()

    assert transformed == expected

def test_remove_lr_punctuation():
    original = "first verse line!\nsecond verse line.\n\n"
    expected = "first verse line! second verse line.\n\n"

    vrs = Verse(original)
    transformed = vrs.remove_lr_punctuation()

    assert transformed == expected

    original = "first verse line,\nsecond verse line.\n\n"
    expected = "first verse line, second verse line.\n\n"

    vrs = Verse(original)
    transformed = vrs.remove_lr_punctuation()

    assert transformed == expected

def test_remove_lr_questionmark():
    original = "first verse line?\nsecond verse line?\n\nhello"
    expected = "first verse line? second verse line?\n\nhello"

    vrs = Verse(original)
    transformed = vrs.remove_lr_questionmark()

    assert transformed == expected



def test_transform_real_verse():
    original = '''
SGANARELLE, MARTINE, paroissant sur le théâtre en se querellant.


SGANARELLE.

NON, je te dis que je n'en veux rien faire, et que c'est à moi de parler
et d'être le maître.

MARTINE.

Et je te dis, moi, que je veux que tu vives à ma fantaisie, et que je ne
me suis point mariée avec toi pour souffrir tes fredaines.

MARTINE.

Voyez un peu l'habile homme,
avec son benêt d'Aristote!

MARTINE.

C'est bien à toi vraiment à te plaindre de cette affaire!
Devrois-tu être un seul moment sans rendre grâce au Ciel de m'avoir pour ta femme?
et méritois-tu d'épouser une personne comme moi?
'''
    expected = '''
SGANARELLE, MARTINE, paroissant sur le théâtre en se querellant.


SGANARELLE: NON, je te dis que je n'en veux rien faire, et que c'est à moi de parler et d'être le maître.

MARTINE: Et je te dis, moi, que je veux que tu vives à ma fantaisie, et que je ne me suis point mariée avec toi pour souffrir tes fredaines.

MARTINE: Voyez un peu l'habile homme, avec son benêt d'Aristote!

MARTINE: C'est bien à toi vraiment à te plaindre de cette affaire! Devrois-tu être un seul moment sans rendre grâce au Ciel de m'avoir pour ta femme? et méritois-tu d'épouser une personne comme moi?
'''

    original = original.strip()
    expected = expected.strip()

    vrs = Verse(original)
    vrs.transform()

    assert vrs.verse == expected


def test_verses():

    original= '''
SGANARELLE.

Oui, habile homme. Trouve-moi un faiseur de fagots qui sache, comme moi,
raisonner des choses, qui ait servi six ans un fameux médecin, et qui
ait su dans son jeune âge son rudiment par coeur.

MARTINE.

Peste du fou fieffé!

SGANARELLE.

Peste de la carogne!
    '''

    expected  = '''
SGANARELLE: Oui, habile homme. Trouve-moi un faiseur de fagots qui sache, comme moi, raisonner des choses, qui ait servi six ans un fameux médecin, et qui ait su dans son jeune âge son rudiment par coeur.

MARTINE: Peste du fou fieffé!

SGANARELLE; Peste de la carogne!
'''
    original = original.strip()
    expected = expected.strip()

    vrs = Verse(original)
    vrs.transform()

    assert vrs.verse == expected
