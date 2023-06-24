import streamlit as st

import json
import pandas as pd
import os, glob

TEXTES_PATH = "../textes/review/*acte_*.json"

def gray(gray_text, text):
    return f" <span style='color:gray'>{gray_text}</span> <span style='color:lightgray'>{text}</span>"

def filename_to_scene(filename):
    if "reviewed" in filename:
        return filename.split("_")[3]

def filename_to_acte(filename):
    if "reviewed" in filename:
        return filename.split("_")[2]

def load_textes(menu_choice):
    print("files: ", files)
    return pd.read_json(files[menu_choice]).to_dict(orient="records")

def main(file):
    st.set_page_config(layout="wide", page_title="Moliere.love")

    df = pd.read_json(file)

    with st.sidebar:
        options_acte = [str(acte) for acte in df.acte.unique()]
        acte_choice = st.selectbox("Choisi l'acte:", options_acte)

        options_scene = [str(scene) for scene in df[df.acte == int(acte_choice)].scene.unique()]
        scene_choice = st.selectbox("Choisi la scene:", options_scene)


    st.header("Le Médecin Malgré Lui")
    st.subheader(f"Acte {acte_choice}, Scène {scene_choice}")
    st.caption(
        """
        Sganarelle, un faiseur de fagots, se querelle avec sa femme Martine, qui lui reproche sa conduite. Il finit par la frapper (scène 1). Un voisin, M. Robert, s'interpose, mais il se fait battre par le couple (scène 2). Martine décide de se venger (scène 3). Deux domestiques de Géronte, Valère et Lucas, cherchent un médecin capable de guérir la fille de leur maître, devenue muette. Martine fait croire aux deux hommes que Sganarelle est un médecin prodigieux mais fantasque, qu'il faut rouer de coups afin de lui faire avouer sa profession (scène 4). Le plan conçu par Martine fonctionne : Valère et Lucas transforment le fagotier en médecin, à grands coups de bâton (scène 5).
    """
    )

    data = df[(df.acte == int(acte_choice)) & (df.scene == int(scene_choice))].copy()
    st.write(f"{data.shape[0]} repliques")
    for i, d in data.iterrows():
        col1, col2, col3, col4 = st.columns([1, 3, 10, 8])
        with col1:
            st.write(d.verse_id)
        with col2:
            st.write(d.char)
        with col3:
            if d.selection == 'original':
                st.markdown(f"{d.modern}")
            else:
                st.markdown(f"_{d.modern}_")
        with col4:
            st.caption(f"{d.text}")




if __name__ == "__main__":

    file_path = os.path.join(os.getcwd(), 'streamlit','*display*.json')
    file = glob.glob(file_path)[0]
    print(f"loaded {file} from {file_path}")

    main(file)
