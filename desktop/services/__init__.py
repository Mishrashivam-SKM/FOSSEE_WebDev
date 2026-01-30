"""
Services Package - API client and authentication services.

Author: FOSSEE Team
Version: 2.0.0
"""

from services.api_client import APIClient
from services.auth_manager import AuthManager

__all__ = ['APIClient', 'AuthManager']
