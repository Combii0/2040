users = {
    'santi': '1234',
    'admin': 'roboyork'
}

def recognizeUser(u, p):
    if u not in users:
        return False

    elif p != users[u]:
        return False
    
    else:
        return True
