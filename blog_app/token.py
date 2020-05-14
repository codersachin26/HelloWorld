import string
from random import shuffle

def generate_token():
    alphabets = string.ascii_lowercase
    digits = string.digits
    all_character = []
    all.extend(list(alphabets))
    all.extend(list(digits))
    token = shuffle(all_character)
    return token
