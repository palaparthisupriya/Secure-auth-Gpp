from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from crypto_utils import decrypt_seed, generate_totp_code, verify_totp_code
import os
import base64
import time

app = FastAPI()
DATA_PATH = "./data"
SEED_FILE = os.path.join(DATA_PATH, "seed.txt")
PRIVATE_KEY_FILE = "student_private.pem"

# Ensure /data exists
os.makedirs(DATA_PATH, exist_ok=True)

# Request models
class DecryptRequest(BaseModel):
    encrypted_seed: str

class VerifyRequest(BaseModel):
    code: str

# -------------------------------
# Endpoint 1: POST /decrypt-seed
# -------------------------------
@app.post("/decrypt-seed")
def decrypt_seed_endpoint(req: DecryptRequest):
    try:
        hex_seed = decrypt_seed(req.encrypted_seed, PRIVATE_KEY_FILE)
        with open(SEED_FILE, "w") as f:
            f.write(hex_seed)
        return {"status": "ok"}
    except Exception as e:
        return HTTPException(status_code=500, detail={"error": "Decryption failed"})

# -------------------------------
# Endpoint 2: GET /generate-2fa
# -------------------------------
@app.get("/generate-2fa")
def generate_2fa():
    try:
        if not os.path.exists(SEED_FILE):
            raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})
        with open(SEED_FILE, "r") as f:
            hex_seed = f.read().strip()

        code = generate_totp_code(hex_seed)
        # Calculate remaining seconds in current 30-sec period
        valid_for = 30 - (int(time.time()) % 30)
        return {"code": code, "valid_for": valid_for}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})

# -------------------------------
# Endpoint 3: POST /verify-2fa
# -------------------------------
@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    if not req.code:
        raise HTTPException(status_code=400, detail={"error": "Missing code"})
    try:
        if not os.path.exists(SEED_FILE):
            raise HTTPException(status_code=500, detail={"error": "Seed not decrypted yet"})
        with open(SEED_FILE, "r") as f:
            hex_seed = f.read().strip()

        valid = verify_totp_code(hex_seed, req.code)
        return {"valid": valid}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail={"error": str(e)})
