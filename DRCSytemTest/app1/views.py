from .forms import SignUpForm, LoginForm
from .models import signUp as signUpModel
from django.http import HttpResponseRedirect
from django.shortcuts import render,HttpResponse,redirect
import logging
from datetime import datetime, timedelta
from .Functions import Functions
from .LoginAttemptStatus import LoginAttemptStatus
def signUp(request):
    submitted = False
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            CongratsMessaage="Congrats!! You have Successfully Signed-up!"
            print(CongratsMessaage)
            logging.info(CongratsMessaage)
            return render(request, 'base.html', {'error': '','success': "Success", 'successMessage':CongratsMessaage})
    else:
        form = SignUpForm()
        if 'submitted' in request.GET:
            submitted = True
    return render(request, 'app1/signUp.html', {'form': form, 'submitted': submitted,'error': '','success':''})


def login(request):
    submitted = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print("qqqq")
        if form.is_valid():
            print("12121iowie")

            if request.POST.get('UserName') == None:
                print(type(form))
                print(type(form.cleaned_data))
                print("riowie")
                errorMessage = "Invalid Username/Mobile no."
                return render(request, 'app1/loginPage.html',
                              {'form': form, 'success': "", 'error': errorMessage})
            else:
                userName = form.cleaned_data['UserName']
            if request.POST.get('Password') == None:
                password = ''
            else:
                password = form.cleaned_data['Password']

            query, loginFlag=Functions.loginAttemptStatus(request,form,userName, password)

            if loginFlag == LoginAttemptStatus.UserNameNotFound:
                errorMessage = "Invalid Username/Mobile no."
                return render(request, 'app1/loginPage.html',
                              {'form': form, 'submitted': submitted,'success': "", 'error': errorMessage})
                # return HttpResponse("Invalid Username/Mobile no")
            elif loginFlag == LoginAttemptStatus.WrongPassword:
                query.loginAttempt += 1
                query.lastLoginAttemptedTime = datetime.now()
                if query.loginAttempt >=3:
                    query.loginAttempt = 0
                    query.isBlocked = True
                    query.lastLoginAttemptedTime =datetime.now()
                    query.save()
                    failureMessaage = "You are Blocked for 10 minutes!"
                    return render(request, 'base.html', {'success': "Fail", 'failureMessage':failureMessaage})
                    # return HttpResponse("You are Blocked for 10 minutes!")
                else:
                    query.save()
                    errorMessage = "Wrong Password. You have {} chances to Login.".format(3-query.loginAttempt)
                    return render(request, 'app1/loginPage.html',
                                  {'form': form, 'submitted': submitted,'success': "",'error':errorMessage})
                    # return HttpResponse("Wrong Password")
            elif loginFlag == LoginAttemptStatus.RightPassword:
                try:
                    query.loginAttempt = 0
                    query.isBlocked = False
                    query.lastLoginAttemptedTime = datetime.now()
                    query.save()
                    request.session["mobile"] = query.mobile
                    request.session["counter"] = 0
                    return redirect('/twoFactAuth')
                except:
                    pass
            elif loginFlag == LoginAttemptStatus.UserBlocked:
                waitingTime = (datetime.now().astimezone() + timedelta(minutes=325) -query.lastLoginAttemptedTime)
                if waitingTime.total_seconds() >= 0:
                    successMessaage = "You Are Unblocked.. please login again!"
                    return render(request, 'base.html', {'success': "success", 'successMessaage': successMessaage})

                    # return HttpResponse("You Are Unblocked.. please login again!")
                else:
                    failureMessaage = "You are blocked. Please wait {} seconds".format(int(abs(waitingTime.total_seconds())))
                    return render(request, 'base.html', {'success': "Fail", 'failureMessage': failureMessaage})

                    # return HttpResponse("You are blocked. Please wait {} seconds".format(int(abs(waitingTime.total_seconds()))))

    else:
        form = LoginForm()
        return render(request, 'app1/loginPage.html',
                      {'form': form, 'submitted': submitted,'success': "", 'error':''})


def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")
