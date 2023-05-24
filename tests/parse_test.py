import pytest
import logging
import os

from parse import Verse

def test_transform_verse():

    original = "CHARACTER.\n\nCAPS, first verse line\nsecond verse line.\n\n"
    # expected = "CHARACTER: CAPS, first verse line\nsecond verse line.\n\n"
    expected = "CHARACTER: CAPS, first verse line second verse line.\n\n"

    vrs = Verse(original)
    vrs.transform()

    assert vrs.transformed == expected

def test_transform_multiple_verse():
    original = '''CHARACTER.\n\nCAPS, first verse line\nsecond verse line.\n\nSECONDCHAR.\n\nsome new first verse line\nsecond verse line.\n\n'''
    expected = '''CHARACTER: CAPS, first verse line second verse line.\n\nSECONDCHAR: some new first verse line second verse line.\n\n'''

    vrs = Verse(original)
    vrs.transform()

    assert vrs.transformed == expected

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
avec son benêt d'Aristote![1]

MARTINE.

C'est bien à toi vraiment à te plaindre de cette affaire! Devrois-tu
être un seul moment sans rendre grâce au Ciel de m'avoir pour ta femme?
et méritois-tu d'épouser une personne comme moi?[3]
'''
    expected = '''
SGANARELLE, MARTINE, paroissant sur le théâtre en se querellant.


SGANARELLE: NON, je te dis que je n'en veux rien faire, et que c'est à moi de parler et d'être le maître.

MARTINE: Et je te dis, moi, que je veux que tu vives à ma fantaisie, et que je ne me suis point mariée avec toi pour souffrir tes fredaines.

MARTINE: Voyez un peu l'habile homme, avec son benêt d'Aristote!

MARTINE: C'est bien à toi vraiment à te plaindre de cette affaire! Devrois-tu être un seul moment sans rendre grâce au Ciel de m'avoir pour ta femme?
et méritois-tu d'épouser une personne comme moi?
'''

    original = original.strip()
    expected = expected.strip()

    vrs = Verse(original)
    vrs.transform()

    assert vrs.transformed == expected
