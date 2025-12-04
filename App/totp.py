import pyotp
import time
import base64

def generate_totp(hex_seed):
    """Generate TOTP code from hex seed"""
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed)
    return totp.now()

def verify_totp(hex_seed, code, window=1):
    """Verify TOTP code with time window tolerance"""
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed)
    return totp.verify(code, valid_window=window)

def get_remaining_seconds():
    """Get remaining seconds in current TOTP period"""
    return 30 - (int(time.time()) % 30)