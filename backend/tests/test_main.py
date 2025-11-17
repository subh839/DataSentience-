import pytest
import sys
import os
import requests  # Add this import

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_app_exists():
    """Test that the FastAPI app can be imported and exists"""
    from app.main import app
    assert app is not None
    assert hasattr(app, 'router')
    print("App import successful")

def test_routes_exist():
    """Test that expected routes exist in the app"""
    from app.main import app
    
    routes = [route.path for route in app.routes]
    assert "/" in routes
    assert "/api/health" in routes
    assert "/api/analyze" in routes
    print("All routes exist")

def test_app_title():
    """Test app metadata"""
    from app.main import app
    assert app.title == "DataSentience API"
    assert app.version == "1.0.0"
    print("App metadata correct")

def test_import_agents():
    """Test that agents can be imported"""
    from app.services.agents import AgentOrchestrator
    orchestrator = AgentOrchestrator()
    assert orchestrator is not None
    print(" Agents import successful")

def test_import_services():
    """Test that all services can be imported"""
    from app.services.vector_store import VectorStore
    from app.services.nim_service import NIMService
    from app.config import settings
    
    assert VectorStore is not None
    assert NIMService is not None
    assert settings.NVIDIA_API_KEY is not None
    print(" All services import successful")

def test_root_endpoint():
    """Test root endpoint via HTTP"""
    # Remove 'self' parameter and make sure server is running on port 8000
    response = requests.get("http://127.0.0.1:8000/")  # Changed to 8000
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("Root endpoint test passed")

def test_health_endpoint():
    """Test health endpoint via HTTP"""
    # Remove 'self' parameter
    response = requests.get("http://127.0.0.1:8000/api/health")  # Changed to 8000
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    print("Health endpoint test passed")