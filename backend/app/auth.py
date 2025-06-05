import time
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2AuthorizationCodeBearer
import jwt
from jwt import PyJWKClient
from app.core.settings import settings

# ⚙️ URLs
KEYCLOAK_INTERNAL_URL = "http://keycloak:8080/realms/myrealm"  # Comunicação interna Docker
KEYCLOAK_EXTERNAL_URL = "http://localhost:8080/realms/myrealm"  # Token emitido com localhost

OPENID_CONFIG_URL = f"{KEYCLOAK_INTERNAL_URL}/.well-known/openid-configuration"

import requests

def wait_for_keycloak():
    print("🔄 Aguardando o Keycloak estar pronto...")
    while True:
        try:
            response = requests.get(OPENID_CONFIG_URL)
            if response.status_code == 200:
                print("✅ Keycloak está pronto!")
                break
        except Exception as e:
            print(f"⏳ Keycloak ainda não respondeu... ({e})")
        time.sleep(3)

# Aguarda o Keycloak ficar disponível
wait_for_keycloak()

# Baixar OpenID Config
OPENID = requests.get(OPENID_CONFIG_URL).json()
ALGORITHMS = ["RS256"]

# OAuth2 via Keycloak
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{KEYCLOAK_EXTERNAL_URL}/protocol/openid-connect/auth",
    tokenUrl=f"{KEYCLOAK_EXTERNAL_URL}/protocol/openid-connect/token"
)

# Inicializa o PyJWKClient
jwks_client = PyJWKClient(OPENID["jwks_uri"])

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        signing_key = jwks_client.get_signing_key_from_jwt(token).key

        payload = jwt.decode(
            token,
            signing_key,
            algorithms=ALGORITHMS,
            audience="myconverter",
            issuer=f"{KEYCLOAK_EXTERNAL_URL}"
        )
        return payload
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Token inválido: {str(e)}")
