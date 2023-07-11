# "prompt": "Le texte suivant est extrait de la pièce de théatre 'L'Avare' de Molière.\nSimplifie ce dialogue en français moderne. Utilise un vocabulaire simple.\n\nLe texte à réécrire est: \n{text}"


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

def initialize(experiment):
    config_file = f"../textes/{experiment}/config.json"
    conf = pd.read_json(config_file).to_dict(orient="records")[0]
    conf["version"] = str(conf["version"]).zfill(2)
    conf["step"] = int(conf["step"])
    # conf["window_size"] = 2 * conf["step"] + 1
    conf["window_size"] = conf["window_size"]

    return conf


def cli_args():
    parser = argparse.ArgumentParser(description="Description of your script.")
    parser.add_argument("--experiment", help="experiment: i.e. mml06")
    parser.add_argument("--acte", help="acte", default=None)
    parser.add_argument("--scene", help="scene", default=None)

    return parser.parse_args()


def sliding_window(array, config):
    num_windows = (len(array) - config['window_size']) // config['step'] + 1
    windows = []
    # end_ = len(array) + 1
    end_ = 0
    for i in range(num_windows):
        start = i * config['step']
        end_ = start + config['window_size']
        window = array[start:end_]
        windows.append(window)
    if end_ < len(array):
        window = array[-config['window_size'] + 1 : len(array)]
        window.append(array[-1] + 1)
        windows.append(window)
    return windows

def chunk_scene(df, config):

    from_verse = df.verse_id.min()
    to_verse = df.verse_id.max()

    windows = sliding_window(list(range(from_verse, to_verse + 1)), config)
    chunks = []
    for w in windows:
        chunks.append(
            {
                "acte": acte,
                "scene": scene,
                "verse_start": w[0],
                "verse_end": w[-1],
            }
        )

    return chunks


def build_text(df, **kwargs):
    # load file
    cond = df.verse_id > 0

    if "verse_start" in kwargs.keys():
        cond = cond & (df.verse_id >= kwargs["verse_start"])

    if "verse_end" in kwargs.keys():
        cond = cond & (df.verse_id < kwargs["verse_end"])

    # get extract
    df = df[cond].copy()

    df.reset_index(inplace=True, drop=True)
    # multiple lines repliques are kept over multiple lines but text directly follows character name after a ":"
    dialogue = []
    for i, d in df.iterrows():

        if d.category == "character":
            if len(dialogue) > 0:
                dialogue.append('\n'.join(text))
            text = []
            dialogue.append(f"\n{d.text.replace('.','').strip()}:")
        elif d.category == "verse":
            text.append(d.text.strip())

    dialogue.append('\n'.join(text))
    dialogue = " ".join(dialogue).strip()
    print(f"===== repliques: {len(df.verse_id.unique())}")
    return dialogue

def replique_id(start_id,lines):
    result = []
    text =[]
    verse_id = start_id
    for n in range(len(lines)):

        line = lines[n]
        if re.match(char_pattern, line):
            text = [line]
            # n +=1
        else:
            if not re.match(char_pattern, line):
                text.append(line)
                # n +=1
        if (n+1 < len(lines)):
            if (re.match(char_pattern, lines[n+1])):
                result.append({
                    'verse_id': verse_id,
                    'text':  '\n'.join(text)
                })
                verse_id +=1
    result.append({
        'verse_id': verse_id,
        'text':  '\n'.join(text)
    })
    return result


def get_completion(prompt, model, temp):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temp,
    )
    return response.choices[0].message["content"]

def save(input, filename):
    df = pd.DataFrame(input)
    with open(filename, "w", encoding="utf-8") as f:
        df.to_json(f, force_ascii=False, orient="records", indent=4)

    data = pd.DataFrame(chunks)
    with open(output_filename, "w", encoding="utf-8") as f:
        data.to_json(f, force_ascii=False, orient="records", indent=4)


def get_prompt(text):
    prompt = config['prompt']
    prompt = prompt.replace("{text}", text)
    return prompt

def get_personnages(df, chunk):
    texts = df[(df.verse_id >= chunk['verse_start']) & (df.verse_id < chunk['verse_end']) & (df.category == 'character')].text.unique()
    personnages = []
    punct_pattern = f"(,|\.|\s)"
    for line in texts:
        match = re.search(punct_pattern, line)
        personnages.append(line[:match.start()])
    return sorted(set(personnages))


char_pattern = r"(Anselme|Brindavoine|Cléante|Dame Claude|Élise|Frosine|Harpagon|La Flèche|La Merluche|Maître Jacques|Maître Simon|Mariane|Valère|Le commissaire)"
SLEEP_FOR = 10

if __name__ == "__main__":

    start_time = time.time()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    args = cli_args()
    acte = int(args.acte)
    scene = int(args.scene)
    print(args)
    config = initialize(args.experiment)
    output_filename = f"../textes/{args.experiment}/l-avare_{args.experiment}_acte_{str(acte).zfill(2)}_scene_{str(scene).zfill(2)}.json"
    print("output_filename:", output_filename)

    # load texte, subset to scene
    df = pd.read_json(config['source'])
    df = df[(df.acte == acte) & (df.scene == scene)].copy()
    df.reset_index(inplace=True, drop=True)

    chunks = chunk_scene(df[df.verse_id > 0], config)
    print(f"{len(df.verse_id.unique())} repliques; {len(chunks)} chunks")

    k = 0
    for chunk in chunks:
        text = build_text(df,**chunk).strip()
        print('--'*20)
        print(chunk)
        chunk["text"] = replique_id(
            chunk['verse_start'],
            text.strip().split('\n')
        )

        prompt = get_prompt(text)

        try:
            modern =  get_completion(
                prompt,
                model=config['model'],
                temp=config['temperature'])

            chunk["modern"] = replique_id(
                chunk['verse_start'],
                modern.strip().split('\n')
            )

            print('>>' * 10, "modern")
            print(modern)
            print('>>' * 10, "/modern")
            print(f" text: {len(chunk['text'])} repliques \t modern: {len(chunk['modern'])} repliques  ")
            save(chunks, output_filename)

        except Exception as error:
            save(chunks, output_filename)
            # handle the exception
            print("*** An exception occurred:", type(error).__name__)
            raise error
        k += 1
        if k < len(chunks):
            print(f"sleep {SLEEP_FOR}", end=" ")
            time.sleep(SLEEP_FOR)
            print("-")
