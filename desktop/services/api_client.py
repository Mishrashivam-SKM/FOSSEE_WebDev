"""
API Client - HTTP client for Django backend communication.

This module provides an API client that handles authentication,
token refresh, and all backend API endpoints matching the web frontend.

Author: FOSSEE Team
Version: 2.0.0
"""

from __future__ import annotations

import os
from typing import Optional, Dict, Any, List, Callable
from urllib.parse import urljoin

import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

from PyQt5.QtCore import QObject, pyqtSignal

from services.auth_manager import get_auth_manager


# API Base URL - same as web frontend
API_BASE_URL = os.environ.get('CEV_API_URL', 'http://localhost:8000/api')


class APIError(Exception):
    """Custom exception for API errors."""
    
    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        errors: Optional[List[str]] = None
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.errors = errors or []


class APIClient(QObject):
    """
    API Client for backend communication.
    
    Handles all HTTP requests with authentication, token refresh,
    and error handling.
    
    Signals:
        request_started: Emitted when a request starts.
        request_finished: Emitted when a request finishes.
        auth_required: Emitted when authentication is required.
        error_occurred: Emitted with error message on request failure.
    """
    
    request_started = pyqtSignal()
    request_finished = pyqtSignal()
    auth_required = pyqtSignal()
    error_occurred = pyqtSignal(str)
    
    def __init__(self, auth_manager=None, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        
        self.base_url = API_BASE_URL
        self.auth_manager = auth_manager if auth_manager else get_auth_manager()
        self.session = requests.Session()
        self.timeout = 30
    
    def _get_headers(self, include_auth: bool = True) -> Dict[str, str]:
        """Get request headers with optional auth token."""
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }
        
        if include_auth:
            token = self.auth_manager.get_access_token()
            if token:
                headers['Authorization'] = f'Bearer {token}'
        
        return headers
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        include_auth: bool = True,
        retry_on_401: bool = True
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the backend.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH).
            endpoint: API endpoint path.
            data: Request body data.
            files: Files to upload (for multipart).
            include_auth: Whether to include auth token.
            retry_on_401: Whether to retry with refreshed token on 401.
            
        Returns:
            Response data as dictionary.
            
        Raises:
            APIError: On request failure.
        """
        url = urljoin(self.base_url + '/', endpoint.lstrip('/'))
        headers = self._get_headers(include_auth)
        
        self.request_started.emit()
        
        try:
            if files:
                # Multipart form data for file uploads
                headers.pop('Content-Type', None)  # Let requests set it
                response = self.session.request(
                    method=method,
                    url=url,
                    data=data,
                    files=files,
                    headers=headers,
                    timeout=self.timeout
                )
            else:
                response = self.session.request(
                    method=method,
                    url=url,
                    json=data,
                    headers=headers,
                    timeout=self.timeout
                )
            
            # Handle 401 with token refresh
            if response.status_code == 401 and retry_on_401 and include_auth:
                if self._refresh_token():
                    # Retry with new token
                    return self._make_request(
                        method, endpoint, data, files,
                        include_auth=True, retry_on_401=False
                    )
                else:
                    self.auth_manager.clear_auth()
                    self.auth_required.emit()
                    raise APIError("Session expired. Please login again.", 401)
            
            # Handle other errors
            if not response.ok:
                error_data = {}
                try:
                    error_data = response.json()
                except:
                    pass
                
                error_msg = error_data.get('error', error_data.get('detail', 'Request failed'))
                errors = error_data.get('errors', {})
                
                # Return error response instead of raising for auth endpoints
                return {
                    'success': False,
                    'error': error_msg,
                    'errors': errors,
                    'status_code': response.status_code
                }
            
            # Handle empty responses (204 No Content)
            if response.status_code == 204:
                return {'success': True}
            
            return response.json()
            
        except Timeout:
            self.error_occurred.emit("Request timed out")
            raise APIError("Request timed out. Please try again.", None)
        except ConnectionError:
            self.error_occurred.emit("Could not connect to server")
            raise APIError("Could not connect to server. Please check your connection.", None)
        except RequestException as e:
            self.error_occurred.emit(str(e))
            raise APIError(f"Request failed: {str(e)}", None)
        finally:
            self.request_finished.emit()
    
    def _refresh_token(self) -> bool:
        """
        Attempt to refresh the access token.
        
        Returns:
            True if refresh successful, False otherwise.
        """
        refresh_token = self.auth_manager.get_refresh_token()
        if not refresh_token:
            return False
        
        try:
            response = self.session.post(
                urljoin(self.base_url + '/', 'auth/token/refresh/'),
                json={'refresh': refresh_token},
                headers={'Content-Type': 'application/json'},
                timeout=self.timeout
            )
            
            if response.ok:
                data = response.json()
                new_token = data.get('access')
                if new_token:
                    self.auth_manager.update_access_token(new_token)
                    return True
        except:
            pass
        
        return False
    
    # =========================================================================
    # AUTHENTICATION ENDPOINTS
    # =========================================================================
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """
        Login user.
        
        Args:
            username: User's username.
            password: User's password.
            
        Returns:
            Response with user and tokens.
        """
        response = self._make_request(
            'POST', '/auth/login/',
            data={'username': username, 'password': password},
            include_auth=False
        )
        
        if response.get('success'):
            self.auth_manager.save_auth(
                response.get('tokens', {}),
                response.get('user', {})
            )
        
        return response
    
    def register(
        self,
        username: str,
        email: str,
        password: str,
        password_confirm: str
    ) -> Dict[str, Any]:
        """
        Register new user.
        
        Args:
            username: Desired username.
            email: User's email.
            password: Password.
            password_confirm: Password confirmation.
            
        Returns:
            Response with user and tokens.
        """
        response = self._make_request(
            'POST', '/auth/register/',
            data={
                'username': username,
                'email': email,
                'password': password,
                'password_confirm': password_confirm
            },
            include_auth=False
        )
        
        if response.get('success'):
            self.auth_manager.save_auth(
                response.get('tokens', {}),
                response.get('user', {})
            )
        
        return response
    
    def logout(self) -> Dict[str, Any]:
        """Logout current user."""
        try:
            refresh_token = self.auth_manager.get_refresh_token()
            if refresh_token:
                self._make_request(
                    'POST', '/auth/logout/',
                    data={'refresh': refresh_token}
                )
        except:
            pass  # Ignore logout errors
        finally:
            self.auth_manager.clear_auth()
        
        return {'success': True}
    
    def get_profile(self) -> Dict[str, Any]:
        """Get current user profile."""
        return self._make_request('GET', '/auth/profile/')
    
    # =========================================================================
    # DATASET ENDPOINTS
    # =========================================================================
    
    def get_datasets(self) -> List[Dict[str, Any]]:
        """Get all datasets for current user."""
        return self._make_request('GET', '/datasets/')
    
    def get_dataset(self, dataset_id: int) -> Dict[str, Any]:
        """Get a specific dataset."""
        return self._make_request('GET', f'/datasets/{dataset_id}/')
    
    def delete_dataset(self, dataset_id: int) -> Dict[str, Any]:
        """Delete a dataset."""
        return self._make_request('DELETE', f'/datasets/{dataset_id}/')
    
    def upload_file(self, file_path: str, name: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a CSV file.
        
        Args:
            file_path: Path to CSV file.
            name: Optional custom dataset name.
            
        Returns:
            Response with dataset info.
        """
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, 'text/csv')}
            data = {}
            if name:
                data['name'] = name
            
            return self._make_request(
                'POST', '/datasets/upload/',
                data=data,
                files=files
            )
    
    # =========================================================================
    # ANALYTICS ENDPOINTS
    # =========================================================================
    
    def get_dashboard_analytics(self) -> Dict[str, Any]:
        """Get combined dashboard analytics for all datasets."""
        return self._make_request('GET', '/datasets/dashboard/')
    
    def get_dataset_analytics(self, dataset_id: int) -> Dict[str, Any]:
        """Get analytics for a specific dataset."""
        return self._make_request('GET', f'/datasets/{dataset_id}/analytics/')
    
    def get_dataset_equipment(self, dataset_id: int) -> List[Dict[str, Any]]:
        """Get equipment items for a dataset."""
        return self._make_request('GET', f'/datasets/{dataset_id}/equipment/')
    
    # =========================================================================
    # PDF REPORT ENDPOINT
    # =========================================================================
    
    def download_pdf(self, dataset_id: int, save_path: str) -> bool:
        """
        Download PDF report and save to specified path.
        
        Args:
            dataset_id: Dataset ID.
            save_path: Path to save the PDF file.
            
        Returns:
            True if successful, False otherwise.
        """
        url = urljoin(self.base_url + '/', f'datasets/{dataset_id}/pdf/')
        headers = self._get_headers()
        
        try:
            response = self.session.get(
                url,
                headers=headers,
                timeout=self.timeout,
                stream=True
            )
            
            if response.ok:
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                return True
            else:
                raise APIError("Failed to download PDF", response.status_code)
                
        except Exception as e:
            self.error_occurred.emit(f"PDF download failed: {str(e)}")
            return False
    
    # =========================================================================
    # EQUIPMENT ENDPOINTS
    # =========================================================================
    
    def get_all_equipment(self, params: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Get all equipment items with optional filtering."""
        endpoint = '/equipment/'
        if params:
            query = '&'.join(f'{k}={v}' for k, v in params.items())
            endpoint += f'?{query}'
        return self._make_request('GET', endpoint)


# Global singleton instance
_api_client: Optional[APIClient] = None


def get_api_client() -> APIClient:
    """Get or create the global APIClient instance."""
    global _api_client
    if _api_client is None:
        _api_client = APIClient()
    return _api_client
