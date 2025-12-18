import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

STUDENT_ID = "23A91A05H7"
REPO_URL = "https://github.com/palaparthisupriya/PKI-Based-2fa-Microservice.git"

# Generate seed
seed_input = STUDENT_ID + REPO_URL
seed = hashlib.sha256(seed_input.encode()).hexdigest()

# Load private key
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# Sign seed
signature = private_key.sign(
    seed.encode(),
    padding.PKCS1v15(),
    hashes.SHA256()
)

# Write raw signature
with open("proof.sig", "wb") as f:
    f.write(signature)

print("Proof generated successfully")
print("Seed:", seed)
print("Signature size:", len(signature), "bytes")
