# test_nvidia_api.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

def test_api_key():
    API_KEY = os.getenv('NVIDIA_API_KEY')
    
    if not API_KEY:
        print(" No API key found in .env file")
        return False
    
    print(f"🔑 API Key: {API_KEY[:20]}...")
    
    # Test 1: List available models
    url = "https://integrate.api.nvidia.com/v1/models"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            models = response.json()['data']
            print(f" API Key is valid! Available models: {len(models)}")
            for model in models[:3]:  # Show first 3 models
                print(f"   - {model['id']}")
            return True
        else:
            print(f"API test failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f" Error testing API: {e}")
        return False

if __name__ == "__main__":
    test_api_key()