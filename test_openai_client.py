from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()  # reads .env in this folder

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Client created:", type(client))
