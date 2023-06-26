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

    # ----
    def form_callback():
        st.write(f"scene_choice {scene_choice} st.session_state.menu_scene {st.session_state.menu_scene}")

    # ----
    try:
        acte_choice
    except NameError:
        acte_choice = 1


    with st.sidebar:


        with st.form(key='my_form'):
            options_acte = [str(acte) for acte in df.acte.unique()]
            acte_choice = st.selectbox("Choisi l'acte:", options_acte)
            options_scene = [str(scene) for scene in df[df.acte == int(acte_choice)].scene.unique()]
            scene_choice = st.selectbox("Choisi la scene:", options_scene, key = 'menu_scene' )
            submit_button = st.form_submit_button(label=':partying_face:', on_click=form_callback)


    st.header("Le Médecin Malgré Lui")
    st.subheader(f"Acte {acte_choice}, Scène {scene_choice}")
    st.caption(
        """Insert resume de la scene"""
    )
    st.divider()
    st.write(st.session_state)
    st.write(scene_choice)
    st.divider()

    data = df[(df.acte == int(acte_choice)) & (df.scene == int(scene_choice))].copy()
    st.write(f"{data.shape[0]} repliques")

    tab1, tab2, tab3 = st.tabs(["Complet", "Moderne", "Original"])

    with tab1:
        col1, col2, col3, col4 = st.columns([1, 12, 1, 10])
        with col2:
            st.subheader("Texte modernisé")
        with col4:
            st.subheader("Texte original")

        for i, d in data.iterrows():

            col1, col2, col3, col4 = st.columns([1, 12, 1, 10])
            with col1:
                st.write(d.verse_id)
            with col2:
                st.write(
                    f"{d.char}",
                    " \n",
                    f"{d.modern}"
                )

            with col4:
                st.write(" \n")
                st.caption(f"_{d.text}_")

    with tab2:
        st.subheader("Texte modernisé")

        for i, d in data.iterrows():

            col1, col2, col3, col4 = st.columns([1, 16, 1, 6])
            with col1:
                st.write(d.verse_id)
            with col2:
                st.write(
                    f"{d.char}",
                    " \n",
                    f"{d.modern}"
                )

    with tab3:
        st.subheader("Texte original")

        for i, d in data.iterrows():

            col1, col2, col3, col4 = st.columns([1, 16, 1, 6])
            with col1:
                st.write(d.verse_id)
            with col2:
                st.write(
                    f"{d.char}",
                    " \n",
                    f"{d.text}"
                )



if __name__ == "__main__":

    file_path = os.path.join(os.getcwd(), 'streamlit/content','*display*.json')
    file = glob.glob(file_path)[0]
    print(f"loaded {file} from {file_path}")

    main(file)
