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


if __name__ == "__main__":
    folders = ["./textes/mml06", "./textes/mml07"]
    folders = ["./textes/mml05", "./textes/mml06", "./textes/mml07"]
    files = []
    for folder in folders:
        files += glob.glob(os.path.join(folder, "medecin*acte*.json"))
    print(f"loaded {len(files)} files")

    data = []
    for file in files:
        experiment = file.split("/")[2]
        df = pd.read_json(file)

        for i, d in df.iterrows():
            otexts = pd.DataFrame(index=d.text.keys(), data=d.text.values())
            otexts.columns = ["text"]
            otexts["verse_id"] = otexts.index
            for j, ot in otexts.iterrows():
                data.append(
                    {
                        "experiment": experiment,
                        "acte": d.acte,
                        "scene": d.scene,
                        "version": "original",
                        "chunk": i,
                        "verse_id": ot.verse_id,
                        "char": ot.text.split(":")[0],
                        "text": ", ".join(ot.text.split(":")[1:]),
                    }
                )

            mtexts = pd.DataFrame(index=d.modern.keys(), data=d.modern.values())
            mtexts.columns = ["text"]
            mtexts["verse_id"] = mtexts.index
            for j, mt in mtexts.iterrows():
                data.append(
                    {
                        "experiment": experiment,
                        "acte": d.acte,
                        "scene": d.scene,
                        "version": "modern",
                        "chunk": i,
                        "verse_id": mt.verse_id,
                        "char": mt.text.split(":")[0],
                        "text": ", ".join(ot.text.split(":")[1:]),
                    }
                )

    data = pd.DataFrame(data)
    data.sort_values(
        by=["version", "acte", "scene", "verse_id", "experiment", "chunk"], inplace=True
    )
    modern = data[data.version == "modern"].copy()

    modern.drop_duplicates(
        inplace=True, subset=["acte", "scene", "verse_id", "char", "text"]
    )

    original = data[data.version == "original"].copy()
    original.drop_duplicates(inplace=True, subset=["acte", "scene", "verse_id"])

    data = pd.concat([original, modern])
    data.sort_values(
        by=["acte", "scene", "verse_id", "version", "experiment", "chunk"], inplace=True
    )
    data.reset_index(inplace=True, drop=True)

    data["text"] = data.text.apply(lambda txt: txt.strip())

    data["selected"] = 0

    # data.to_csv("./textes/medecin-malgre-lui_modernized.csv", quoting  = csv.QUOTE_ALL, index = False)
    filename = "./textes/review/medecin-malgre-lui_review.json"
    with open(filename, "w", encoding="utf-8") as f:
        data.to_json(f, force_ascii=False, orient="records", indent=4)
