import string
from random import shuffle

def generate_token():
    alphabets = string.ascii_lowercase
    digits = string.digits
    all_character = []
    all.extend(list(alphabets))
    all.extend(list(digits))
    shuffle_character = shuffle(all_character)
    token = "".join(shuffle_character[0:6])
    return token
