import streamlit as st

import json
import pandas as pd
import os, glob


dict_actes = {0:'I',1:'II',2:'III'}
dict_scenes = {'I':[1,2,3,4,5],'II':[1,2,3,4,5],'III':[1,2,3,4,5,6,7,8,9,10,11]}

actes_to_int = {'I':1,'II':2,'III':3}

def reset_query():
    st.experimental_set_query_params()

def get_query():
    query = st.experimental_get_query_params()
    query_acte = 0
    if query:
        if 'acte' in query.keys():
            query_acte = int(query['acte'][0]) -1
            try:
                st.session_state.menu_acte = dict_actes[query_acte]
            except:
                st.session_state.menu_acte = dict_actes[0]
                reset_query()
            scene_options = dict_scenes[st.session_state.menu_acte]
            if 'scene' in query.keys():
                query_scene = int(query['scene'][0]) -1
                try:
                    st.session_state.menu_scene = scene_options[query_scene]
                except:
                    st.session_state.menu_scene = scene_options[0]
                    reset_query()
            else:
                st.session_state.menu_scene = scene_options[0]
        else:
            st.session_state.menu_acte = dict_actes[0]

    return query_acte


def main(file):
    st.set_page_config(
        page_title="Moliere.love",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={"About": "Le site de Molière en français moderne"}
    )

    # st.markdown('''
    # <style>
    # .stApp [data-testid="stToolbar"]{
    #     display:none;
    # }
    # </style>
    # ''', unsafe_allow_html=True)

    hide_menu_style = """
            <style>
            #MainMenu {visibility: hidden;}
            </style>
            """
    st.markdown(hide_menu_style, unsafe_allow_html=True)


    df = pd.read_json(file)

    query_acte = get_query()

    with st.sidebar:

        acte_choice = st.selectbox("Choisi l'acte:", dict_actes.values(), key = 'menu_acte', on_change = reset_query)
        scene_options = dict_scenes[acte_choice]
        scene_choice = st.selectbox("Choisi la scène:", scene_options, key = 'menu_scene' ,on_change = reset_query)

    st.header("Le Médecin Malgré Lui")
    st.subheader(f"Acte {acte_choice}, Scène {scene_choice}")
    st.caption(
        """Insert resume de la scene"""
    )

    data = df[(df.acte == int(actes_to_int[acte_choice])) & (df.scene == int(scene_choice))].copy()
    st.write(f"{data.shape[0]} repliques")

    tab1, tab2, tab3 = st.tabs([":open_book: Côte à Côte", ":memo: Version Moderne", ":scroll: Version Original"])

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
