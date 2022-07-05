from django.db import models
from django.core.validators import RegexValidator
from datetime import datetime
class signUp(models.Model):
    userName = models.CharField(max_length=30,unique=True)
    password = models.CharField(max_length=12)
    email = models.EmailField()
    mobileRegex = RegexValidator(regex = r'[0-9]{10}', message="Mobile must be have 10 digits.")
    mobile= models.CharField(max_length=10, validators= [mobileRegex],unique=True)
    loginAttempt = models.IntegerField(default=0)
    lastLoginAttemptedTime = models.DateTimeField(default=datetime.now())
    isBlocked = models.BooleanField(default=False)

    def __str__(self):
        return self.userName + " " + self.email + " " + self.mobile + " " + self.password

    def check_password(self, req):
        if self.password == req:
            return True
        else:
            return False