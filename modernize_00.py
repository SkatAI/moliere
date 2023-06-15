'''
'''

import openai
import os
import re, json
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

from sentence_transformers import SentenceTransformer, util

def get_completion(prompt, model="gpt-3.5-turbo", temp=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature = temp,
    )
    return response.choices[0].message["content"]


def save(input, filename):
    df = pd.DataFrame(input)
    with open(filename, 'w', encoding='utf-8') as f:
        df.to_json(f , force_ascii=False, orient = 'records', indent = 4)
        # json.dump(some_df, f, indent = 4)


def get_prompt(text):

    prompt =  f'''Le texte suivant est extrait de la pièce de théatre 'Le Médecin Malgré Lui' de Molière.
Réecris ce texte en français, utilise un vocabulaire simple et moderne, garde chaque ligne du dialogue

Le texte à réécrire est: \n{text}'''


    return prompt

def count_tokens(text):
    return len(text.split(' '))

def build_text(**kwargs):

    # load file
    filename = './textes/medecin-malgre-lui_verse_original.json'
    df = pd.read_json(filename)
    cond = (df.verse_id > 0)
    if 'acte' in kwargs.keys():
        cond = cond & (df.acte == kwargs['acte'])
        # print('acte', kwargs['acte'] ,df[cond].shape[0])
    if 'scene' in kwargs.keys():
        cond = cond & (df.scene == kwargs['scene'])
        # print('scene', kwargs['scene'] ,df[cond].shape[0])
    if 'verse_id_start' in kwargs.keys():
        cond = cond & (df.verse_id >= kwargs['verse_id_start'])
        # print('verse_id_start', kwargs['verse_id_start'] ,df[cond].shape[0])
    if 'verse_id_end' in kwargs.keys():
        cond = cond & (df.verse_id < kwargs['verse_id_end'])
        # print('verse_id_end', kwargs['verse_id_end'] ,df[cond].shape[0])

    # get extract
    df = df[cond].copy()
    df.reset_index(inplace = True, drop = True)
    # build dialogue
    dialogue = []
    for i,d in df.iterrows():
        if d.category == 'personnage':
            dialogue.append(f"\n{d.text}:")
        elif d.category == 'verse':
            dialogue.append(d.text)

    dialogue = ' '.join(dialogue)
    print(f'===== verses: {len(df.verse_id.unique())} -- tokens {count_tokens(dialogue)}')
    return dialogue

def check(source, idx):
    df = pd.read_json(output_filename).to_dict(orient = 'records')
    text = df[idx][source].strip()
    print(f"-- [{source}] tokens: {count_tokens(text)} verses: ",len(text.split('\n')))
    # if show_text:
    print(text.replace('\n', '\n\n'))


chunks = [
    {'acte': 1, 'scene': 1, 'verse_id_start':  0, 'verse_id_end': 14},
    {'acte': 1, 'scene': 1, 'verse_id_start':  14, 'verse_id_end': 24},
    {'acte': 1, 'scene': 1, 'verse_id_start':  24, 'verse_id_end': 30},
    {'acte': 1, 'scene': 1, 'verse_id_start':  30, 'verse_id_end': 52},
    {'acte': 1, 'scene': 2, 'verse_id_start':  52, 'verse_id_end': 72},
    {'acte': 1, 'scene': 2, 'verse_id_start':  72, 'verse_id_end': 84},
    {'acte': 1, 'scene': 2, 'verse_id_start':  83, 'verse_id_end': 102},
    # {'acte': 1, 'scene': 3, 'verse_id_start':  102, 'verse_id_end': 103},
    # {'acte': 1, 'scene': 4, 'verse_id_start':  103, 'verse_id_end': 110},
    # {'acte': 1, 'scene': 4, 'verse_id_start':  110, 'verse_id_end': 119},
    # {'acte': 1, 'scene': 4, 'verse_id_start':  119, 'verse_id_end': 126},
    # {'acte': 1, 'scene': 4, 'verse_id_start':  126, 'verse_id_end': 138},
    # {'acte': 1, 'scene': 5, 'verse_id_start':  138, 'verse_id_end': 140},
    # {'acte': 1, 'scene': 5, 'verse_id_start':  140, 'verse_id_end': 148},
    # {'acte': 1, 'scene': 5, 'verse_id_start':  148, 'verse_id_end': 160},
    # {'acte': 1, 'scene': 5, 'verse_id_start':  160, 'verse_id_end': 166},
    # {'acte': 1, 'scene': 5, 'verse_id_start':  166, 'verse_id_end': 180},
    # {'acte': 1, 'scene': 5, 'verse_id_start':  180, 'verse_id_end': 202},
    # {'acte': 1, 'scene': 5, 'verse_id_start':  202, 'verse_id_end': 225},
    # {'acte': 1, 'scene': 5, 'verse_id_start':  225, 'verse_id_end': 240},
]

