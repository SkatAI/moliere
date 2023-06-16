import streamlit as st
# import importlib
# import traceback
import os
# import platform
import glob


st.set_page_config(layout="wide", page_title="Moliere.love")
def main():
    st.experimental_set_query_params()

    home_page()

def home_page():
    st.title("Molière.love")
    st.markdown("Bienvenue sur [Molière.love](./), le site avec la traduction des pièces de Molière en langue moderne.")
    st.write("""Qui n'adore pas Molière!! Oh Molière firmament de la culture, alpha et oméga des arts du divertissement. Parangon du savoir-écrire, éphèbe de l'humour et du tendre
    Startupeur vérulent de la critique sociale!
    .""")
    st.write("Ok, ok, bon Molière c'est sympa, surtout quand on voit la pièce jouée sur scène par des bons acteurs. ")
    st.write("Mais Molière, en classe c'est plutôt galère. Et faut bien le dire souvent incompréhensible. ")


    st.write("Que neni, nonobstant et foutre de Dieu, C'est pourquoi j'ai crée Molière.love où tu trouveras jeune collégiens en culote courte ...")
    st.markdown(":red[**La traduction des pièces de Molière en français moderne!!!**]")
    st.write("A commencer par:")
    st.markdown(":blue[ - Le mèdecin malgré lui]")

    st.write("Le français est peut être la langue de Molière, mais depuis 400 ans, le français a bien évolué. Il était temps de rafraîchir Molière!")




if __name__ == "__main__":
    main()
