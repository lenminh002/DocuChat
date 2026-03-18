from openai import OpenAI
from supabase import create_client, Client
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

supabase_url = os.getenv("SUPABASE_URL")
supabase_api_key = os.getenv("SUPABASE_API_KEY")
if not supabase_url or not supabase_api_key:
    raise ValueError("SUPABASE_URL and SUPABASE_API_KEY environment variables must be set.")

supabase_client: Client = create_client(supabase_url, supabase_api_key)
