import streamlit as st

import json
import pandas as pd
import os, glob

def load_textes(menu_choice):
    return pd.read_json(files[menu_choice]).to_dict(orient="records")

def main(file):
    st.set_page_config(
        page_title="Moliere.love",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={"About": "Le site de Molière en français moderne"}
    )

    df = pd.read_json(file)

    with st.sidebar:
        options_acte = [str(acte) for acte in df.acte.unique()]
        acte_choice = st.selectbox("Choisi l'acte:", options_acte)

        options_scene = [str(scene) for scene in df[df.acte == int(acte_choice)].scene.unique()]
        scene_choice = st.selectbox("Choisi la scene:", options_scene)


    st.header("Le Médecin Malgré Lui")
    st.subheader(f"Acte {acte_choice}, Scène {scene_choice}")
    st.caption(
        """Insert resume de la scene"""
    )

    data = df[(df.acte == int(acte_choice)) & (df.scene == int(scene_choice))].copy()
    st.write(f"{data.shape[0]} repliques")
    for i, d in data.iterrows():
        col1, col2, col3, col4 = st.columns([1, 2, 10, 8])
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

    file_path = os.path.join(os.getcwd(), 'streamlit/content','*display*.json')
    file = glob.glob(file_path)[0]
    print(f"loaded {file} from {file_path}")

    main(file)
