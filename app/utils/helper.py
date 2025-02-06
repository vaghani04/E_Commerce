def user_helper(user) -> dict:
    return {
        'name' : user['name'],
        'email' : user['email'],
        'password' : user['password'],
        'role' : user['role']
    }