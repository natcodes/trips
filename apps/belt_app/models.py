from __future__ import unicode_literals
from django.db import models
import bcrypt 
#import datetime module
from datetime import datetime, timedelta
from datetime import date
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
#format regex 
import re 
LETTER_REGEX = re.compile(r"^[a-zA-Z]+$")
# EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

class UserManager(models.Manager):
    def reg_val(self, postData):
        errors = {}
#name validation
        if len(postData['name']) < 1:
            errors['name']="Name must be at least 3 characters long"
        if bool(re.search(r'\d', postData["name"])):
            errors['name']= "Name must be letters only"
#username validation
        if len(postData['username'])<1:
            errors['username'] = "please provide a user name"
#password 
        if len(postData['password']) < 1:
            errors['password'] = "Password must not be blank!"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters!"
#confirm password
        if len(postData['confirm_password']) < 1: 
            errors['confirm_password'] = "Please confirm your password!"
        if postData['password']!=postData["confirm_password"]:
            errors['password'] = "Password does not match confirmation."
#return errors for looping in html
        return errors        

    def login_val(self, postData):
        errors = {}  
        user = User.objects.filter(username=postData['username'])
        print user
        if len(postData['username']) < 1:
            errors['username'] = "Please enter your user name"
        if len(postData['password'])<1:
            errors['password'] = "Please enter a password"
        if not user:
            errors['username'] = "Incorrect login"
        #if password-entered hash doesn't match the database hash
        elif not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors['username'] = "Incorrect login"
        return errors 

class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length= 255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    def __str__(self):
        return " name: " + self.name + ", username: " + self.username 

class TripManager(models.Manager):
    def trip_val(self, postData):
        # user = User.objects.filter()
        start_date = unicode(postData['start_date'])
        date_today = unicode(date.today())
        end_date = unicode(postData['end_date'])
        errors = {}
        if len(postData['destination'])<1:
            errors['destination'] = "field can not be left empty"
        if len(postData['plan'])<1:
            errors['plan'] = "field can not be left empty"
        if len(postData['start_date']) < 8:
            errors['start_date'] = "Start date may not be black"
        if start_date <= date_today:
            errors['start_date'] = "Trip start date must be in the future"
        if end_date < start_date:
            errors['end_date'] = "Trip end date must be after the start date"

        return errors

class Trip(models.Model):
    destination = models.CharField(max_length=40)
    start_date = models.DateField(blank=False, default=datetime.now().strftime('%Y-%m-%d'))
    end_date = models.DateField(blank=False, default=datetime.now().strftime('%Y-%m-%d'))
    plan = models.CharField(max_length=30)
    join_by = models.ManyToManyField(User, related_name = "going_to")
    added_by = models.ForeignKey(User, related_name="added_trips", on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
    def __str__(self):
        return " to: " + self.destination
    
