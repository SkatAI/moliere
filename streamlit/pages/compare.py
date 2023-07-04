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

verse_col = "verse_id"
verse_col = "verse"


def count_tokens(text):
    return len(text.split(' '))


def progress(subset):
    verses_count = len(subset[verse_col].unique())
    verses_reviewed = len(subset[subset.selected == 1][verse_col].unique())
    pct = str(np.round(100.0 * verses_reviewed / verses_count, 2))
    return f" {verses_reviewed}/ {verses_count} verses; {pct}% done  "


def select(idx):
    print("idx",idx)
    val = data.loc[idx, "selected"]
    print("val",val)
    data.loc[idx, "selected"] = 1 if val == 0 else 0

    acte = data.loc[idx].acte
    scene = data.loc[idx].scene
    filename = f"./textes/review/{play_title}_reviewed_{str(acte).zfill(2)}_{str(scene).zfill(2)}.json"
    # data.sort_values(
    #     by=["acte", "scene", "verse_id", "version", "selected", "tokens", "experiment", "chunk"],
    #     ascending = [True, True, True, True, False, True, True, True],
    #     inplace=True
    # )
    with open(filename, "w", encoding="utf-8") as f:
        data[(data.acte == acte) & (data.scene == scene)].to_json(f, force_ascii=False, orient="records", indent=4)


def add_text(verse_id, acte, scene, char):
    text = st.session_state[f"{verse_id}_text_key"].strip()
    new_item = {
        "experiment": "mmlman",
        "acte": acte,
        "scene": scene,
        "version": "modern",
        "chunk": 0,
        verse_col: verse_id,
        "tokens": count_tokens(text),
        "char": char,
        "text": text,
        "selected": 1,
    }
    data.loc[data.shape[0] + 1] = new_item


    filename = f"./textes/review/{play_title}_reviewed_{str(acte).zfill(2)}_{str(scene).zfill(2)}.json"
    with open(filename, "w", encoding="utf-8") as f:
        data[(data.acte == acte) & (data.scene == scene)].to_json(f, force_ascii=False, orient="records", indent=4)



if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Moliere.love")

    query_params = st.experimental_get_query_params()

    acte  = int(query_params["acte"][0]) if "acte" in query_params else None
    scene = int(query_params["scene"][0]) if "scene" in query_params else None

    # by default load review file
    main_filename = f"./textes/review/{play_title}_review.json"
    data = pd.read_json(main_filename)
    acte_scene_cond = None

    if (acte is not None) & (scene is not None):
        acte_scene_cond = (data.acte == int(acte)) & (data.scene == int(scene))

        # load already reviewed file if it exists
        filename = f"./textes/review/{play_title}_reviewed_{str(acte).zfill(2)}_{str(scene).zfill(2)}.json"
        if os.path.exists(filename):
            data = pd.read_json(filename)
        else:
            data = data[acte_scene_cond].copy()
            filename = main_filename

    if acte_scene_cond is None:
        # TODO get list of acts and scenes from main file not already created review files
        files = glob.glob("./textes/review/*reviewed*.json")
        prev_acte = ""
        for file in files:
            acte = int(file.split("_")[2])
            scene = int(file.split("_")[3].split(".")[0])

            if acte != prev_acte:
                prev_acte = acte
                st.markdown(f"## Acte {acte}")
            df = pd.read_json(file)
            html_string = f"* <a href='/compare?acte={acte}&scene={scene}' target=_self>acte {acte}, scene {scene}</a> {progress(df)}"
            st.markdown(html_string, unsafe_allow_html=True)

    if acte_scene_cond is not None:
        st.subheader(f"working with: :red[{filename.split('/')[-1]}]")
        # subset = data[acte_scene_cond].copy()
        subset = data.copy()

        st.caption(progress(subset))

        # st.table(subset)


        verse_ids = sorted(subset[verse_col].unique())

        for verse_id in verse_ids:
            # col1, col2, col3, col4 = st.columns([1, 2, 5, 5])
            col1, col2, col3 = st.columns([1, 2, 12])
            verse_cond = subset[verse_col] == verse_id
            char = subset[verse_cond]["char"].unique()[0]
            # verse_id status
            with col1:
                if subset[(subset[verse_col] == verse_id) & (subset.selected == 1)].shape[0] < 1:
                    st.markdown(f"**:red[{verse_id}]**")
                elif subset[(subset[verse_col] == verse_id) & (subset.selected == 1)].shape[0] > 1:
                    st.markdown(f"**:orange[{verse_id}]**")
                else:
                    st.markdown(f"**:blue[{verse_id}]**")

            with col2:
                st.write(f"{char}")

            with col3:

                tmp = subset[verse_cond & (subset.version == "original")].to_dict(orient="records")
                idx = subset[verse_cond & (subset.version == "original")].index[0]

                subcol1, subcol2, subcol3 = st.columns([1, 8, 1])
                with subcol1:
                    st.checkbox(
                        str(idx),
                        value=subset.loc[idx].selected == 1,
                        on_change=select,
                        args=(idx,),
                    )
                with subcol2:
                    st.write(f":blue[{tmp[0]['text'] }]")
                with subcol3:
                    st.caption(f"{subset.loc[idx].tokens}")

                tmp = subset[verse_cond & (subset.version == "modern")].copy()
                tmp["idx"] = tmp.index

                for i, d in tmp.iterrows():
                    subcol1, subcol2, subcol3 = st.columns([1, 8, 1])
                    with subcol1:
                        st.checkbox(
                            str(d.idx),
                            value= d.selected == 1,
                            on_change=select,
                            args=(d.idx,),
                        )
                    with subcol2:
                        st.write(f":orange[{d.text}]")

                    with subcol3:
                        st.caption(f"{d.selected} idx:{d.idx}  {d.tokens} {d.experiment}:{d.chunk}")

                st.text_area(
                    "enter text",
                    on_change=add_text,
                    key=f"{verse_id}_text_key",
                    args=(verse_id, acte, scene, char),
                )
                # st.write(d.idx)
            st.divider()
