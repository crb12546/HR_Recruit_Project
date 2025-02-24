"""Mock storage service for testing"""
import os
from typing import Dict, Optional

class MockStorageService:
    """Mock implementation of storage service for testing"""
    
    def __init__(self):
        """Initialize mock storage"""
        self.files: Dict[str, bytes] = {}
        
    def upload_file(self, content: bytes, file_path: str) -> str:
        """Upload a file to mock storage"""
        self.files[file_path] = content
        return f"https://mock-oss.test/{file_path}"
        
    def get_file(self, file_path: str) -> Optional[bytes]:
        """Get a file from mock storage"""
        return self.files.get(file_path)
