import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Load private key
with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

# Read commit hash
with open("commit_hash.txt", "r") as f:
    commit_hash = f.read().strip()

# Sign commit hash
signature = private_key.sign(
    commit_hash.encode(),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Base64 encode
signature_b64 = base64.b64encode(signature).decode()

# Save to file
with open("encrypted_commit_signature.txt", "w") as f:
    f.write(signature_b64)

print("Encrypted signature generated!")
