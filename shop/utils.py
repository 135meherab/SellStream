
from cryptography.fernet import Fernet

# Generate and store this securely; it should be environment-specific
SECRET_KEY = Fernet.generate_key()
cipher_suite = Fernet(SECRET_KEY)

def encrypt_otp(otp):
    return cipher_suite.encrypt(otp.encode()).decode()

def decrypt_otp(encrypted_otp):
    return cipher_suite.decrypt(encrypted_otp.encode()).decode()
