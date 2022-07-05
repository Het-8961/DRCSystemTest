import enum
class LoginAttemptStatus(enum.Enum):
    UserNameNotFound = -1
    WrongPassword = 0
    RightPassword = 1
    UserBlocked = -2