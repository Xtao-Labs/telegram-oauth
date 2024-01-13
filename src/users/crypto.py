import base64
import pathlib
import re
import string
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Tuple

from Crypto.PublicKey import RSA
from jose import constants, jwt
from jose.exceptions import JWTError

from ..config import settings

RANDOM_STRING_CHARS = string.ascii_lowercase + string.ascii_uppercase + string.digits
KEYS = {}


def reformat_rsa_key(rsa_key: str) -> str:
    """Reformat an RSA PEM key without newlines to one with correct newline characters

    @param rsa_key: the PEM RSA key lacking newline characters
    @return: the reformatted PEM RSA key with appropriate newline characters
    """
    # split headers from the body
    split_rsa_key = re.split(r"(-+)", rsa_key)

    # add newlines between headers and body
    split_rsa_key.insert(4, "\n")
    split_rsa_key.insert(6, "\n")

    reformatted_rsa_key = "".join(split_rsa_key)

    # reformat body
    return RSA.importKey(reformatted_rsa_key).exportKey().decode("utf-8")


def read_rsa_key_from_env(file_path: str) -> str:
    if file_path in KEYS:
        return KEYS[file_path]
    path = pathlib.Path(file_path)

    # path to rsa key file
    if path.is_file():
        with open(file_path, "rb") as key_file:
            jwt_private_key = RSA.importKey(key_file.read()).exportKey()
        k = jwt_private_key.decode("utf-8")
        KEYS[file_path] = k
        return k

    # rsa key without newlines
    if "\n" not in file_path:
        k = reformat_rsa_key(file_path)
        KEYS[file_path] = k
        return k

    return file_path


def get_n(rsa: RSA):
    bytes_data = rsa.n.to_bytes((rsa.n.bit_length() + 7) // 8, 'big')
    return base64.urlsafe_b64encode(bytes_data).decode('utf-8')


def get_pub_key_resp():
    pub_key = RSA.importKey(read_rsa_key_from_env(settings.JWT_PUBLIC_KEY))
    return {
        "keys": [
            {
                "n": get_n(pub_key),
                "kty": "RSA",
                "alg": "RS256",
                "kid": "sig",
                "e": "AQAB",
                "use": "sig"
            }
        ]
    }


def encode_jwt(
        expires_delta,
        sub,
        secret=None,
        additional_claims=None,
        algorithm=constants.ALGORITHMS.RS256,
):
    if additional_claims is None:
        additional_claims = {}
    if secret is None:
        secret = read_rsa_key_from_env(settings.JWT_PRIVATE_KEY)
    now = datetime.now(timezone.utc)

    claims = {
        "iat": now,
        "jti": str(uuid.uuid4()),
        "nbf": now,
        "sub": sub,
        "exp": now + timedelta(seconds=expires_delta),
        **additional_claims,
    }

    return jwt.encode(
        claims,
        secret,
        algorithm,
    )


def decode_jwt(
        encoded_token,
        secret=None,
        algorithms=None,
):
    if algorithms is None:
        algorithms = constants.ALGORITHMS.RS256
    if secret is None:
        secret = read_rsa_key_from_env(settings.JWT_PRIVATE_KEY)
    return jwt.decode(
        encoded_token,
        secret,
        algorithms=algorithms,
    )


def get_jwt(user):
    access_token = encode_jwt(
        sub=str(user.id),
        expires_delta=settings.ACCESS_TOKEN_EXP,
        additional_claims={
            "token_type": "access",
            "is_blocked": user.is_blocked,
            "is_superuser": user.is_superuser,
            "username": user.username,
            "is_active": user.is_active,
        },
    )

    refresh_token = encode_jwt(
        sub=str(user.id),
        expires_delta=settings.REFRESH_TOKEN_EXP,
        additional_claims={
            "token_type": "refresh",
            "is_blocked": user.is_blocked,
            "is_superuser": user.is_superuser,
            "username": user.username,
            "is_active": user.is_active,
        },
    )

    return access_token, refresh_token


def authenticate(
        *,
        token: str,
        key: str,
) -> Tuple[bool, Dict]:
    """Authenticate user by token"""
    try:
        token_header = jwt.get_unverified_header(token)
        decoded_token = jwt.decode(token, key, algorithms=token_header.get("alg"))
    except JWTError:
        return False, {}
    else:
        return True, decoded_token
