import random, string

def generate_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(random.choice(alphabet) for i in range(16))