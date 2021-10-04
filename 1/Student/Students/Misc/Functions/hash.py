import bcrypt


def generate_salt():
    return bcrypt.gensalt(14)


def get_hashed_password(password, salt):
    return bcrypt.hashpw(password.encode(), salt).removeprefix(salt)


def check_password(password, salted_hashed_password):
    return bcrypt.checkpw(password.encode(), salted_hashed_password.encode())
