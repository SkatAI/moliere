import json
import re
import pandas as pd
import numpy as np
import uuid

input_filename = './textes/medecin-malgre-lui_04.json'

def get_uid(item):
    return '-'.join([
        str(item['acte']).zfill(2),
        str(item['scene']).zfill(2),
        item['category'][:2],
        str(item['order']).zfill(4),
        str(uuid.uuid4()).split('-')[0]
    ])

def create_item(verse_count, order, scene, category, text):
    item = {
        'acte': scene['acte'],
        'scene': scene['scene'],
        'category': category,
        'text': text,
        'verse_id': verse_count,
        'order': order,
        'source': source_type
    }
    item['id'] = get_uid(item)
    return item



if __name__ == "__main__":
    personnage_pattern = r"^[A-ZÉÈ\.]{2,}"
    role_pattern = r"(SGANARELLE|MARTINE|M. ROBERT|GÉRONTE|LÉANDRE|LUCINDE|JACQUELINE|PERRIN|LUCAS|VALÈRE|THIBAUT)(:|\.|,)"

    scenes = pd.read_json(input_filename).to_dict(orient = 'records')

    items = []
    verse_count = 0
    order = 0
    source_type = 'original'
    for scene in scenes:
        original = scene['texte']
        for text in original.split('\n'):
            tmp = re.split(role_pattern, text)
            if len(tmp) > 1:
                verse_count +=1
                order +=1
                items.append(
                    create_item(verse_count, order, scene, 'personnage', tmp[1])
                )
                if len(tmp) > 3:
                    order +=1
                    items.append(
                        create_item(verse_count, order, scene, 'verse', tmp[3])
                    )
            elif len(tmp) == 1:
                    order +=1
                    items.append(
                        create_item(verse_count, order, scene, 'verse', tmp[0])
                    )
            else:
                print(tmp)

    verse_count = 0
    order = 0
    source_type = 'modern'
    for scene in scenes:
        modern   = scene['modern_01']
        for text in modern.split('\n'):
            tmp = re.split(role_pattern, text)
            if len(tmp) > 1:
                verse_count +=1
                order +=1
                items.append(
                    create_item(verse_count, order, scene, 'personnage', tmp[1])
                )
                if len(tmp) > 3:
                    order +=1
                    items.append(
                        create_item(verse_count, order, scene, 'verse', tmp[3])
                    )
            elif len(tmp) == 1:
                    order +=1
                    items.append(
                        create_item(verse_count, order, scene, 'verse', tmp[0])
                    )
            else:
                print(tmp)


    df = pd.DataFrame(items)
    df.sort_values(by = ['acte', 'scene', 'order','verse_id'], inplace = True)
    df.reset_index(inplace = True, drop = True)

    df['text'] = df.text.apply(lambda d : d.strip())


    df = df[['id', 'acte', 'scene','verse_id','source','category','text']].copy()

    output_filename = "./textes/medecin-malgre-lui_04_modern.json"
    with open(output_filename, 'w', encoding='utf-8') as f:
        df.to_json(f , force_ascii=False, orient = 'records', indent = 4)


    output_filename = "./textes/medecin-malgre-lui_04_02_modern.json"
    df = df[[ 'acte', 'scene','source','category','text']].copy()

    # df.drop_duplicates(subset = ['acte', 'scene', 'text'], inplace = True)

    with open(output_filename, 'w', encoding='utf-8') as f:
        df.to_json(f , force_ascii=False, orient = 'records', indent = 4)


    #
    #     df[cond].tail(10)



    # parts = text.split('\n\n')
    # parts = [p.strip() for p in parts]
    #
    # df = pd.DataFrame(
    #     columns = ['text'],
    # )
    # df['text'] = parts
    # df['acte'] = 0
    # df['scene'] = 0
    # df['item'] = ''
    #
    # acte_count = 0
    # scene_count = 0
    # verse_count = 1
    # personnage_pattern = r"^[A-ZÉÈ\.]{2,}"
    #
    # for i, d in df.iterrows():
    #     text = d.text
    #     if "== ACTE" in d.text:
    #         df.loc[i, 'item'] = 'acte'
    #         df.loc[i, 'verse'] = 0
    #         text = text[3:]
    #         acte_count +=1
    #         scene_count = 0
    #     elif "-- SCENE" in d.text:
    #         df.loc[i, 'item'] = 'scene'
    #         df.loc[i, 'verse'] = 0
    #         text = text[3:]
    #         scene_count +=1
    #     elif re.match(personnage_pattern, d.text):
    #         df.loc[i, 'item'] = 'personnage'
    #         df.loc[i, 'verse'] = verse_count
    #     else:
    #         df.loc[i, 'item'] = 'verse'
    #         df.loc[i, 'verse'] = verse_count
    #         verse_count +=1
    #
    #     df.loc[i, 'text'] = remove_brackets(text.replace('\n',' '))
    #     df.loc[i, 'acte'] = acte_count
    #     df.loc[i, 'scene'] = scene_count
    #
    #     print(f"acte: {acte_count}, scene {scene_count}, verse {verse_count}")
    #
    # df['verse'] = df['verse'].astype('int')
    # # tag the line after SCENE as scene_setup
    # vc = df.verse.value_counts()
    # # all verses that occur  more than twice
    # verse_numbers = sorted(vc[vc>2].keys())[1:]
    #
    # for verse_count in verse_numbers:
    #     id = df[df.verse == verse_count].index[0]
    #     df.loc[id, 'item'] = 'setup'
    #
    #
    #
    # with open("./textes/medecin-malgre-lui_03_original.json", 'w', encoding='utf-8') as f:
    #     df.to_json(f , force_ascii=False, orient = 'records', indent = 4)
