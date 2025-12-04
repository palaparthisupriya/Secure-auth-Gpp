# app/__init__.py
"""
PKI-Based 2FA Microservice package initializer.

This file makes the `app` folder a Python package and
imports core modules for easy access.
"""

from .crypto import decrypt_seed, encrypt_seed, load_keys
from .totp import generate_totp, verify_totp
from .api import app  # FastAPI app instance
