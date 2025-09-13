from passlib.context import CryptContext

# Create a CryptContext instance for password hashing using the bcrypt algorithm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Function to verify a plain password against a hashed one
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash a new password
def get_password_hash(password):
    return pwd_context.hash(password)