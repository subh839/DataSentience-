import pytest
import asyncio
import sys
import os

# Add the app directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def sample_analysis():
    """Sample analysis data for testing"""
    return {
        "root_causes": ["Cooling system degradation", "Filter blockage"],
        "severity": "High - Potential system failure",
        "time_to_failure_hours": 72,
        "affected_systems": ["Cooling System", "Server Racks"],
        "confidence_score": 0.85
    }

@pytest.fixture
def sample_query():
    """Sample query for testing"""
    return "Why is my cooling system consuming more power?"

@pytest.fixture
def sample_documents():
    """Sample documents for vector store testing"""
    return [
        "Cooling system maintenance should be performed quarterly",
        "UPS batteries need replacement every 3 years",
        "Optimal data center temperature is 18-27°C"
    ]