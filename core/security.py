import os

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkeyhex")
ALGORITHM = os.getenv("ALGORITHM", "HS512")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
