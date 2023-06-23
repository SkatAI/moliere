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

    if 'script' in os.getcwd():
        root = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    else:
        root = os.getcwd()

    files = sorted(glob.glob(os.path.join(root,"textes/review", "*reviewed*.json")))
    print(f"loaded {len(files)} files")
    df = pd.DataFrame()

    for file in files:
        df = pd.concat([pd.read_json(file), df])

    original = df[df.version == 'original'].copy()
    selected = df[df.selected == 1].copy()
    selected_shape = selected.shape[0]
    selected.drop_duplicates(subset = ['acte', 'scene', 'verse_id'], inplace = True)
    if selected.shape[0] != selected_shape:
        print(f"{selected_shape - selected.shape[0]} selected duplicates were dropped")

    verse_ids = sorted(original.verse_id.unique())

    for verse_id in verse_ids:
        ocond = original.verse_id == verse_id
        scond = selected.verse_id == verse_id
        if selected[scond].shape[0] >0:
            original.loc[ocond, 'modern'] = selected[scond].text.values[0]
            original.loc[ocond, 'selection'] = selected[scond].version.values[0]
            try:
                assert original[ocond].char.values[0] == selected[scond].char.values[0]
            except:
                print(f"char mismatch {original[ocond].char.values[0]}!= {selected[scond].char.values[0]}")
        else:
            original.loc[ocond, 'modern'] = ''
            original.loc[ocond, 'selection'] = ''


    original.sort_values(by = ['verse_id', 'selection'], inplace = True)
    original = original[['acte', 'scene', 'version', 'selection', 'verse_id', 'char', 'text', 'modern']].copy()
    original.reset_index(inplace = True, drop = True)

    filename = os.path.join(root,"streamlit/", "medecin-malgre-lui_display.json")

    with open(filename, "w", encoding="utf-8") as f:
        original.to_json(f, force_ascii=False, orient="records", indent=4)
