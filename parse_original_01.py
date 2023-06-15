import json
import re
import pandas as pd

filename = './textes/medecin-malgre-lui.txt'

def remove_brackets(verse):
    reg = r'\[\d+\]'
    return re.sub(reg, '' , verse)

if __name__ == "__main__":
    with open(filename, 'r') as f:
        text = f.read()

    parts = text.split('\n\n')
    parts = [p.strip() for p in parts]

    df = pd.DataFrame(
        columns = ['text'],
    )
    df['text'] = parts
    df['acte'] = 0
    df['scene'] = 0
    df['item'] = ''

    acte_count = 0
    scene_count = 0
    verse_count = 1
    personnage_pattern = r"^[A-ZÉÈ\.]{2,}"

    for i, d in df.iterrows():
        text = d.text
        if "== ACTE" in d.text:
            df.loc[i, 'item'] = 'acte'
            df.loc[i, 'verse'] = 0
            text = text[3:]
            acte_count +=1
            scene_count = 0
        elif "-- SCENE" in d.text:
            df.loc[i, 'item'] = 'scene'
            df.loc[i, 'verse'] = 0
            text = text[3:]
            scene_count +=1
        elif re.match(personnage_pattern, d.text):
            df.loc[i, 'item'] = 'personnage'
            df.loc[i, 'verse'] = verse_count
        else:
            df.loc[i, 'item'] = 'verse'
            df.loc[i, 'verse'] = verse_count
            verse_count +=1

        df.loc[i, 'text'] = remove_brackets(text.replace('\n',' '))
        df.loc[i, 'acte'] = acte_count
        df.loc[i, 'scene'] = scene_count

        print(f"acte: {acte_count}, scene {scene_count}, verse {verse_count}")

    df['verse'] = df['verse'].astype('int')
    # tag the line after SCENE as scene_setup
    vc = df.verse.value_counts()
    # all verses that occur  more than twice
    verse_numbers = sorted(vc[vc>2].keys())[1:]

    for verse_count in verse_numbers:
        id = df[df.verse == verse_count].index[0]
        df.loc[id, 'item'] = 'setup'



    with open("./textes/medecin-malgre-lui_03_original.json", 'w', encoding='utf-8') as f:
        df.to_json(f , force_ascii=False, orient = 'records', indent = 4)
