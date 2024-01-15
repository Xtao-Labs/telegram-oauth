import hashlib
import hmac
from typing import Optional

from starlette.datastructures import QueryParams

from src.config import settings


async def verify_telegram_auth_data(params: QueryParams) -> Optional[int]:
    data = list(params.items())
    hash_str = ""
    text_list = []
    for key, value in data:
        if key == "hash":
            hash_str = value
        else:
            text_list.append(f"{key}={value}")
    check_string = "\n".join(sorted(text_list))

    secret_key = hashlib.sha256(str.encode(settings.BOT_TOKEN)).digest()
    hmac_hash = hmac.new(secret_key, str.encode(check_string), hashlib.sha256).hexdigest()

    return int(params.get("id")) if hmac_hash == hash_str else None
