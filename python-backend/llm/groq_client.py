import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-70b-8192")

class GroqClient:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = Groq(api_key=GROQ_API_KEY)
        return cls._instance
    
    def generate(self, messages: list[dict]) -> str:
        response = self.client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0,
            max_tokens=1024
        )
        return response.choices[0].message.content.strip()