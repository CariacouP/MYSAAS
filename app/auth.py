import requests
import urllib.parse
from supabase import create_client, Client
from config import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, SUPABASE_URL, SUPABASE_KEY
import streamlit as st

# Initialiser le client Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Génère l'URL de connexion pour Auth0
def generate_auth0_login_url():
    auth_url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "client_id": AUTH0_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": "http://localhost:8501/callback",
        "scope": "openid profile email"
    }
    return f"{auth_url}?{urllib.parse.urlencode(params)}"

# Processus d'authentification via le callback Auth0
def process_auth0_callback(code):
    # Échange le code pour obtenir un token d'accès
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    token_data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": "http://localhost:8501/callback"
    }
    token_response = requests.post(token_url, json=token_data).json()
    
    # Vérifie si le token d'accès a été reçu
    if 'access_token' in token_response:
        headers = {'Authorization': f"Bearer {token_response['access_token']}"}
        
        # Récupère les informations utilisateur
        userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
        userinfo_response = requests.get(userinfo_url, headers=headers).json()
        
        # Appelle la fonction pour enregistrer l'utilisateur dans Supabase
        store_user_in_supabase(userinfo_response)
    else:
        # Affiche un message d'erreur en cas d'échec
        st.error("Échec de l'obtention du token d'accès. Vérifiez vos paramètres Auth0.")
        st.write("Réponse d'erreur Auth0:", token_response)  # Affiche la réponse pour le débogage

# Enregistrement de l'utilisateur dans Supabase
def store_user_in_supabase(user_info):
    user_id = user_info["sub"]
    email = user_info["email"]
    name = user_info.get("name", "")

    # Vérifie si l'utilisateur existe déjà
    existing_user = supabase.table("users").select("*").eq("user_id", user_id).execute()
    
    if not existing_user.data:
        # Insère un nouvel utilisateur
        supabase.table("utilisateurs").insert({
            "user_id": user_id,
            "email": email,
            "name": name
        }).execute()
    else:
        st.write("Utilisateur déjà inscrit.")