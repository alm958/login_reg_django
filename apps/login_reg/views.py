from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
from django.urls import reverse
from django.core.urlresolvers import reverse

# Create your views here.
def index(request):
    return render(request, 'login_reg/index.html' )

def login(request):
    if request.method == 'POST':
        result = User.objects.login(email=request.POST['email'], password=request.POST['password'], c_password=request.POST['c_password'])
    if result[0] == False :
        print "result : ", result[0]
        for error_message in result[1] :
            messages.error(request, error_message)
        return redirect(reverse( 'index' ) )
    else :
        print "result : ", result[0]
        for success_message in result[1] :
            messages.success(request, success_message)
        request.session['activeuser'] = result[2]
        return redirect(reverse( 'users/'+str(result[2].id) ) )

def register(request):
    if request.method == 'POST':
        result = User.objects.register(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], dob=request.POST['dob'], password=request.POST['password'], c_password=request.POST['c_password'])
        if result[0] == False :
            print "result : ", result[0]
            for error_message in result[1] :
                messages.error(request, error_message)
            return redirect(reverse( 'index' ) )
        else :
            print "result : ", result[0]
            for success_message in result[1] :
                messages.success(request, success_message)
            request.session['activeuser'] = result[2]
            print "*|/"*15
            print result[2].id
            print "*|/"*15
            return redirect(reverse( 'showusers', kwargs={'id': 11 }))

def showusers(request, id):
    if id == '' :
        users = User.objects.getusers(id='all')
        return render(request, 'login_reg/allusers.html', context)
    else :
        users = User.objects.getusers(id=id)

    context = {
    'users' : users
    }
    return render(request, 'login_reg/users.html', context)

def logout(request):
    request.session.pop('name', None)
    return redirect(reverse( 'index' ) )
