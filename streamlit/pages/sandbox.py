import streamlit as st

import json
import pandas as pd
import os, glob

list_actes = [1,2,3]
list_scenes = {
    1: [1,2,3],
    2: [1,2,3],
    3: [1,2,3,4,5]
}

def reset_query():
    st.experimental_set_query_params()

def get_query(list_scenes):
    query = st.experimental_get_query_params()
    query_acte = 0
    query_scene = 0
    if query:
        if 'acte' in query.keys():
            query_acte = int(query['acte'][0]) -1
        if 'scene' in query.keys():
            query_scene = int(query['scene'][0]) -1
        if query_acte:
            if query_scene not in list_scenes[query_acte]:
                print(f"[OOB] query_acte: {query_acte} query_scene: {query_scene}")
                query_scene = list_scenes[query_acte][0]-1
    else:
        st.write(f"st.session_state:")
        st.write(st.session_state)
        query_acte = int(st.session_state.menu_acte) -1
        query_scene = int(st.session_state.menu_scene) -1
        if query_scene not in list_scenes[query_acte]:
            print(f"[OOB] query_acte: {query_acte} query_scene: {query_scene}")
            query_scene = list_scenes[int(st.session_state.menu_acte)][0]-1


    return query_acte, query_scene

def sidebar(query_acte, query_scene):
    with st.sidebar:
        options_acte = [str(acte) for acte in list_actes]
        acte_choice = st.selectbox("Choisi l'acte:", options_acte, key = 'menu_acte', index = query_acte, on_change = reset_query)
        options_scene = [str(scene) for scene in list_scenes[int(acte_choice)]]
        scene_choice = st.selectbox("Choisi la scene:", options_scene, key = 'menu_scene', index = query_scene, on_change = reset_query )
    return acte_choice, scene_choice


def main():
    # Init variables
    query_acte, query_scene = get_query(list_scenes)
    # acte_choice, scene_choice = sidebar(query_acte, query_scene)

    with st.sidebar:
        st.write(f"query_acte: {query_acte}")
        st.write(f"query_scene: {query_scene}")
        options_acte = [str(acte) for acte in list_actes]
        acte_choice = st.selectbox("Choisi l'acte:", options_acte, key = 'menu_acte', index = query_acte, on_change = reset_query)
        options_scene = [str(scene) for scene in list_scenes[int(acte_choice)]]
        scene_choice = st.selectbox("Choisi la scene:", options_scene, key = 'menu_scene', index = query_scene, on_change = reset_query )

    st.divider()

    st.subheader("[end main()]:")
    st.write(f"Acte: {acte_choice}")
    st.write(f"Scène: {scene_choice}")


if __name__ == "__main__":
    main()
