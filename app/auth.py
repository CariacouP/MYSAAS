import requests
import urllib.parse
from supabase import create_client, Client
from config import AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, SUPABASE_URL, SUPABASE_KEY
import streamlit as st

# Initialize the Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Generate the Auth0 login URL
def generate_auth0_login_url():
    auth_url = f"https://{AUTH0_DOMAIN}/authorize"
    params = {
        "client_id": AUTH0_CLIENT_ID,
        "response_type": "token",
        "redirect_uri": "http://localhost:8501",
        "scope": "openid profile email"
    }
    return f"{auth_url}?{urllib.parse.urlencode(params)}"

# Process the Auth0 callback
def process_auth0_callback(code):
    # Exchange the code for an access token
    token_url = f"https://{AUTH0_DOMAIN}/oauth/token"
    token_data = {
        "grant_type": "authorization_code",
        "client_id": AUTH0_CLIENT_ID,
        "client_secret": AUTH0_CLIENT_SECRET,
        "code": code,
        "redirect_uri": "http://localhost:8501"
    }
    token_response = requests.post(token_url, json=token_data).json()
    
    # Check if the access token was received
    if 'access_token' in token_response:
        headers = {'Authorization': f"Bearer {token_response['access_token']}"}
        
        # Get user information
        userinfo_url = f"https://{AUTH0_DOMAIN}/userinfo"
        userinfo_response = requests.get(userinfo_url, headers=headers).json()
        
        # Store user session state
        st.session_state['user'] = userinfo_response  # Save user info
        st.session_state['is_authenticated'] = True   # Mark as authenticated

        # Call the function to store the user in Supabase
        store_user_in_supabase(userinfo_response)
    else:
        # Display an error message in case of failure
        st.error("Failed to obtain access token. Check your Auth0 settings.")
        st.write("Auth0 error response:", token_response)  # Display response for debugging

# Store the user in Supabase
def store_user_in_supabase(user_info):
    user_id = user_info["sub"]
    email = user_info["email"]
    name = user_info.get("name", "")

    # Check if the user already exists
    existing_user = supabase.table("users").select("*").eq("user_id", user_id).execute()
    
    if not existing_user.data:
        # Insert a new user
        supabase.table("users").insert({
            "user_id": user_id,
            "email": email,
            "name": name
        }).execute()
    else:
        st.write("User already registered.")

# Check if the user is authenticated
def is_authenticated():
    # Return True if the user is marked as authenticated in the session
    return st.session_state.get("is_authenticated", False)
