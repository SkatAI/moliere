"""
Medecin malgre lui
== ACTE
\n\n
-- SCENE {numscene}
\n
Character list
\n\n
    {character} {comment}
    {comment}
    \n
        {verse}
        {verse}
"""

import json
import re
import pandas as pd
import numpy as np

class Play():
    acte_count = 0
    scene_count = 0
    verse_count = 0
    subverse_count = 0
    character_pattern = r"\- (Anselme|Brindavoine|Cléante|Dame Claude|Élise|Frosine|Harpagon|La Flèche|La Merluche|Maître Jacques|Maître Simon|Mariane|Valère|Le commissaire) \-"
    action_pattern = r"-action- \("

    def __init__(self):
        self.input_filename = "../textes/original/l-avare.txt"
        self.output_filename = "../textes/original/l-avare.json"
        self.load()
        self.items = []

    def load(self):
        self.lines = []
        with open(self.input_filename, "r") as file:
            for line in file:
                self.lines.append(line)
        self.line_count = len(self.lines)

    def add(self,line):
        if line.category in ['acte','character_list']:
            ps.items.append(line.to_dict(
                **{
                    'verse': 0
                }
            ))
        elif line.category == 'scene':
            ps.items.append(line.to_dict(
                **{
                    'text': line.text.split('-')[0].strip(),
                    'verse': 0
                }
            ))
            ps.items.append(line.to_dict(
                **{
                    'text': line.text.split('-')[1].strip(),
                    'category': 'character_list',
                    'verse': 0
                }
            ))

        else:
            ps.items.append(line.to_dict())

    def concat_verse(self):
        par = self.items.copy()

        par['paragraph'] = par.groupby(
            by = ['category', 'acte', 'scene', 'verse', 'subverse']
        )['text'].transform(lambda x: ' '.join(x))


        par.drop_duplicates(subset = ['category', 'acte', 'scene', 'verse', 'subverse', 'paragraph'],inplace = True)
        par['text'] = par.paragraph
        self.items = par[['category', 'acte', 'scene', 'verse', 'subverse', 'pos', 'text']].copy()
        self.items.reset_index(inplace = True, drop = True)

    def save(self):
        with open(self.output_filename, "w", encoding="utf-8") as f:
            self.items.to_json(f, force_ascii=False, orient="records", indent=4)



class Line(Play):

    def __init__(self,n,text):

        self.pos = n
        self.text = text.strip()
        self.text = re.sub(r"\(\d+\)", "", self.text)
        self.category = None
        self.get_category()

    def fix_space_punctuation(self):
        self.text = self.text.replace(" ,",",")
        self.text = self.text.replace(" .",",")


    def inc_acte(self):
        Play.acte_count +=1
        Play.scene_count =0

    def inc_scene(self):
        Play.scene_count +=1

    def inc_verse(self):
        Play.verse_count +=1

    def inc_subverse(self):
        Play.subverse_count +=1

    def reset_subverse(self, val = 0):
        Play.subverse_count = 0

    def get_category(self):

        if "ACTE " in self.text:
            self.category = 'acte'
            self.inc_acte()

        elif "Scène " in self.text:
            self.category = 'scene'
            self.inc_scene()
            self.reset_subverse()

        elif re.match(Play.character_pattern, self.text):
            self.category = 'character'
            self.inc_verse()
            self.reset_subverse()
            self.text = self.text.replace('-','').strip()

        elif re.search(Play.action_pattern, self.text):
            self.category = 'action'
            self.inc_subverse()
            mark = re.search(Play.action_pattern, self.text).end()
            self.text = self.text[mark:].replace('(','').replace(')','')

        elif len(self.text.strip()) > 0:
            self.category = 'verse'


    def to_dict(self, **kwargs):
        dd = {
            "category": self.category,
            "acte": Play.acte_count,
            "scene": Play.scene_count,
            "verse": Play.verse_count,
            "subverse": Play.subverse_count,
            "pos": self.pos,
            "text": self.text,
        }

        if kwargs is not None:
            dd.update(kwargs)
        return dd


