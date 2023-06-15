import openai
import os
import re, json
import time, datetime
from datetime import timedelta
import pandas as pd
import argparse
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


def save(input, filename):
    df = pd.DataFrame(input)
    with open(filename, 'w', encoding='utf-8') as f:
        df.to_json(f , force_ascii=False, orient = 'records', indent = 4)

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
            dialogue.append(f"\n{d.text.strip()}:")
        elif d.category == 'verse':
            dialogue.append(d.text.strip())

    dialogue = ' '.join(dialogue).strip()
    print(f'===== verses: {len(df.verse_id.unique())} -- tokens {count_tokens(dialogue)}')
    return dialogue

def check(source, idx):
    df = pd.read_json(output_filename).to_dict(orient = 'records')
    text = [v.strip() for k,v in df[idx][source].items()]
    print(f"-- [{source}] tokens: {count_tokens(' '.join(text))} verses: {len(text)}")
    for k,v in df[idx][source].items():
        print(f"{k}: {v}")


def sliding_window(array):
    num_windows = (len(array) - WINDOW_SIZE) // STEP + 1
    windows = []
    # end_ = len(array) + 1
    end_ = 0
    for i in range(num_windows):
        start = i * STEP
        end_ = start + WINDOW_SIZE
        window = array[start:end_]
        windows.append(window)
    if end_ < len(array):
        window = array[-WINDOW_SIZE +1:len(array)]
        print(f"add {array[-1] +1}")
        window.append(array[-1] +1)
        windows.append(window)
    return windows

def chunk_scene(acte, scene):
    # load scene, get number of verses
    # use sliding window to create chunks

    df = pd.read_json(input_filename)
    cond = (df.verse_id > 0)
    cond = cond & (df.acte == acte)
    cond = cond & (df.scene == scene)
    df = df[cond].copy()
    df.reset_index(inplace = True, drop = True)
    from_verse_id = df.verse_id.min()
    to_verse_id = df.verse_id.max()
    windows = sliding_window(
        list(range(from_verse_id, to_verse_id + 1))
    )
    chunks = []
    for w in windows:
        chunks.append({
            'acte': acte,
            'scene': scene,
            'verse_id_start': w[0],
            'verse_id_end': w[-1],
        })


    return chunks

def versify(verse_id_start, text):
    k = verse_id_start
    verses = text.split('\n')
    versified = {}
    for i in range(len(verses)):
        versified[verse_id_start + i] = verses[i]

    return versified


SLEEP_FOR = 10
# VERSION = "07"
# STEP = 9
# WINDOW_SIZE = 2 * STEP + 1
# ACTE  = 3
# SCENE  = None

def initialize(experiment):
    config_file = f"./textes/{experiment}/config.json"
    conf = pd.read_json(config_file).to_dict(orient ="records")[0]
    conf['version'] = str(conf['version']).zfill(2)
    conf['step'] = int(conf['step'])
    conf['window_size'] = 2 * conf['step'] + 1

    return conf


def cli_args():
    # Create the parser
    parser = argparse.ArgumentParser(description='Description of your script.')

    # Add the arguments
    parser.add_argument('--experiment', help='experiment: i.e. mml06')
    parser.add_argument('--acte', help='acte', default = None)
    parser.add_argument('--scene', help='scene', default = None)

    return parser.parse_args()



if __name__ == "__main__":
    start_time = time.time()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    args = cli_args()
    config = initialize(args.experiment)

    model   = config['model']
    input_filename = config['source']

    df = pd.read_json(input_filename)

    if args.acte is not None:
        df = df[df.acte ==  int(args.acte)].copy()

        if args.scene is not None:
            df = df[df.scene ==  int(args.scene)].copy()

        df.reset_index(inplace  = True, drop  = True)

    acte_scenes = df[['acte','scene']].drop_duplicates().to_dict(orient = "records")

    print(acte_scenes)


    for acte_scene in acte_scenes:
        acte = acte_scene['acte']
        scene = acte_scene['scene']
        print(f"========== Acte: {acte}, Scene: {scene} ==========")

        output_filename = f"./textes/medecin-malgre-lui_{VERSION}_acte_{str(acte).zfill(2)}_scene_{str(scene).zfill(2)}.json"
        print('output_filename:', output_filename)
        # in case of restart
        if False:
            results = pd.read_json(output_filename).to_dict(orient = 'records')
            k = len(results)
        else:
            # cold start
            results = []
            k = 0

        chunks = chunk_scene(acte, scene)
        print(f"-- {len(chunks)} chunks")

        for chunk in chunks[k:]:
            result = chunk.copy()
            print('--'*20)
            print(chunk)
            text = build_text(**chunk).strip()
            result['text'] = versify(chunk['verse_id_start'], text)

            # now get the modernized text from GPT
            prompt = get_prompt(text)
            try:
                response = get_completion(prompt, model=model, temp=0)
                result['modern'] = versify(chunk['verse_id_start'], response)
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
