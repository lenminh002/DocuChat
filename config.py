import os
from openai import OpenAI
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# OpenAI config
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OpenAI API key is missing or invalid.")
openai = OpenAI(api_key=openai_api_key)

# Supabase config
supabase_key = os.environ.get("SUPABASE_API_KEY")
if not supabase_key:
    raise ValueError("Expected env var SUPABASE_API_KEY")
url = os.environ.get("SUPABASE_URL")
if not url:
    raise ValueError("Expected env var SUPABASE_URL")

supabase: Client = create_client(url, supabase_key)