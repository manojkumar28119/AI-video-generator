from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class GPTService:
    def __init__(self):
        print("[GPT_SERVICE] Initializing GPT service...")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        print("[GPT_SERVICE] GPT service initialized successfully")
    
    async def extract_keywords(self, prompt: str) -> list:
        """Extract keywords from prompt using GPT"""
        print(f"[GPT_SERVICE] Starting keyword extraction for prompt: '{prompt[:50]}...'")
        
        try:
            print("[GPT_SERVICE] Sending request to OpenAI API...")
            gpt_response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You're helping generate search phrases for a stock video engine like Pexels. "
                        "From the given prompt, extract 3–5 clear, specific, and visually descriptive search phrases. "
                        "Fix any typos. Avoid repeating the original prompt exactly unless it's already suitable. "
                        "Think like a video search engine and imagine what people would tag a video with. "
                        "Return the phrases as a comma-separated string, without extra words."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

            keyword_string = gpt_response.choices[0].message.content.strip()
            print(f"[GPT_SERVICE] Raw GPT response: '{keyword_string}'")
            
            keywords = [k.strip() for k in keyword_string.split(",")]
            print(f"[GPT_SERVICE] Extracted keywords: {keywords}")
            
            return keywords
            
        except Exception as e:
            print(f"[GPT_SERVICE] ERROR: Failed to extract keywords - {str(e)}")
            raise e