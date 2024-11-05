from dotenv import load_dotenv
import os

# Charger les variables depuis .env
load_dotenv()

# Récupérer les variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
APP_NAME=os.getenv("APP_NAME")