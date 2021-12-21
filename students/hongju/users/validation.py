import re
from users.models     import User

def check_empty(email_or_pw):
    if email_or_pw == '':
        return True
    else:
        return False

def validate_email(email_data):
    if check_empty(email_data) == True:
        return 'empty'
    
    if User.objects.filter(email=email_data).exists():
        return 'duplicate_email'
    
    if re.match(r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$", email_data) == None:
        return 'no_match'

    return True

def validate_pw(pw_data):
    if check_empty(pw_data) == True:
        return 'empty'
        
    if re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*#?&]).{8,}$", pw_data) == None:
        return 'no_match'

    return True
