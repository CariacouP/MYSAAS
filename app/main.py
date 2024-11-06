import streamlit as st
from db import get_data, insert_data
from config import APP_NAME
from auth import generate_auth0_login_url, process_auth0_callback, is_authenticated
st.title(APP_NAME)

# Récupération des paramètres de l'URL pour vérifier la présence du code d'authentification
query_params = st.query_params

# Gestion de l'authentification avec Auth0
if "code" in query_params:
    # Auth0 a redirigé avec un code d'autorisation
    code = query_params["code"][0]  # Prend le premier élément s'il y a plusieurs codes
    process_auth0_callback(code)
elif not is_authenticated():
    # Utilisateur non authentifié
    st.write("Bienvenue ! Veuillez vous connecter pour continuer.")
    if st.button("Se connecter avec Auth0"):
        auth_url = generate_auth0_login_url()
        # Redirige vers la page de connexion Auth0
        st.write(f'<meta http-equiv="refresh" content="0; url={auth_url}">', unsafe_allow_html=True)
else:
    # Utilisateur authentifié, chargement de la page principale
    st.write("Vous êtes connecté ! Bienvenue dans l'application.")
   