from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from models import *
# from .models import User
from django.contrib import messages
from datetime import datetime, timedelta
import bcrypt
from django.core.urlresolvers import reverse

def index(request):
    return render(request, 'belt_app/index.html')

def login(request):
    errors = User.objects.login_val(request.POST)
    print errors
    if errors:
        for key, error in errors.items():
            messages.error(request, error, extra_tags="log {}".format(key))
        return redirect("/")
    else:
        request.session["id"]=User.objects.get(username=request.POST['username']).id
        # messages.success(request, "Welcome!")
        return redirect("/home")
    return errors

def registration(request):
    errors = User.objects.reg_val(request.POST)
    if errors:
        for key, error in errors.items():
            messages.error(request, error, extra_tags="reg {}".format(key))
        return redirect('/')
    else:
        user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()))
        request.session['id'] = user.id
        return redirect('/home')

def logout(request):
    this_user = request.session['id']
    request.session.flush()
    return redirect('/')

def home(request):
    try:
        request.session['id']
    except KeyError:
        return redirect('/')

    user_logged = User.objects.get(id=request.session['id'])
    my_add = Trip.objects.filter(added_by__id = request.session['id'])
    my_join = Trip.objects.filter(join_by__id = request.session['id'])
    others_join= Trip.objects.all().exclude(join_by__id =request.session['id'])

    context = {
        "user_logged" : user_logged,
        "my_add": my_add,
        "my_join": my_join,
        "others_join": others_join,

    }
    
    return render(request, "belt_app/home.html", context)

def addtrip_page(request):
    return render(request, "belt_app/addtrip.html")

def addtrip(request):
    user_logged = User.objects.get(id=request.session['id'])
    errors = Trip.objects.trip_val(request.POST)
    if errors:
        for key, error in errors.items():
            messages.error(request, error, extra_tags="add {}".format(key))
        return redirect('/addtrip_page')
    else:
        new_trip = Trip.objects.create(destination=request.POST['destination'], start_date=datetime.strptime(request.POST['start_date'], '%Y-%m-%d'), end_date=datetime.strptime(request.POST["end_date"], '%Y-%m-%d'), plan=request.POST["plan"], added_by= user_logged)
    return redirect('/home')

def viewtrip(request, id):
    tripview = Trip.objects.get(id=id)
    users_joining = tripview.join_by.all()

    context = {
        "tripview" : tripview,
        "users_joining" : users_joining
    }
    return render(request, "belt_app/destination.html", context)

def jointrip(request, id):
    this_trip = Trip.objects.get(id=id)
    this_trip.join_by.add(request.session['id'])
    return redirect('/home')