if __name__ == "__main__":
    ps = Play()

    for n in range(ps.line_count):
        line = Line(n, ps.lines[n].strip())
        ps.add(line)
    ps.items = pd.DataFrame(ps.items)

    ps.items.dropna(subset = 'category', inplace = True)

    assert ps.items[ps.items.category == 'acte'].shape[0] == 5
    assert ps.items[ps.items.category == 'scene'].shape[0] == 44
    assert ps.items.scene.max() == 15
    assert ps.items.verse.max() == 967
    assert ps.items.subverse.max() == 3
    assert ps.items[ps.items.category == 'character_list'].shape[0] == 44
    assert ps.items[ps.items.category == 'character'].text.value_counts().shape[0] == 13
    assert np.alltrue(
        ps.items[ps.items.category == 'character'].text.value_counts().values ==
        [360, 161, 102,  86,  66,  60,  51,  31,  20, 17,  5,   5,   3]
    )
    assert ps.items[ps.items.category == 'action'].shape[0] == 159



    # paragraphize
    ps.concat_verse()

    assert ps.items.verse.value_counts().shape[0] == 967 + 1
    assert ps.items.subverse.max() == 3
    assert np.alltrue( ps.items.subverse.value_counts().values == [1917, 265, 43, 7])
    assert np.alltrue( ps.items.verse.value_counts().head(10).values == [93,  8,  7,  7,  6,  6,  6,  6,  6,  6])


    ps.save()

    # par = ps.items.copy()
    #
    # par['paragraph'] = par.groupby(
    #     by = ['category', 'acte', 'scene', 'verse', 'subverse']
    # )['text'].transform(lambda x: ','.join(x))
    #
    #
    # par.drop_duplicates(subset = ['category', 'acte', 'scene', 'verse', 'subverse', 'paragraph'],inplace = True)
    # par['text'] = par.paragraph
    # par = par[['category', 'acte', 'scene', 'verse', 'subverse', 'pos', 'text']]



    #     if "ACTE " in line:
    #         # reset scene count
    #         acte_count += 1
    #         scene_count = 0
    #         items.append(
    #             {
    #                 "category": "acte",
    #                 "acte": acte_count,
    #                 "scene": 1,
    #                 "pos": n ,
    #                 "text": line,
    #             }
    #         )
    #     elif "Scène" in line:
    #         scene_str = line.split('-')[0].strip()
    #         char_list = line.split('-')[1].strip()
    #
    #         scene_count += 1
    #         items.append(
    #             {
    #                 "category": "scene",
    #                 "acte": acte_count,
    #                 "scene": scene_count,
    #                 "pos": n ,
    #                 "text": scene_str,
    #             }
    #         )
    #         items.append(
    #             {
    #                 "category": "char_list",
    #                 "acte": acte_count,
    #                 "scene": scene_count,
    #                 "pos": n ,
    #                 "text": char_list,
    #             }
    #
    #         )
    #
    #     elif re.search(char_pattern, line):
    #         char_name = line[re.search(char_pattern, line).start():re.search(char_pattern, line).end()]
    #         items.append(
    #             {
    #                 "category": "character",
    #                 "acte": acte_count,
    #                 "scene": scene_count,
    #                 "pos": n ,
    #                 "text": char_name,
    #             }
    #         )
    #     elif re.search(action_pattern, line):
    #         action_str = line[re.search(action_pattern, line).end(): -1]
    #         items.append(
    #             {
    #                 "category": "action",
    #                 "acte": acte_count,
    #                 "scene": scene_count,
    #                 "pos": n ,
    #                 "text": action_str,
    #             }
    #         )
    #     else:
    #         paragraph = []
    #         start_n = n
    #         while (line.strip() != "") & (n < len(lines)):
    #             paragraph.append(line)
    #             try:
    #                 n +=1
    #                 line = lines[n].strip()
    #             except:
    #                 pass
    #         items.append(
    #             {
    #                 "category": "replique",
    #                 "acte": acte_count,
    #                 "scene": scene_count,
    #                 "pos": start_n ,
    #                 "text": " ".join(paragraph),
    #             }
    #         )
    #
    # items = pd.DataFrame(items)
    # items = items[items.text != ""].copy()
    #
    #
    #
    # # post parsing
    # # remove []
    # items["text"] = items.text.apply(lambda t: re.sub(r"\(\d+\)", "", t))
    #
    # # verse_id
    # verse_id = 0
    # for i, d in items.iterrows():
    #     if d["category"] == "character":
    #         verse_id += 1
    #     items.loc[i, "verse_id"] = verse_id
    # items["verse_id"] = items.verse_id.astype(int)
    #
    # items.loc[items.category == 'acte', 'verse_id' ] = 0
    # items.loc[items.category == 'scene', 'verse_id' ] = 0
    # items.loc[items.category == 'character list', 'verse_id' ] = 0
    #
    # # anomaly: "== ACTE ..." as replique => delete
    # # items = items.drop(index = items[(items.category == 'replique') & (items.text.str.contains('== ACTE'))].index).copy()
    # items.reset_index(drop = True, inplace = True)
    #
    # items = items[['pos','acte', 'scene', 'category', 'verse_id', 'text']]
    #
    # # save
    # with open(output_filename, "w", encoding="utf-8") as f:
    #     items.to_json(f, force_ascii=False, orient="records", indent=4)



def test(**kwargs):
    print(kwargs)
