import os
import json
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "netlogai-secret-key-2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def load_users():
    if not os.path.exists(USERS_FILE):
        default = {
            "admin": {
                "username": "admin",
                "hashed_password": pwd_context.hash("admin123"),
                "email": "admin@netlogai.com",
                "full_name": "Admin User"
            }
        }
        save_users(default)
        return default
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_users(users: dict):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password = plain_password[:70]
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    password = password[:70]
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    users = load_users()
    user = users.get(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def register_user(username: str, password: str, email: str, full_name: str):
    try:
        users = load_users()
        if username in users:
            raise HTTPException(status_code=400, detail="Username already exists")
        if len(password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        if not email or "@" not in email:
            raise HTTPException(status_code=400, detail="Invalid email address")
        users[username] = {
            "username": username,
            "hashed_password": get_password_hash(password),
            "email": email,
            "full_name": full_name
        }
        save_users(users)
        return {"message": "User created successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    users = load_users()
    user = users.get(username)
    if user is None:
        raise credentials_exception
    return user