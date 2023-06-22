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


def progress(subset):
    verses_count = len(subset.verse_id.unique())
    verses_reviewed = len(subset[subset.selected == 1].verse_id.unique())
    pct = str(np.round(100.0 * verses_reviewed / verses_count, 2))
    return f" {verses_reviewed}/ {verses_count} verses; {pct}% done  "


def select(idx):
    val = data.loc[idx, "selected"]

    data.loc[idx, "selected"] = 1 if val == 0 else 0

    # filename = "./textes/review/medecin-malgre-lui_review.json"
    # with open(filename, "w", encoding="utf-8") as f:
    #     data.to_json(f, force_ascii=False,  orient="records", indent=4)
    # save to acte scene reviewed
    acte = data.loc[idx].acte
    scene = data.loc[idx].scene
    filename = f"./textes/review/medecin-malgre-lui_reviewed_{str(acte).zfill(2)}_{str(scene).zfill(2)}.json"
    with open(filename, "w", encoding="utf-8") as f:
        data[(data.acte == acte) & (data.scene == scene)].to_json(
            f, force_ascii=False, orient="records", indent=4
        )


def add_text(verse_id, acte, scene, char):
    print("--", verse_id)
    print("--", st.session_state[f"{verse_id}_text_key"])

    new_item = {
        "experiment": "mml_manual",
        "acte": acte,
        "scene": scene,
        "version": "modern",
        "chunk": 0,
        "verse_id": verse_id,
        "char": char,
        "text": st.session_state[f"{verse_id}_text_key"],
        "selected": 1,
    }
    print("new_item:", new_item)
    data.loc[data.shape[0] + 1] = new_item
    data.sort_values(
        by=["acte", "scene", "verse_id", "version", "experiment", "chunk"], inplace=True
    )
    # data.reset_index(inplace = True, drop= True)

    data["text"] = data.text.apply(lambda txt: txt.strip())

    # data.to_csv("./textes/medecin-malgre-lui_modernized.csv", quoting  = csv.QUOTE_ALL, index = False)
    filename = "./textes/review/medecin-malgre-lui_review.json"
    with open(filename, "w", encoding="utf-8") as f:
        data.to_json(f, force_ascii=False, orient="records", indent=4)
    # save to acte scene reviewed
    filename = f"./textes/review/medecin-malgre-lui_reviewed_{str(acte).zfill(2)}_{str(scene).zfill(2)}.json"
    with open(filename, "w", encoding="utf-8") as f:
        data[(data.acte == acte) & (data.scene == scene)].to_json(
            f, force_ascii=False, orient="records", indent=4
        )

    # data[(data.acte == acte) & (data.scene == scene)].to_csv(filename, quoting  = csv.QUOTE_ALL, index = False)


if __name__ == "__main__":
    st.set_page_config(layout="wide", page_title="Moliere.love")

    query_params = st.experimental_get_query_params()

    acte = int(query_params["acte"][0]) if "acte" in query_params else None
    scene = int(query_params["scene"][0]) if "scene" in query_params else None

    if (acte is not None) & (scene is not None):
        # load already reviewed file
        filename = f"./textes/review/medecin-malgre-lui_reviewed_{str(acte).zfill(2)}_{str(scene).zfill(2)}.json"
        if not os.path.exists(filename):
            filename = f"./textes/review/medecin-malgre-lui_review.json"
        data = pd.read_json(filename)
        acte_scene_cond = (data.acte == acte) & (data.scene == scene)

    else:
        filename = f"./textes/review/medecin-malgre-lui_review.json"
        data = pd.read_json(filename)
        acte_scene_cond = None

    if acte_scene_cond is None:
        files = glob.glob("./textes/review/*reviewed*.json")
        prev_acte = ""
        for file in files:
            acte = int(file.split("_")[2])
            scene = int(file.split("_")[3].split(".")[0])
            # todo: add pct progress per file
            if acte != prev_acte:
                prev_acte = acte
                st.markdown(f"## Acte {acte}")
            df = pd.read_json(file)
            # st.markdown(f"* [acte {acte}, scene {scene}](/compare?acte={acte}&scene={scene}) {progress(df)}", unsafe_allow_html = True)
            html_string = f"* <a href='/compare?acte={acte}&scene={scene}' target=_self>acte {acte}, scene {scene}</a> {progress(df)}"
            st.markdown(html_string, unsafe_allow_html=True)

    if acte_scene_cond is not None:
        st.subheader(f"working with: :red[{filename.split('/')[-1]}]")
        subset = data[acte_scene_cond].copy()
        print("subset.shape", subset.shape)
        st.caption(progress(subset))

        verse_ids = sorted(subset.verse_id.unique())

        for verse_id in verse_ids:
            col1, col2, col3, col4 = st.columns([1, 1, 5, 5])
            verse_cond = subset.verse_id == verse_id
            char = subset[verse_cond]["char"].unique()[0]

            with col1:
                if (
                    subset[
                        (subset.verse_id == verse_id) & (subset.selected == 1)
                    ].shape[0]
                    < 1
                ):
                    st.markdown(f"**:red[{verse_id}]**")
                elif (
                    subset[
                        (subset.verse_id == verse_id) & (subset.selected == 1)
                    ].shape[0]
                    > 1
                ):
                    st.markdown(f"**:orange[{verse_id}]**")
                else:
                    st.markdown(f"**:blue[{verse_id}]**")

            with col2:
                st.write(f"{char}")

            with col3:
                tmp = subset[verse_cond & (subset.version == "original")].to_dict(
                    orient="records"
                )
                idx = subset[verse_cond & (subset.version == "original")].index[0]
                print(idx)

                subcol1, subcol2 = st.columns([5, 1])
                with subcol1:
                    st.write(f":blue[{tmp[0]['text'] }]")
                with subcol2:
                    st.checkbox(
                        str(idx),
                        value=subset.loc[idx].selected == 1,
                        on_change=select,
                        args=(idx,),
                    )

            with col4:
                tmp = subset[verse_cond & (subset.version == "modern")].copy()
                tmp["idx"] = tmp.index

                for i, d in tmp.iterrows():
                    subcol1, subcol2 = st.columns([5, 1])
                    with subcol1:
                        st.write(f":orange[{d.text}]")

                    with subcol2:
                        st.checkbox(
                            str(d.idx),
                            value=d.selected == 1,
                            on_change=select,
                            args=(d.idx,),
                        )

                st.text_area(
                    "enter text",
                    on_change=add_text,
                    key=f"{verse_id}_text_key",
                    args=(verse_id, acte, scene, char),
                )
                # st.write(d.idx)
            st.divider()
