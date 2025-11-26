from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    # Autenticación dummy: acepta cualquier usuario/contraseña
    if not request.username or not request.password:
        raise HTTPException(status_code=400, detail="Usuario y contraseña requeridos")
    return LoginResponse(access_token="dummy-token", token_type="bearer")
