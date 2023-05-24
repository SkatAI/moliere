'''
- split into actes
- split into scenes
- transform each verse from

    CHARACTER.
    the verse content
    over multiple lines.

to
    CHARACTER: the verse content over multiple lines.

'''

import json
import re
import pandas as pd

class Verse(object):
    def __init__(self, verse):
        self.verse = verse
        self.transformed = verse

    def transform(self):
        # initialize
        str_ = self.verse
        # removes line returns after character name beginneing of each verse
        reg = r'([A-Z][A-Z]+)\.\n\n'
        str_ = re.sub(reg, r'\1: ' , str_)
        # line returns with the verse
        reg = r'(\w+,*)\n(\w+)'
        str_ = re.sub(reg, r'\1 \2' , str_)

        # remove brackets
        reg = r'\[\d+\]'
        str_ = re.sub(reg, '' , str_)


        self.transformed = str_



if __name__ == "__main__":

    filename = 'medecin-malgre-lui.txt'

    with open(filename, 'r') as f:
        text = f.read()

    # split along ACTE
    actes = re.split("== ACTE", text)[1:]

    scenes = []
    num_acte = 1
    for acte in actes:
        num_scene = 1
        # remove until 1st /n
        acte = acte.split('\n', 1)[1].strip()
        for scene in acte.split('-- SCÈNE')[1:]:
            scene = scene.split('\n', 1)[1].strip()
            scene = re.sub('\n\n+', '\n', scene)
            scenes.append({
                'acte': num_acte,
                'scene': num_scene,
                'texte': scene
            })
            num_scene +=1

        num_acte +=1

    scenes = pd.DataFrame(scenes)
    out = filename.split('.')[0] + '.json'
    with open(out, 'w', encoding='utf-8') as f:
        scenes.to_json(f , force_ascii=False, orient = 'records')
