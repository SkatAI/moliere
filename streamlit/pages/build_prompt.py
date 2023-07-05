import streamlit as st
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

play_title = "medecin-malgre-lui"
play_title = "l-avare"

actes_options = [1,2,3]
scenes_options = {
    1: [n for n in range(1,6)],
    2: [n for n in range(1,6)],
    3: [n for n in range(1,12)],
}

def get_completion(prompt, model="gpt-3.5-turbo", temp=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temp,
    )
    return response.choices[0].message["content"]


def load_config():
    config_file = os.path.join(os.getcwd(), "./streamlit/pages/build_prompt_config.json")

    conf = pd.read_json(config_file).to_dict(orient="records")[0]
    return conf

def build_text(config, **kwargs):
    df = pd.read_json(config['source'])
    cond = (df.acte == kwargs['acte_choice']) & (df.scene == kwargs['scene_choice'])
    min_verse = df[cond & (df.verse_id > 0)].verse_id.min()
    cond = cond & (df.verse_id >= kwargs['verse_start'] + min_verse) & (df.verse_id < kwargs['verse_start'] + min_verse + kwargs['verse_count'])
    df = df[cond].copy()
    print(f"===== {len(df.verse_id.unique())} originales repliques")

    dialogue = []
    for i, d in df.iterrows():

        if d.category == "character":
            if len(dialogue) > 0:
                dialogue.append('\n'.join(text))
            text = []
            dialogue.append(f"\n\n{d.text.replace('.','').strip()}:")

        elif d.category in ["verse","action"]:
            text.append(d.text.strip())

    dialogue.append('\n'.join(text))
    dialogue = " ".join(dialogue).strip()
    return dialogue


if __name__ == "__main__":
    st.set_page_config(page_title="BuildPrompt", layout="wide")
    # openai.api_key = os.getenv("OPENAI_API_KEY")

    config = load_config()

    with st.sidebar:

        acte_choice = st.selectbox("Acte:", actes_options, key = 'menu_acte')
        scene_choice = st.selectbox("Scène:", scenes_options, key = 'menu_scene')
        verse_start = st.number_input("Verse start:", value = 0)
        verse_count = st.number_input("Verse count:", value = 5)

    st.write('acte_choice', acte_choice, 'scene_choice', scene_choice, 'verse_start', verse_start, 'verse_count', verse_count )


    col1, col2 = st.columns([8, 8])
    with col1:
        with st.form("prompt_form"):
            experiment = st.text_input("Experiment")
            notes = st.text_input("Notes")
            prompt = st.text_area("prompt", height=200,value = config['prompt'])
            submitted = st.form_submit_button("Submit")

    with col2:
        text = build_text(config, **{'acte_choice': acte_choice, 'scene_choice': scene_choice, 'verse_start': verse_start, 'verse_count': verse_count })

        for txt in  text.split('\n'):
            st.write(txt)

    st.divider()
    if submitted:

        prompt = prompt.replace("{text}",text)
        modern =  get_completion(
            prompt,
            model=config['model'],
            temp=0)

        original_token_count = len(text.split(' '))
        original_verse_count = len(text.split('\n'))
        modern_token_count = len(modern.split(' '))
        modern_verse_count = len(modern.split('\n'))
        ratio = f"{np.round(100.0 * modern_token_count / original_token_count, 2)}%"

        col1, col2 = st.columns([8, 8])
        with col1:
            st.subheader("original")
            st.caption(f" {original_verse_count} verses; {original_token_count} tokens ")
            st.write(text)

        with col2:
            st.subheader("transformed")
            st.caption(f" {modern_verse_count} verses; {modern_token_count} tokens => {ratio} vs original")
            st.write(modern)


        with st.form("result_form"):
            comment = st.text_area("so ?", height=150)
            result_submitted = st.form_submit_button("Save")

            if result_submitted:
                st.write("Saving ...")
