def user_helper(user):
    return {
        'name' : user['name'],
        'email' : user['email'],
        'password' : user['password'],
        'role' : user['role']
    }