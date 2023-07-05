import streamlit as st
from PIL import Image

import json
import pandas as pd
import os, glob


dict_actes = {0:'Acte I',1:'Acte II',2:'Acte III'}
dict_scenes = {
    'Acte I':[f"Scène {k}" for k in range (1,6)],
    'Acte II':[f"Scène {k}" for k in range (1,6)],
    'Acte III':[f"Scène {k}" for k in range (1,12)]
}

actes_to_int = {'Acte I':1,'Acte II':2,'Acte III':3}
scenes_to_int = lambda x:  int(x.split(' ')[1])

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


def write_character(char):
    if (len(char.split(' ')) > 1) & (char != "M. ROBERT"):
        str_char = f"**{char.split(' ')[0]}** _{' '.join(char.split(' ')[1:])}_"
    else:
        str_char = f"**{char}**"
    return str_char

def main(file):


    df = pd.read_json(file)

    query_acte = get_query()

    with st.sidebar:

        acte_choice = st.selectbox("Choisis l'acte:", dict_actes.values(), key = 'menu_acte', on_change = reset_query, label_visibility = "collapsed")
        scene_options = dict_scenes[acte_choice]
        scene_choice = st.selectbox("Choisis la scène:", scene_options, key = 'menu_scene' ,on_change = reset_query, label_visibility = "collapsed")
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

    current_acte = int(actes_to_int[acte_choice])
    current_scene = scenes_to_int(scene_choice)
    # current_scene = int(scene_choice)
    link_previous, link_next = previous_next_link(df, current_acte, current_scene)
    data = df[(df.acte == current_acte) & (df.scene == current_scene)].copy()

    # header
    col1, col2, col3 = st.columns([14, 2, 8])
    with col1:
        st.header("Le Médecin Malgré Lui")
        st.subheader(f"{acte_choice}, {scene_choice}")

    with col3:
        # image = Image.open('./streamlit/img/sganarelle_wide_head.png')
        image = None
        if current_acte == 1:
            if current_scene == 1:
                image = Image.open('./streamlit/img/alexis808_17th_century_faggot_maker_brandishes_a_stick_poor_woo_f1bdfb90-6ed0-4cfa-9ad5-231e826be9ac.png')
            elif current_scene == 2:
                image = Image.open('./streamlit/img/alexis808_17th_century_peasant_surprised_stupid_poor_wood_works_e6ea7218-ddd5-4439-98fe-f1618d9a9c54.png')
            elif current_scene == 3:
                image = Image.open('./streamlit/img/alexis808_17th_century_walking_housewife_looks_to_the_left_of_t_6e0dc49f-94e7-49e5-8ceb-0404e55a720e.png')

        if image is not None:
            st.image(image, width = 300)


    st.markdown(f"**{list_characters(data)}** ")
    st.caption(f"{data.shape[0]} répliques")

    tab1, tab2, tab3 = st.tabs([" :page_facing_up: + :scroll: Côte à Côte ", " :page_facing_up: Version Moderne ", " :scroll: Version Original "])

    with tab1:
        col1, col2, col3, col4, col5 = st.columns([1, 12, 1, 10, 4])
        with col2:
            st.subheader(":page_facing_up: Texte modernisé")
        with col4:
            st.subheader(":scroll: Texte original")


        for i, d in data.iterrows():

            col1, col2, col3, col4 = st.columns([1, 12, 1, 10])
            with col1:
                st.write(d.verse_id)
            with col2:
                str_char = write_character(d.char)
                st.write(
                    f"{str_char}",
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
                str_char = write_character(d.char)
                st.write(
                    f"{str_char}",
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
                str_char = write_character(d.char)
                st.write(
                    f"{str_char}",
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
