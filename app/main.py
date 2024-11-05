import streamlit as st
from db import get_data, insert_data
from config import APP_NAME
from auth import generate_auth0_login_url, process_auth0_callback

st.title(APP_NAME)

# Interface Streamlit
query_params = st.query_params  # Utilisation de st.query_params pour récupérer les paramètres de l'URL

if "callback" in query_params:
    # Récupère le code de redirection et appelle la fonction de callback
    code = query_params["callback"][0]
    process_auth0_callback(code)
else:
    # Affiche un bouton de connexion
    st.write("Bienvenue ! Connectez-vous pour continuer.")
    if st.button("Se connecter avec Auth0"):
        auth_url = generate_auth0_login_url()
        # Redirection explicite avec le paramètre `callback` dans l’URL
        st.write(f'<meta http-equiv="refresh" content="0; url=/?callback=auth0_redirect">', unsafe_allow_html=True)