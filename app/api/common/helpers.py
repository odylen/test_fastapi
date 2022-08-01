import string
import random


def generate_code(code_length) -> str:
    code = ''.join(random.choices(string.digits, k=code_length))
    return code
