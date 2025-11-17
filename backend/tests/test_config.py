# tests/test_config.py
import pytest
import os
from app.config import settings

class TestConfig:
    """Test application configuration"""
    
    def test_settings_loaded(self):
        """Test that settings are properly loaded"""
        assert hasattr(settings, 'NVIDIA_API_KEY')
        assert isinstance(settings.NVIDIA_API_KEY, str)
        assert settings.NVIDIA_API_KEY.startswith('nvapi-')
    
    def test_database_url(self):
        """Test database URL setting"""
        assert settings.DATABASE_URL == "chroma_data"
    
    def test_debug_mode(self):
        """Test debug mode setting"""
        assert isinstance(settings.DEBUG, bool)