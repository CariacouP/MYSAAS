from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

# Connexion à Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_data():
    """Récupère les données de la table principale."""
    response = supabase.table("nom_table").select("*").execute()
    return response.data

def insert_data(new_data):
    """Insère de nouvelles données."""
    response = supabase.table("nom_table").insert({"colonne": new_data}).execute()
    return response.data