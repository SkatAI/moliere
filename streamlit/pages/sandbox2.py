import streamlit as st

import json
import pandas as pd
import os, glob

dict_actes = {0:'A',1:'B',2:'C'}
dict_scenes = {'A':['a','b','c'],'B':['a','b','c'],'C':['a','b','c','d','e']}


def reset_query():
    st.experimental_set_query_params()

def get_query():
    query = st.experimental_get_query_params()
    query_acte = 0
    if query:
        if 'acte' in query.keys():
            query_acte = int(query['acte'][0]) -1
            st.session_state.menu_acte = dict_actes[query_acte]
            scene_options = dict_scenes[st.session_state.menu_acte]
            if 'scene' in query.keys():
                query_scene = int(query['scene'][0]) -1
                st.session_state.menu_scene = scene_options[query_scene]
            else:
                st.session_state.menu_scene = scene_options[0]
        else:
            st.session_state.menu_acte = dict_actes[0]

    return query_acte


def main():
    # Init variables
    query_acte = get_query()

    with st.sidebar:

        acte_choice = st.selectbox("Choisi l'acte:", dict_actes.values(), key = 'menu_acte', on_change = reset_query)
        scene_options = dict_scenes[acte_choice]
        scene_choice = st.selectbox("Choisi la scene:", scene_options, key = 'menu_scene' ,on_change = reset_query)

    st.divider()

    st.subheader("[end main()]:")
    st.write(f"Acte: {acte_choice}")
    st.write(f"Scene: {scene_choice}")


if __name__ == "__main__":
    main()

    st.markdown("- [/sandbox2](./sandbox2)")
    st.markdown("- [/sandbox2?acte=1](./sandbox2?acte=1)")
    st.markdown("- [/sandbox2?acte=2](./sandbox2?acte=2)")
    st.markdown("- [/sandbox2?acte=2&scene=1](./sandbox2?acte=2&scene=1)")
    st.markdown("- [/sandbox2?acte=2&scene=3](./sandbox2?acte=2&scene=3)")
    st.markdown("- [/sandbox2?acte=3](./sandbox2?acte=3)")
