import streamlit as st

import json
import pandas as pd
import glob

TEXTES_PATH = "./textes/**/*acte_*.json"


def gray(gray_text, text):
    return f" <span style='color:gray'>{gray_text}</span> <span style='color:lightgray'>{text}</span>"


def filename_to_scene(filename):
    if "acte_" in filename:
        tmp = filename.split("acte_")
        acte = tmp[1][:2]
        scene = tmp[1][9:11]
        tmp = filename.split("medecin-malgre-lui_")
        version = tmp[1][:2]
        return f"[{version}] Acte {acte}, Scène {scene}"


def load_textes(menu_choice):
    # files = glob.glob(TEXTES_PATH)
    print("files: ", files)
    return pd.read_json(files[menu_choice]).to_dict(orient="records")


def main(files):
    st.set_page_config(layout="wide", page_title="Moliere.love")

    # files = glob.glob(TEXTES_PATH)
    options = [filename_to_scene(file) for file in files]

    versions = sorted(set([file.split("medecin-malgre-lui_")[1][:2] for file in files]))

    query_params = st.experimental_get_query_params()
    if "choice" in query_params:
        choice = int(query_params["choice"][0])
    else:
        choice = 0

    with st.sidebar:
        experiment = st.selectbox("experiment", versions)
        print("experiment", experiment)
        file_path = f"./textes/mml{experiment}/*acte_*.json"
        print("file_path", file_path)
        experiment_files = glob.glob(f"./textes/mml{experiment}/*acte_*.json")
        print(experiment_files)
        options = [filename_to_scene(file) for file in experiment_files]
        # practices = data[“practice_name”].loc[data[“ICS”] == ics_choice]
        # practice_choice = st.sidebar.multiselect(“Select practices”, practices)
        st.divider()
        menu_choice = st.radio("Choisis la scène:", options, index=choice)
        if menu_choice:
            st.experimental_set_query_params(choice=options.index(menu_choice))
    if menu_choice:
        scene_page(menu_choice)
    else:
        st.write("choisi une scene a gauche")

    if choice & (choice > 0):
        st.markdown(f"<< [{options[choice -1]}](./scene?choice={choice-1})")
    if choice & (choice < len(options) - 1):
        st.markdown(f">> [{options[choice +1]}](./scene?choice={choice+1})")


def scene_page(menu_choice):
    query_params = st.experimental_get_query_params()
    if "choice" in query_params:
        choice = int(query_params["choice"][0])

    st.title("Le Médecin Malgré Lui")
    st.header(menu_choice.split(",")[0])
    st.caption(
        """
        Sganarelle, un faiseur de fagots, se querelle avec sa femme Martine, qui lui reproche sa conduite. Il finit par la frapper (scène 1). Un voisin, M. Robert, s'interpose, mais il se fait battre par le couple (scène 2). Martine décide de se venger (scène 3). Deux domestiques de Géronte, Valère et Lucas, cherchent un médecin capable de guérir la fille de leur maître, devenue muette. Martine fait croire aux deux hommes que Sganarelle est un médecin prodigieux mais fantasque, qu'il faut rouer de coups afin de lui faire avouer sa profession (scène 4). Le plan conçu par Martine fonctionne : Valère et Lucas transforment le fagotier en médecin, à grands coups de bâton (scène 5).
    """
    )
    st.subheader(menu_choice.split(",")[1])
    st.caption(
        """
        Sganarelle, un faiseur de fagots, se querelle avec sa femme Martine, qui lui reproche sa conduite. Il finit par la frapper.
    """
    )

    df = load_textes(int(choice))
    col1, col2 = st.columns(2)
    with col1:
        st.header("Texte Original")

    with col2:
        st.header("Version moderne")

    chunk_idx = 0
    for chunk in df:
        verses = chunk["text"]
        modern = chunk["modern"]
        # st.divider()

        col1, col2 = st.columns(2)

        max_ = int(chunk["verse_id_start"]) + int(chunk["verse_id_end"])
        max_ = int((int(chunk["verse_id_start"]) + int(chunk["verse_id_end"])) / 2)

        with col1:
            for verse_id, verse in verses.items():
                if (chunk_idx + 1 < len(df)) & (int(verse_id) >= max_):
                    break
                st.markdown(gray(verse_id, verse), unsafe_allow_html=True)

        with col2:
            for verse_id, verse in modern.items():
                if (chunk_idx + 1 < len(df)) & (int(verse_id) >= max_):
                    break
                st.write(f":orange[{verse_id}: {verse}]")

        chunk_idx += 1

    col1, col2 = st.columns(2)
    with col1:
        st.divider()

    with col2:
        st.divider()


if __name__ == "__main__":
    files = glob.glob(TEXTES_PATH)
    main(files)
