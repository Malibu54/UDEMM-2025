import hashlib


def generar_hash(
    password
):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()