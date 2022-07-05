from .forms import SignUpForm
from .models import signUp as signUpModel
from django.http import HttpResponseRedirect
from django.shortcuts import render
import logging

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
