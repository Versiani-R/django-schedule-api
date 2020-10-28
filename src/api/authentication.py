from hashlib import sha256


def generate_hash(password):
    return sha256(password.encode('utf-8')).hexdigest()


def generate_token(email, password):
    return sha256(email.encode('utf-8') + password.encode('utf-8')).hexdigest()
