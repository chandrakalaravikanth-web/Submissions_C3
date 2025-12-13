"""LLM Factory for creating AI clients"""

from openai import OpenAI
from config import config

class LLMFactory:
    """Factory for creating LLM clients"""
    
    def __init__(self):
        self.client = None
    
    def get_client(self) -> OpenAI:
        """Get or create OpenAI client"""
        if not self.client and config.OPENROUTER_API_KEY:
            self.client = OpenAI(
                base_url=config.OPENROUTER_BASE_URL,
                api_key=config.OPENROUTER_API_KEY
            )
        return self.client
    
    def create_completion(self, messages: list, max_tokens: int = 2500):
        """Create a completion"""
        client = self.get_client()
        if not client:
            raise ValueError("No API key configured")
        
        try:
            response = client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=messages,
                max_tokens=max_tokens,
                temperature=config.TEMPERATURE
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"LLM API Error: {str(e)}")
