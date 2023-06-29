import streamlit as st

# import importlib
# import traceback
import os

# import platform
import glob


def main():
    st.experimental_set_query_params()

    home_page()


def home_page():
    st.title(":orange[Molière.love]")
    st.header(":violet[Le théâtre de Molière en français moderne.]")

    st.write("Qui n'adore pas Molière? Hein?*")
    st.write("Oh Molière firmament de la culture française :flag-fr:, alpha et oméga des arts :art: du divertissement :performing_arts:. Parangon du savoir-écrire, éphèbe de l'humour et du tendre! Startupeur vérulent de la critique sociale!. ok, ok ...")
    # st.write()
    st.write("Molière c'est très sympa, surtout en live au théâtre.",
    # " \n",
    "Mais, en classe c'est pas toujours folichon :scream_cat:",
    " \n",
    "Le français est peut être la langue de Molière, mais depuis 400 ans, le français a bien évolué.",
    " \n",
    )
    st.markdown("**Il était temps de rafraîchir Molière!**")

    st.markdown("""Voici donc :drum_with_drumsticks:
        <a href="./" target = "_self">
            Moliere.love
        </a> :drum_with_drumsticks: le site où tu trouveras, jeune collégien  :male_elf:, collégienne  :female_elf:, lycéen :man_in_lotus_position:, lycéenne :woman_in_lotus_position:, jeune esthèthe féru d'art et de beauté:""",
        unsafe_allow_html=True
    )


    st.subheader(":red[**La traduction des pièces de Molière en français moderne!!!**]")
    st.write("A commencer par:")
    st.markdown("""
    <ul><li>
        <a href="./Médecin_Malgrè_Lui" target = "_self">
            Le mèdecin malgré lui
        </a>
    </li></ul>""",
        unsafe_allow_html=True
    )
    # st.markdown("- [Le mèdecin malgré lui](./Médecin_Malgrè_Lui)")

    st.divider()
    st.caption("(*) en fait, amis, on ne te demande pas ton avis. Molière est au programme depuis Charlemagne et du Molière tu vas en bouffer tous les ans!. ")

if __name__ == "__main__":

    st.set_page_config(
        page_title="Moliere.love: Molière en français moderne.",
        page_icon=None,
        layout="centered",
        initial_sidebar_state="auto",
        menu_items={"About": "Le site de Molière en français moderne"}
    )
    css_file = os.path.join(os.getcwd(), "streamlit/pages/style.css")

    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    main()
