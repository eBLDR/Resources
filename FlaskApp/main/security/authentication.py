import hashlib


def authenticate(username, password):
    """
    Authenticate user credentials.
    :param username: user name input
    :param password: user password input
    :return auth: validation result
    """
    auth = False
    reason = ''

    user = ''  # Fill me

    if user:
        hash_pwd = hashlib.md5(password.encode('utf-8')).hexdigest()
        if user.password == hash_pwd:
            auth = True
        else:
            reason = 'Wrong password.'
    else:
        reason = 'Username not found.'

    return auth, reason
