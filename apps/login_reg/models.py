from __future__ import unicode_literals
from django.db import models
from datetime import datetime, date
import bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+[a-zA-Z-]*[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, **kwargs):
        message_list = []
        min_age = 13
        today = date.today()
        if not (NAME_REGEX.match(kwargs['first_name']) and NAME_REGEX.match(kwargs['last_name'])):
            message_list.append('Both name fields are required and can contain only letters. (hyphens OK)')
        if not EMAIL_REGEX.match(kwargs['email']):
            message_list.append('Invalid e-mail address entered. Please enter valid email address.')
        elif User.objects.filter(email=kwargs['email']).exists():
            message_list.append('The e-mail address entered already exists in the database.')
        if len(kwargs['password']) < 8:
            message_list.append("Password must be at least eight characters in length")
        elif kwargs['password'] != kwargs['c_password']:
            message_list.append("Password and Password Confirmation do not match.")
        print (kwargs['dob'] == '')
        if kwargs['dob'] == '':
            message_list.append("Date of birth is a required field. You must be {} years of age to register.".format(min_age))
        else :
            dob_date = datetime.strptime(kwargs['dob'], "%Y-%m-%d").date()
            if (dob_date.year + min_age, dob_date.month, dob_date.day) > (today.year, today.month, today.day):
                message_list.append("You must be {} years of age to register.".format(min_age))

        if len(message_list) is 0 :
            pw_hash = bcrypt.hashpw(kwargs['password'].encode(), bcrypt.gensalt())
            user = self.create(first_name=kwargs['first_name'], last_name=kwargs['last_name'], email=kwargs['email'], dob=kwargs['dob'], password=pw_hash)
            activeuser_dict = {'first_name' : user.first_name, 'last_name' : user.last_name, 'email' : user.email, 'dob' : user.dob, 'id' : user.id}
            message_list.append('New User {} {} successfully registered and logged in.'.format(user.first_name, user.last_name))
            return (True, message_list, activeuser_dict )
        else :
            return (False, message_list)

    def login(self, **kwargs):
        message_list = []
        if not EMAIL_REGEX.match(kwargs['email']):
            message_list.append('Invalid e-mail address entered. Please enter valid email address.')
        if len(kwargs['password']) < 8:
            message_list.append("Password must be at least eight characters in length")
        elif kwargs['password'] != kwargs['c_password']:
            message_list.append("Password and Password Confirmation do not match.")
        if len(message_list) == 0:
            if User.objects.filter(email=kwargs['email']).exists():
                user = self.get(email=kwargs['email'])
                if bcrypt.hashpw(kwargs['password'].encode(), user.password.encode()) ==  user.password.encode() :
                    activeuser_dict = {'first_name' : user.first_name, 'last_name' : user.last_name, 'email' : user.email, 'dob' : unicode(user.dob), 'id' : user.id}
                    message_list.append('User {} {} successfully logged in.'.format(user.first_name, user.last_name))
                    return (True, message_list, activeuser_dict)
            message_list.append("Email, Password combination not found.  Check and try again.")
        return (False, message_list)

    def getusers(self, **kwargs):
        if kwargs['id'] == 'all':
            users = Users.objects.values('first_name','last_name','id','dob','created_at','updated_at')
        else :
            users = User.objects.filter(id=kwargs['id']).values('first_name','last_name','id','dob','created_at','updated_at')
        return users

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    dob = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
