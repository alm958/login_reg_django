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
        result = User.objects.login(email=request.POST['email'], password=request.POST['password'])
    if result[0] == False :
        for error_message in result[1] :
            messages.error(request, error_message)
        return redirect(reverse( 'index' ) )
    else :
        for success_message in result[1] :
            messages.success(request, success_message)
        request.session['activeuser'] = result[2]
        return redirect(reverse( 'showusers', kwargs={'id': result[2]['id']}))

def register(request):
    if request.method == 'POST':
        result = User.objects.register(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], dob=request.POST['dob'], password=request.POST['password'], c_password=request.POST['c_password'])
        print result
        if result[0] == False :
            for error_message in result[1] :
                messages.error(request, error_message)
            return redirect(reverse( 'index' ) )
        else :
            for success_message in result[1] :
                messages.success(request, success_message)
            request.session['activeuser'] = result[2]
            return redirect(reverse( 'showusers', kwargs={'id': result[2]['id']}))

def showusers(request, id):
    if id == '' :
        request.session['del_user'] = False
        users = User.objects.getusers(id='all')
    else :
        print "id : ",id
        users = User.objects.getusers(id=id)
    user_count = len(users)
    context = {
    'users' : users,
    'user_count': user_count
    }
    return render(request, 'login_reg/user.html', context)

def logout(request):
    request.session.clear()
    request.session['del_user'] = False
    return redirect(reverse( 'index' ) )

def edituser(request, id):
    return render(request, 'login_reg/edituser.html' )

def updateuser(request, id):
    result = User.objects.updateuser(id=id,first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], dob=request.POST['dob'], old_password=request.POST['old_password'], new_password=request.POST['new_password'], c_new_password=request.POST['c_new_password'])
    print result
    if result[0] == False :
        for error_message in result[1] :
            messages.error(request, error_message)
        return redirect(reverse( 'edituser', kwargs={'id': id}))
    else :
        for success_message in result[1] :
            messages.success(request, success_message)
        request.session['activeuser'] = result[2]
        return redirect(reverse( 'showusers', kwargs={'id': id}))

def del_user_prompt(request, id):
    request.session['del_user'] = True
    return redirect(reverse( 'showusers', kwargs={'id': id}))

def keep_user(request, id):
    request.session['del_user'] = False
    return redirect(reverse( 'showusers', kwargs={'id': id}))

def deleteuser(request, id):
    if request.session['activeuser']['id'] == id :
        request.session.pop('name', None)
    User.objects.filter(id=id).delete()
    return redirect(reverse( 'index' ) )
