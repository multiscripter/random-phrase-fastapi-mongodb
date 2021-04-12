import hashlib


class AuthService:
    """Auth service."""

    def __init__(self, root_dir: str):
        self.hash_name = 'sha256'
        self.iterations = 100000
        self.root_dir = root_dir

    def check(self, key: str) -> bool:
        with open(self.root_dir + '.htsalt') as f:
            salt = f.readlines()
        with open(self.root_dir + '.hthash', 'br') as f:
            orig = f.readlines()[0]

        key = key.encode('utf-8')
        salt = bytearray(salt[0], 'utf-8')
        pass_hash = hashlib.pbkdf2_hmac(
            self.hash_name, key, salt, self.iterations
        )
        return orig == pass_hash