SLEEP_FOR = 10

if __name__ == "__main__":
    start_time = time.time()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    model   ="gpt-3.5-turbo"

    acte = 1
    scene = 1
    output_filename = f"./textes/medecin-malgre-lui_05_acte_{str(acte).zfill(2)}_scene_{str(scene).zfill(2)}.json"
    chunks = chunk_scene(acte, scene)

    if False:
        results = pd.read_json(output_filename).to_dict(orient = 'records')
        k = len(results)
    else:
        # cold start
        results = []
        k = 0

    for chunk in chunks[k:]:
        result = chunk.copy()
        print('--'*20)
        print(chunk)
        text = build_text(**chunk)
        result['text'] = text.strip()

        # now get the modernized text from GPT
        prompt = get_prompt(text)
        try:
            response = get_completion(prompt, model=model, temp=0)
            result['modern'] = response
            results.append(result)
            save(results, output_filename)

        except Exception as error:

            save(results, output_filename)
            # handle the exception
            print("*** An exception occurred:", type(error).__name__)
            raise error


        # print results
        print("-- verses: ",len(response.split('\n')))
        elapsed = (time.time() - start_time)
        print('--'*20, str(timedelta(seconds=elapsed)).split('.')[0])
        check('modern', k)

        k +=1
        if k < len(chunks):
            print(f"sleep {SLEEP_FOR}", end = " ")
            time.sleep(SLEEP_FOR)
            print('-')


        # suite = input("next ? ")
        # if suite.lower() in ['no','n']:
        #     break;


    # calculate simillarity for each sentence pair
    models= ['sentence-transformers/all-MiniLM-L6-v2','sentence-transformers/all-mpnet-base-v2']
    models= ['sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2','sentence-transformers/paraphrase-multilingual-mpnet-base-v2']

    df = pd.read_json(output_filename)
    data = []
    model_MiniLM = SentenceTransformer(models[0])
    model_mpnet = SentenceTransformer(models[1])

    for i, d in df.iterrows():
        text = d.text.strip().split('\n')
        modern = d.modern.strip().split('\n')
        verse_count = max([len(text), len(modern)])
        for k in range(verse_count):
            str_text = text[k] if k < len(text)  else ''
            str_modern = modern[k] if k < len(modern)  else ''
            if (str_text != '') & (str_modern!=''):
                embeddings = model_MiniLM.encode([text[k], modern[k]])
                score_minilM=util.pytorch_cos_sim(embeddings[0], embeddings[1])
                embeddings = model_mpnet.encode([text[k], modern[k]])
                score_mpnet=util.pytorch_cos_sim(embeddings[0], embeddings[1])

                score_minilM = np.round(float(score_minilM[0][0]),3)
                score_mpnet = np.round(float(score_mpnet[0][0]),3)

            else:
                score_minilM, score_mpnet = 0,0

            data.append({
                'chunk_id': i+1,
                'acte': d.acte,
                'scene': d.scene,
                'verse_id': d.verse_id_start + k,
                'text': str_text,
                'modern': str_modern,
                'sim_miniLM': score_minilM,
                'sim_mpnet': score_mpnet,
            })
            k +=1
    data = pd.DataFrame(data)
