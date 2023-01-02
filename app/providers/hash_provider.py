from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_generate(senha):
    return pwd_context.hash(senha)

def check_password(senha, hash):
    return pwd_context.verify(senha, hash)