
from .forms import SignUpForm, LoginForm, TwoFactAuth
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
        if form.is_valid():

            if request.POST.get('UserName') == None:
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
            elif loginFlag == LoginAttemptStatus.WrongPassword:
                query.loginAttempt += 1
                query.lastLoginAttemptedTime = datetime.now()
                if query.loginAttempt >=3:
                    query.loginAttempt = 0
                    query.isBlocked = True
                    query.lastLoginAttemptedTime =datetime.now()
                    query.save()
                    failureMessaage = "You are Blocked for 5 minutes!"
                    return render(request, 'base.html', {'success': "Fail", 'failureMessage':failureMessaage})
                else:
                    query.save()
                    errorMessage = "Wrong Password. You have {} chances to Login.".format(3-query.loginAttempt)
                    return render(request, 'app1/loginPage.html',
                                  {'form': form, 'submitted': submitted,'success': "",'error':errorMessage})
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

                else:
                    failureMessaage = "You are blocked. Please wait {} seconds".format(int(abs(waitingTime.total_seconds())))
                    return render(request, 'base.html', {'success': "Fail", 'failureMessage': failureMessaage})

    else:
        form = LoginForm()
        return render(request, 'app1/loginPage.html',
                      {'form': form, 'submitted': submitted,'success': "", 'error':''})


def logout(request):
    try:
        del request.session['mobile']
        del request.session['counter']
        del request.session['otp']
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

def twoFactorAuth(request):
    submitted = False
    if request.session.get("mobile") == None:
        failureMessaage = "Session time-out. Please visit Login Page."
        return render(request, 'base.html', {'success': "Fail", 'failureMessage': failureMessaage})


    if request.method == 'POST':
            form = TwoFactAuth(request.POST)

            if form.is_valid():
                if request.POST.get("OTP") == None:
                    otpData = ""
                else:
                    otpData=request.POST['OTP']
                    if not (otpData.isnumeric()) or int(otpData)<0 or int(otpData)>999999:
                        otpData=""
                if otpData==request.session['otp']:

                    request.session["counter"] = 0
                    CongratsMessaage="Congrets! You have logged in successfully!"
                    return render(request, 'base.html',
                                  {'error': '', 'success': "Success", 'successMessage': CongratsMessaage})
                else:
                    if request.session["counter"] >= 3:
                        m = signUpModel.objects.filter(mobile=request.session.get("mobile"))
                        # print(m[0].isBlocked)
                        # changes needed
                        m[0].isBlocked = True
                        # print(m[0].isBlocked)
                        m[0].lastLoginAttemptedTime = datetime.now()
                        m[0].save()
                        del request.session['mobile']
                        del request.session['counter']
                        del request.session['otp']
                        failureMessaage = "You are Blocked for 5 minutes!"
                        return render(request, 'base.html', {'success': "Fail", 'failureMessage': failureMessaage})
                    form = TwoFactAuth()
                    otp = Functions.generateOtp(request.session["counter"],request.session['mobile'])
                    request.session["counter"] += 1
                    request.session['otp'] = otp
                    print(otp)
                    logging.info(otp)
                    errorMessage = "Invalid OTP. You have only {} change to Login.".format(4-request.session["counter"])
                    return render(request, 'app1/otpPage.html',
                                  {'form': form, 'submitted': submitted, 'success': "", 'error': errorMessage})

    else:
        form = TwoFactAuth()
        if request.session.get("mobile") == None:
            failureMessaage = "Session time-out. Please visit Login Page."
            return render(request, 'base.html', {'success': "Fail", 'failureMessage': failureMessaage})
        if request.session["counter"] >= 3:
            m = signUpModel.objects.filter(mobile=request.session.get("mobile"))
            # print(m[0].isBlocked)
            # changes needed
            m[0].isBlocked = True
            # print(m[0].isBlocked)
            m[0].lastLoginAttemptedTime = datetime.now()
            m[0].save()
            del request.session['mobile']
            del request.session['counter']
            del request.session['otp']
            failureMessaage = "You are Blocked for 5 minutes!"
            return render(request, 'base.html', {'success': "Fail", 'failureMessage': failureMessaage})
        otp = Functions.generateOtp(request.session["counter"],request.session['mobile'])
        request.session['otp'] = otp
        request.session["counter"] += 1
        print(otp)
        return render(request, 'app1/otpPage.html', {'form': form, 'submitted': submitted,'error':''})
    pass
