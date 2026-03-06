"""
API Key Manager - Manages API keys for integrations
"""
import os
import json
from typing import Dict, Optional
from cryptography.fernet import Fernet
from backend.utils.logger import log_info, log_error


class APIKeyManager:
    """Manages API keys securely for integrations"""

    def __init__(self, key_file: str = "api_keys.enc"):
        self.key_file = os.path.join("config", key_file)
        self.encryption_key = self._get_or_create_key()
        self.cipher = Fernet(self.encryption_key)
        self.keys: Dict[str, str] = {}
        self._load_keys()

    def _get_or_create_key(self) -> bytes:
        """Get or create encryption key"""
        key_file = "encryption.key"
        os.makedirs("config", exist_ok=True)

        if os.path.exists(key_file):
            with open(key_file, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(key_file, "wb") as f:
                f.write(key)
            return key

    def _load_keys(self):
        """Load encrypted keys from file"""
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, "rb") as f:
                    encrypted_data = f.read()
                    decrypted_data = self.cipher.decrypt(encrypted_data)
                    self.keys = json.loads(decrypted_data.decode())
        except Exception as e:
            log_error(f"Error loading API keys: {str(e)}")
            self.keys = {}

    def _save_keys(self):
        """Save keys encrypted to file"""
        try:
            data = json.dumps(self.keys).encode()
            encrypted_data = self.cipher.encrypt(data)
            with open(self.key_file, "wb") as f:
                f.write(encrypted_data)
        except Exception as e:
            log_error(f"Error saving API keys: {str(e)}")

    def set_key(self, service: str, key: str):
        """Set API key for a service"""
        self.keys[service] = key
        self._save_keys()
        log_info(f"API key set for service: {service}")

    def get_key(self, service: str) -> Optional[str]:
        """Get API key for a service"""
        return self.keys.get(service)

    def delete_key(self, service: str):
        """Delete API key for a service"""
        if service in self.keys:
            del self.keys[service]
            self._save_keys()
            log_info(f"API key deleted for service: {service}")

    def list_services(self) -> list:
        """List all services with keys"""
        return list(self.keys.keys())

    def has_key(self, service: str) -> bool:
        """Check if service has an API key"""
        return service in self.keys


# Global API key manager instance
api_key_manager = APIKeyManager()


# Convenience functions
def set_api_key(service: str, key: str):
    """Set API key for a service"""
    api_key_manager.set_key(service, key)


def get_api_key(service: str) -> Optional[str]:
    """Get API key for a service"""
    return api_key_manager.get_key(service)


def delete_api_key(service: str):
    """Delete API key for a service"""
    api_key_manager.delete_key(service)


def list_api_keys() -> list:
    """List all services with API keys configured"""
    return api_key_manager.list_services()


def list_api_services() -> list:
    """List all services with API keys"""
    return api_key_manager.list_services()


def has_api_key(service: str) -> bool:
    """Check if service has API key"""
    return api_key_manager.has_key(service)
