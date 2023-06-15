'''
results should
- rewrite in modern french
- keep dialogue structure: no summary
- keep most or all verses
- reduce length of long verses
- be able to perform on extracts or full version of the scene
'''

import openai
import os
import re
import time, datetime
from datetime import timedelta
import pandas as pd
pd.options.display.max_columns = 100
pd.options.display.max_rows = 60
pd.options.display.max_colwidth = 100
pd.options.display.precision = 10
pd.options.display.width = 160
pd.set_option("display.float_format", "{:.2f}".format)
import numpy as np

def get_completion(prompt, model="gpt-3.5-turbo", temp=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature = temp,
    )
    return response.choices[0].message["content"]

def sort_verses(df):
    k = 0
    for item in [ 'acte', 'scene', 'setup', 'personnage', 'verse', 'modern']:
        df.loc[df.item == item, 'item_sort' ] = k
        k += 1
    df['item_sort'] = df.item_sort.astype(int)
    df.sort_values(by = ['acte','scene','verse', 'item_sort'], inplace = True)
    df.reset_index(inplace = True, drop = True)
    return df

def save(df, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        df.to_json(f , force_ascii=False, orient = 'records', indent = 4)

def get_prompt(text, previous):
    # test add acte and scene number
    # test add garde toutes les répartis de chaque personnage
    prompt =  f'''Le texte suivant est extrait de la pièce de théatre 'Le Médecin Malgré Lui' de Molière.
    Réecris ce texte en français, utilise un vocabulaire simple et moderne.

    Le texte à réécrire est: \n{text}'''
    return prompt



SLEEP_FOR = 15

if __name__ == "__main__":
    start_time = time.time()

    openai.api_key = os.getenv("OPENAI_API_KEY")
    model   ="gpt-3.5-turbo"
    # input_filename = './textes/medecin-malgre-lui_03_original.json'
    input_filename = './textes/medecin-malgre-lui_03_acte_1_modern.json'
    output_filename = './textes/medecin-malgre-lui_03_acte_1_modern_47.json'

    df = pd.read_json(input_filename)

    # only the 1st act and scene
    scope = (df.acte == 1) & (df.verse > 47)
    df = df[scope].copy()

    tr = df.copy()

    verse_numbers = sorted(df.verse.unique())[1:]
    verse_count = df[df.item == 'verse'].shape[0]
    count_idx = 1

    history = 2

    for i, d in df[df.item == 'verse'].iterrows():
        tmp_a = df[df.verse == d.verse].reset_index(drop = True)
        text = ': '.join(tmp_a.text.values[-2::]).replace(".:", ":")

        new_row = {
            'acte': tmp_a.acte.unique()[0],
            'scene': tmp_a.scene.unique()[0],
            'verse': tmp_a.verse.unique()[0],
            'item': 'modern',
        }
        # TODO reset for each new scene


        # get N previous verses
        verse_scope = range(max([verse_numbers[0], d.verse - history]), d.verse)
        previous = []
        for j in verse_scope:
            tmp_b = df[df.verse == j].reset_index(drop = True)
            previous.append(
                ': '.join(tmp_b.text.values[-2::]).replace(".:", ":")
            )
        previous = '\n'.join(previous)

        # now get the modernized text from GPT
        prompt = get_prompt(text, previous)
        try:
            response = get_completion(prompt, model=model, temp=0)
        except Exception as error:
            tr = sort_verses(tr)
            save(tr, output_filename)
            # handle the exception
            print("An exception occurred:", type(error).__name__) # An exception occurred: division by zero
            raise error

        new_row['text'] =  ' '.join(response.split(': ')[1:])

        tr.loc[tr.index.max() + 1] = new_row

        # print results
        elapsed = (time.time() - start_time)
        print('--'*20, str(timedelta(seconds=elapsed)).split('.')[0])

        print( f"{count_idx}/{verse_count}",  tr.index.max())
        if len(text)> 150:
            print( text[:150], "...")
        else:
            print( text)

        if len(response)> 150:
            print( response[:150], "...")
        else:
            print( response)


        count_idx += 1

        # print('*** sleep', SLEEP_FOR)
        time.sleep(SLEEP_FOR)
        # print('--> waking up')

        if False:
#             print(f"""
# \n\n----
# \n\t [prompt]: {prompt}
# \n
# \n\t [previous]: {previous}
# \n\t [text]: {text}
#
# \n\n\t [response]: {response}""")

            suite = input("next ? ")
            if suite.lower() in ['no','n']:
                break;

    # sorting order
    tr = sort_verses(tr)

    save(tr, output_filename)
