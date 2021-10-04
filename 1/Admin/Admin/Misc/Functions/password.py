import random
import string

def generate_password():
    length = 8                

    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    symbols = string.punctuation

    all = lower + upper + num + symbols

    password = random.sample(all,length)

    return "".join(password)
