import streamlit as st

# import importlib
# import traceback
import os

# import platform
import glob

st.set_page_config(
    page_title="Moliere.love",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="auto",
    menu_items={"About": "Le site de Molière en français moderne"}
)
# st.set_page_config(, page_title="Moliere.love")


def main():
    st.experimental_set_query_params()

    home_page()


def home_page():
    st.title("Molière.love")
    st.markdown("Bienvenue sur [Molière.love](./), le site qui donne un coup de frais à Molière!")
    st.write("Qui n'adore pas Molière!!! Hein?*")
    st.write("Oh Molière firmament de la culture française, alpha et oméga des arts du divertissement. Parangon du savoir-écrire, éphèbe de l'humour et du tendre! Startupeur vérulent de la critique sociale!. ok, ok ...")
    # st.write()
    st.write("Molière c'est très sympa, surtout quand on voit ses pièces jouées sur scène par des bons acteurs.",
    " \n",
    "Mais, en classe c'est pas toujours la joie.",
    " \n",
    "Le français est peut être la langue de Molière, mais depuis 400 ans, le français a bien évolué.",
    " \n",
    "Il était temps de rafraîchir Molière!"
    )

    st.write(
        "Que neni, nonobstant et foutre de Dieu, voici [Molière.love](http://moliere.love), le site où tu trouveras, jeune collégien, collégienne , lycéen, lycéenne, jeune esthèthe féru d'art et de beauté:"
    )
    st.subheader(":red[**La traduction des pièces de Molière en français moderne!!!**]")
    st.write("A commencer par:")
    st.markdown("- [Le mèdecin malgré lui](./Médecin_Malgrè_Lui)")

    st.divider()
    st.caption("(*) en fait, amis, on ne te demande pas ton avis. Molière est au programme depuis Charlemagne et du Molière tu vas en bouffer tous les ans!. ")

if __name__ == "__main__":
    main()
