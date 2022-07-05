from .LoginAttemptStatus import LoginAttemptStatus
from datetime import datetime,timedelta
from .forms import signUp as signUpModel

class Functions:
    @staticmethod
    def loginAttemptStatus(request, form,userName, password):
        query = signUpModel.objects.filter(userName=userName)

        if len(query) > 0:
            if query[0].isBlocked and \
                    (datetime.now().astimezone() + timedelta(minutes=325) - query[
                        0].lastLoginAttemptedTime).total_seconds() < 0:
                return query[0], LoginAttemptStatus.UserBlocked
            else:
                if query[0].check_password(password):
                    print("la1")
                    return query[0], LoginAttemptStatus.RightPassword
                else:
                    return (query[0], LoginAttemptStatus.WrongPassword)
        else:  # check using Mobile
            query = signUpModel.objects.filter(mobile=userName)
            if len(query) > 0:
                if query[0].isBlocked and \
                        (datetime.now().astimezone() + timedelta(minutes=325) - query[
                            0].lastLoginAttemptedTime).total_seconds() < 0:
                    return (query[0], LoginAttemptStatus.UserBlocked)
                else:
                    if query[0].check_password(password):
                        return query[0], LoginAttemptStatus.RightPassword
                    else:
                        return (query[0], LoginAttemptStatus.WrongPassword)
            else:
                return None, LoginAttemptStatus.UserNameNotFound
