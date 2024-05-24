from passlib.context import CryptContext

class PasswordMixin:

    password_context: CryptContext = CryptContext(schemes=["argon2"])