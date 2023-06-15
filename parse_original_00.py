"""
- split into actes
- split into scenes
- transform each verse from

    CHARACTER.
    the verse content
    over multiple lines.

to
    CHARACTER: the verse content over multiple lines.

"""

import json
import re
import pandas as pd


class Verse(object):
    def __init__(self, verse):
        self.verse = verse

    def transform(self):
        self.verse = self.remove_brackets()
        self.verse = self.character_name()
        self.verse = self.remove_lr_punctuation()
        self.verse = self.remove_lr_within()
        self.verse = self.remove_lr_questionmark()

        # # remove lr after punctuation signs
        # reg = r'([^\w\s])\s*\n'
        # str_ = re.sub(reg, r'\1 ', str_)
        # # str_ = re.sub(reg, '? ', str_)
        # # str_ = re.sub(reg, '' , str_)

    def remove_brackets(self):
        reg = r"\[\d+\]"
        return re.sub(reg, "", self.verse)

    def character_name(self):
        reg = r"([A-Z][A-Z]+)\.\n\n"
        return re.sub(reg, r"\1: ", self.verse)

    def remove_lr_within(self):
        # line returns within the verse
        reg = r"(\w+)\n(\w+)"
        return re.sub(reg, r"\1 \2", self.verse)

    def remove_lr_punctuation(self):
        # list the punctiation signs
        # reg = r'([^\n]*)(,|!)\s*\n([^\n]*)'
        reg = r"!\s*\n([^\n]*)"
        return re.sub(reg, r"! \1", self.verse)

    def remove_lr_questionmark(self):
        # remove lr after question mark
        # ? + space + lr + anything that's not a lr at least once
        # keeps word?\n\nword but replaces word?\nword with word? word
        reg = r"\?\s*\n([^\n]*)"
        return re.sub(reg, r"? \1", self.verse)


if __name__ == "__main__":
    if False:
        filename = "textes/medecin-malgre-lui.txt"
        output = "textes/medecin-malgre-lui_02.txt"
        # ´format original texte
        with open(filename, "r") as f:
            text = f.read()

        text = Verse(text)
        text.transform()

        with open(output, "w", encoding="utf-8") as f:
            f.write(text.verse)

    if True:
        filename = "textes/medecin-malgre-lui_02.txt"
        output = "textes/medecin-malgre-lui_02.json"

        with open(filename, "r") as f:
            text = f.read()

        # split along ACTE
        actes = re.split("== ACTE", text)[1:]

        scenes = []
        num_acte = 1
        for acte in actes:
            num_scene = 1
            # remove until 1st /n
            acte = acte.split("\n", 1)[1].strip()
            for scene in acte.split("-- SCÈNE")[1:]:
                scene = scene.split("\n", 1)[1].strip()
                scene = Verse(scene)
                scene.transform()
                scenes.append(
                    {"acte": num_acte, "scene": num_scene, "texte": scene.verse}
                )
                num_scene += 1

            num_acte += 1

        scenes = pd.DataFrame(scenes)

        with open(output, "w", encoding="utf-8") as f:
            scenes.to_json(f, force_ascii=False, orient="records", indent=4)
