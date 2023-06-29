import streamlit as st

import json
import pandas as pd
import os, glob


dict_actes = {0:'I',1:'II',2:'III'}
dict_scenes = {'I':[1,2,3,4,5],'II':[1,2,3,4,5],'III':[1,2,3,4,5,6,7,8,9,10,11]}

actes_to_int = {'I':1,'II':2,'III':3}

def reset_query():
    st.experimental_set_query_params()

def list_characters(data):
    characters = [char.split(' ')[0].replace(',','') for char in data.char.unique()]
    characters = ', '.join(list(set(characters)))
    return characters

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

def previous_next_link(df, acte, scene):
    items = [ (pair[0], pair[1])    for pair in df[['acte', 'scene']].drop_duplicates().values]

    current = items.index((acte,scene))
    if current > 0:
        previous = items[current -1]
        link_previous = f"""<a
                href="?acte={previous[0]}&scene={previous[1]}"
                target = "_self"
                class = "previous_arrow"
                title = "Médecin malgré lui, acte {previous[0]}, scène {previous[1]}"
            > :arrow_backward: :arrow_backward: </a>"""
    else:
        link_previous = ""

    if current < len(items):
        next = items[current + 1]
        link_next = f"""<a
                href="?acte={next[0]}&scene={next[1]}"
                target = "_self"
                class = "next_arrow"
                title = "Médecin malgré lui, acte {next[0]}, scène {next[1]}"
            > :arrow_forward: :arrow_forward: </a>"""
    else:
        link_next = ""

    return link_previous, link_next


def main(file):


    df = pd.read_json(file)

    query_acte = get_query()

    with st.sidebar:

        acte_choice = st.selectbox("Choisis l'acte:", dict_actes.values(), key = 'menu_acte', on_change = reset_query)
        scene_options = dict_scenes[acte_choice]
        scene_choice = st.selectbox("Choisis la scène:", scene_options, key = 'menu_scene' ,on_change = reset_query)
        st.write(" \n")
        st.write(" \n")
        st.write(" \n")
        with st.expander("Liste des personnages:"):
            st.caption(
"""
- SGANARELLE, mari de Martine.
- MARTINE, femme de Sganarelle.
- M. ROBERT, voisin de Sganarelle.
- VALÈRE, domestique de Géronte.
- LUCAS, mari de Jacqueline.
- GÉRONTE, père de Lucinde.
- JACQUELINE, nourrice chez Géronte, et femme de Lucas.
- LUCINDE, fille de Géronte.
- LÉANDRE, amant de Lucinde.
- THIBAUT, père de Perrin, paysan.
- PERRIN, fils de Thibaut, paysan.
"""
            )


    st.header("Le Médecin Malgré Lui")
    st.subheader(f"Acte {acte_choice}, Scène {scene_choice}")
    # st.caption(
    #     """Insert resume de la scene"""
    # )
    # link_previous, link_next = previous_next_link(df, int(actes_to_int[acte_choice]), int(scene_choice))
    current_acte = int(actes_to_int[acte_choice])
    current_scene = int(scene_choice)
    link_previous, link_next = previous_next_link(df, current_acte, current_scene)
    data = df[(df.acte == int(actes_to_int[acte_choice])) & (df.scene == int(scene_choice))].copy()
    st.markdown(f"**{list_characters(data)}** ")
    st.caption(f"{data.shape[0]} répliques")

    tab1, tab2, tab3 = st.tabs([" :page_facing_up: + :scroll: Côte à Côte ", " :page_facing_up: Version Moderne ", " :scroll: Version Original "])

    with tab1:
        col1, col2, col3, col4 = st.columns([1, 12, 1, 10])
        with col2:
            st.subheader(":page_facing_up: Texte modernisé")
        with col4:
            st.subheader(":scroll: Texte original")

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
        st.subheader(":page_facing_up: Texte modernisé")

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
        st.subheader(":scroll: Texte original")

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


    st.divider()
    col1, col2, col3 = st.columns([1,  10, 1 ])
    with col1:
        st.markdown(link_previous, unsafe_allow_html=True )

    with col3:
        st.markdown(link_next, unsafe_allow_html=True )


if __name__ == "__main__":

    st.set_page_config(
        page_title="Moliere.love: Le Médecin Malgré Lui en français moderne.",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="auto",
        menu_items={"About": "Le site de Molière en français moderne"}
    )

    css_file = os.path.join(os.getcwd(), "streamlit/pages/style.css")
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


    file_path = os.path.join(os.getcwd(), 'streamlit/content','*display*.json')
    file = glob.glob(file_path)[0]
    print(f"loaded {file} from {file_path}")

    main(file)
