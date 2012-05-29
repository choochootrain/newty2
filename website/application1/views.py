from django.http import HttpResponse, HttpRequest, HttpResponseNotFound, Http404
from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from application1.models import UserExtended
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import json
from django.utils import simplejson
from datetime import datetime
import uuid
def home(request):
    # t = loader.get_template('postRequest.html')
    # t.render(Context({"name":"Lu"}))
    #{{{Name}}}
    if request.user.is_authenticated():
        is_authenticated = True
    else:
        is_authenticated = False
    
    c = {'Name':'Lu', 'is_authenticated':is_authenticated}
    c.update(csrf(request))
    #return render_to_response('postRequest.html', c)
    return render_to_response('index.html', c)
#return HttpResponse(loader.get_template('postRequest.html').render(c))
#return HttpResponse("you have come home to app1")

def timeline(request):
    if request.user.is_authenticated():
        is_authenticated = True
    else:
        is_authenticated = False
    
    c = {'Name':'Lu', 'is_authenticated':is_authenticated}
    c.update(csrf(request))
    #return render_to_response('postRequest.html', c)
    return render_to_response('timeline.html', c)

def timeline_dynamic(request):
    if request.user.is_authenticated():
        is_authenticated = True
    else:
        is_authenticated = False
    
    c = {'Name':'Lu', 'is_authenticated':is_authenticated}
    c.update(csrf(request))
    #return render_to_response('postRequest.html', c)
    return render_to_response('timeline_dynamic.html', c)


def get_timeline_ajax(request):
    jsonData = simplejson.loads(request.raw_post_data)
    keyword = jsonData['keyword']
    print keyword
    data = [{"label": "Trolling News", "data": [[2000, 5.9], [2000.5, 3.9], [2001, 2.0], [2002, 1.2], [2003, 1.3], [2004, 2.5], [2005, 2.0], [2006, 3.1], [2007, 2.9], [2008, 0.9]]}
            ,{"label": "Test2", "data": [[1999, -0.1], [2000, 2.9], [2001, 0.2], [2002, 0.3], [2003, 1.4], [2004, 2.7], [2005, 1.9], [2006, 2.0], [2007, 2.3], [2008, -0.7]]}]
    return HttpResponse(json.dumps(data))


def createUser(request):

    jsonData = simplejson.loads(request.raw_post_data)
    username = jsonData['username'].strip()
    email = jsonData['email'].strip()
    password = jsonData['password'].strip()
    first = jsonData['first'].strip()
    last = jsonData['last'].strip()
    newUser = User(username=username, email=email, password=password, first_name=first, last_name=last)
    newUser.set_password(password)
    newUser.save()
    
    return HttpResponse("Yay")




def login_view(request):
    jsonData = simplejson.loads(request.raw_post_data)
    email = jsonData['email'].strip()
    password = jsonData['password'].strip()
    if email == '' or password == '':
        return HttpResponse("wrong password")
    if len(User.objects.filter(email=email)) == 1:
        username = User.objects.get(email=email).username
    else:
        return HttpResponse("wrong password")

    user = authenticate(username=username, password=password)

    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse(user.first_name)
        else:
            return HttpResponse("no longer active")
    else:
        return HttpResponse("wrong password")

def logout_view(request):
    logout(request)
    return HttpResponse("Successfully logged out")


def get_id(request):
    id = request.REQUEST['id']
    try:
        posting_obj = UserExtended.objects.get(x = id)
    except Exception:
        return HttpResponse("you have no entry with x = " + id)
    return HttpResponse("your request id was there " + id)
