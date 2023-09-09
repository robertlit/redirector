import random
import string


def generate_random_src(length: int = 10) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
