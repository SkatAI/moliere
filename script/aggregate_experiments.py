import openai
import os
import re, json, csv
import time, datetime
from datetime import timedelta
import pandas as pd
import argparse
import glob

pd.options.display.max_columns = 100
pd.options.display.max_rows = 60
pd.options.display.max_colwidth = 100
pd.options.display.max_colwidth = None

pd.options.display.precision = 10
pd.options.display.width = 160
pd.set_option("display.float_format", "{:.2f}".format)
import numpy as np

def count_tokens(text):
    return len(text.split(' '))

play_root = "medecin"
play_root = "avare"
play_title = "medecin-malgre-lui"
play_title = "l-avare"

verse_col = "verse_id"
verse_col = "verse"


if __name__ == "__main__":
    # folders = ["./textes/mml06", "./textes/mml07"]
    # folders = ["textes/mml05", "textes/mml06", "textes/mml07", "textes/mml08", "textes/mml09"]
    folders = ["textes/avr01"]
    # folders = ["textes/mml07", "textes/mml08"]
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
                otexts[verse_col] = otexts.index
            if isinstance(d.text, list):
                otexts = pd.DataFrame(d.text)

            for j, ot in otexts.iterrows():
                text = ", ".join(ot.text.split(":")[1:]).strip()
                data.append(
                    {
                        "experiment": experiment,
                        "acte": d.acte,
                        "scene": d.scene,
                        "version": "original",
                        "chunk": i,
                        verse_col: int(ot[verse_col]),
                        "tokens": count_tokens(text),
                        "char": ot.text.split(":")[0],
                        "text": text,
                    }
                )

            if isinstance(d.modern, dict):
                mtexts = pd.DataFrame(index=d.modern.keys(), data=d.modern.values())
                mtexts.columns = ["text"]
                mtexts[verse_col] = mtexts.index
            if isinstance(d.modern, list):
                mtexts = pd.DataFrame(d.modern)

            for j, mt in mtexts.iterrows():
                text = ", ".join(mt.text.split(":")[1:]).strip()
                data.append(
                    {
                        "experiment": experiment,
                        "acte": d.acte,
                        "scene": d.scene,
                        "version": "modern",
                        "chunk": i,
                        verse_col: int(mt[verse_col]),
                        "tokens": count_tokens(text),
                        "char": mt.text.split(":")[0],
                        "text": text,
                    }
                )

    data = pd.DataFrame(data)
    data.sort_values(by=["version", "acte", "scene", verse_col,"tokens", "experiment", "chunk"], inplace=True)

    modern = data[data.version == "modern"].copy()
    modern.drop_duplicates(inplace=True, subset=["acte", "scene", verse_col, "char", "text"])

    original = data[data.version == "original"].copy()
    original.drop_duplicates(inplace=True, subset=["acte", "scene", verse_col])

    data = pd.concat([original, modern])
    data.sort_values(by=["acte", "scene", verse_col, "version","tokens", "experiment", "chunk"], inplace=True)
    data.reset_index(inplace=True, drop=True)

    data["selected"] = 0

    filename = os.path.join(root,"textes/review", f"{play_title}_review.json")

    with open(filename, "w", encoding="utf-8") as f:
        data.to_json(f, force_ascii=False, orient="records", indent=4)
