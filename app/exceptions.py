

class UserAlreadyExistError(Exception):
    """exception for store when user exist with given id"""
    pass
    
class UserNotFoundError(Exception):
    """exception for store when user not found with given id"""
    pass