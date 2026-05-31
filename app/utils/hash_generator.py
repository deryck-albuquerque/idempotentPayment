import hashlib
import json


def generate_request_hash(payload: dict) -> str:
    """
    Converte o payload
    para uma string padronizada.

    sort_keys=True garante:

    {
        "a":1,
        "b":2
    }

    seja igual a

    {
        "b":2,
        "a":1
    }
    """
    normalized_payload = json.dumps(
        payload,
        sort_keys=True
    )

    """
    Gera SHA256.

    Exemplo:

    e3b0c44298fc...
    """

    return hashlib.sha256(
        normalized_payload.encode()
    ).hexdigest()