# app/services/nim_service.py
import requests
import os
import asyncio
from app.config import settings

class NIMService:
    def __init__(self):
        self.api_key = settings.NVIDIA_API_KEY
        self.base_url = "https://integrate.api.nvidia.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    async def generate_completion(self, prompt: str, system_prompt: str = ""):
        """Generate completion using reasoning models only"""
        url = f"{self.base_url}/chat/completions"
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        # Try different reasoning models
        reasoning_models = [
            "meta/llama-3.1-8b-instruct",
            "microsoft/phi-3-mini-4k-instruct", 
            "google/gemma-2-2b-it",
            "mistralai/mistral-7b-instruct"
        ]
        
        for model in reasoning_models:
            try:
                payload = {
                    "model": model,
                    "messages": messages,
                    "temperature": 0.1,
                    "top_p": 0.7,
                    "max_tokens": 1024,
                    "stream": False
                }
                
                print(f" Trying reasoning model: {model}")
                response = requests.post(url, json=payload, headers=self.headers)
                response.raise_for_status()
                print(f" Successfully used reasoning model: {model}")
                return response.json()
            except Exception as e:
                print(f" Model {model} failed: {e}")
                continue
        
        raise Exception("All reasoning models failed")

nim_service = NIMService()