import openai
import os
import re, json, csv
import time, datetime
from datetime import timedelta
import pandas as pd
import argparse
import glob
from tqdm import tqdm

pd.options.display.max_columns = 100
pd.options.display.max_rows = 60
pd.options.display.max_colwidth = 100
# pd.options.display.max_colwidth = None

pd.options.display.precision = 10
pd.options.display.width = 160
pd.set_option("display.float_format", "{:.2f}".format)
import numpy as np

from readability_score import ReadScore
from lingx.core.lang_model import get_nlp_object
from lingx.utils.lx import get_sentence_lx
from lingx.metrics.monolingual.le import get_le_score
from lingx.metrics.monolingual.nnd import get_nnd_score


def count_tokens(text):
    return len(text.split(' '))

play_root = "medecin"
play_root = "avare"
play_title = "medecin-malgre-lui"
play_title = "l-avare"


if __name__ == "__main__":
    # folders = ["./textes/mml06", "./textes/mml07"]
    # folders = ["textes/mml05", "textes/mml06", "textes/mml07", "textes/mml08", "textes/mml09"]
    folders = ["textes/avr01","textes/avr02","textes/avr03","textes/avr04"]
    # folders = ["textes/mml07", "textes/mml08"]
    nlp = get_nlp_object("fr", use_critt_tokenization = False, package="gsd")

    files = []
    if 'script' in os.getcwd():
        root = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    else:
        root = os.getcwd()

    for folder in folders:
        files += glob.glob(os.path.join(root,folder, f"*{play_root}*acte*.json"))
    print(f"loaded {len(files)} files")

    data = []
    for file in files:
        experiment = file.split("/")[-2]
        df = pd.read_json(file)

        for i, d in df.iterrows():


            if isinstance(d.text, dict):
                otexts = pd.DataFrame(index=d.text.keys(), data=d.text.values())
                otexts.columns = ["text"]
                otexts["verse_id"] = otexts.index
            if isinstance(d.text, list):
                otexts = pd.DataFrame(d.text)
                otexts.rename(columns = {'verse': 'verse_id'}, inplace = True)
            for j, ot in tqdm(otexts.iterrows()):
                text = ", ".join(ot.text.split(":")[1:]).strip()
                rs = ReadScore(nlp, text).score().to_dict()
                data.append(
                    {
                        "experiment": experiment,
                        "acte": d.acte,
                        "scene": d.scene,
                        "version": "original",
                        "chunk": i,
                        "verse_id": int(ot["verse_id"]),
                        # "tokens": count_tokens(text),
                        "tokens": rs['tokens'],
                        "sentences": rs['sentences'],
                        "idt": np.round(rs['idt'], 2),
                        "le": np.round(rs['le'], 2),
                        "char": ot.text.split(":")[0],
                        "text": text,
                    }
                )

            if isinstance(d.modern, dict):
                mtexts = pd.DataFrame(index=d.modern.keys(), data=d.modern.values())
                mtexts.columns = ["text"]
                mtexts["verse_id"] = mtexts.index
            if isinstance(d.modern, list):
                mtexts = pd.DataFrame(d.modern)
                mtexts.rename(columns = {'§verse': 'verse_id'}, inplace = True)

            for j, mt in tqdm(mtexts.iterrows()):
                text = ", ".join(mt.text.split(":")[1:]).strip()
                rs = ReadScore(nlp, text).score().to_dict()

                data.append(
                    {
                        "experiment": experiment,
                        "acte": d.acte,
                        "scene": d.scene,
                        "version": "modern",
                        "chunk": i,
                        "verse_id": int(mt["verse_id"]),
                        # "tokens": count_tokens(text),
                        "tokens": rs['tokens'],
                        "sentences": rs['sentences'],
                        "idt": np.round(rs['idt'], 2),
                        "le": np.round(rs['le'], 2),
                        "char": mt.text.split(":")[0],
                        "text": text,
                    }
                )

    data = pd.DataFrame(data)
    data.sort_values(by=["version", "acte", "scene", "verse_id","tokens", "experiment", "chunk"], inplace=True)

    modern = data[data.version == "modern"].copy()
    # modern.drop_duplicates(inplace=True, subset=["acte", "scene", "verse_id", "char", "text"])

    original = data[data.version == "original"].copy()
    original.drop_duplicates(inplace=True, subset=["acte", "scene", "verse_id"])

    data = pd.concat([original, modern])
    data.sort_values(by=["acte", "scene", "verse_id", "version","tokens", "experiment", "chunk"], inplace=True)
    data.reset_index(inplace=True, drop=True)

    data["selected"] = 0

    filename = os.path.join(root,"textes/review", f"{play_title}_review.json")

    with open(filename, "w", encoding="utf-8") as f:
        data.to_json(f, force_ascii=False, orient="records", indent=4)


    print(filename)
