import streamlit as st
from app.db import get_data, insert_data
from app.config import APP_NAME

st.title(APP_NAME)

# Exemple simple d’interface utilisateur
st.sidebar.header("Menu")
choice = st.sidebar.selectbox("Sélectionnez une option", ["Voir les données", "Ajouter des données"])

if choice == "Voir les données":
    data = get_data()
    st.write(data)
elif choice == "Ajouter des données":
    new_data = st.text_input("Entrez des informations")
    if st.button("Soumettre"):
        insert_data(new_data)
        st.success("Données ajoutées avec succès !")