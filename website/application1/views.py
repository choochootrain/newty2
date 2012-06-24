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
import classify_one_view
import uuid
from pymongo import Connection, DESCENDING
import operator
import heapq
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



c = Connection('localhost', 27018)
db = c['body_words']
body_words = db['all_body_words']
db = c['title_words']
title_words = db['all_title_words']
articles = c['all_articles']['techcrunch.com']            

def get_classification(request):
    try:
        word = request.REQUEST['word']
    except:
        jsonData = simplejson.loads(request.raw_post_data)
        word = jsonData['word']
    print word

    word_arr = word.split(' ')
    to_return = {}
    for single_word in word_arr:
        title_entries_matched = title_words.find({'word' : single_word}).sort('date', DESCENDING)
        body_entries_matched = body_words.find({'word' : single_word}).sort('date', DESCENDING)
        threshold = .01
        counts_per_date = {}
        '''        
        for entry in title_entries_matched:
            date = entry['date']
            percentage = entry['percentage']
            if percentage > threshold:
                if date in counts_per_date:
                    counts_per_date[date] += 2
                else:
                    counts_per_date[date] = 2
                    '''
        for entry in body_entries_matched:
            date = entry['date']
            percentage = entry['percentage']
            if percentage > threshold:
                if date in counts_per_date:
                    counts_per_date[date] += 1
                else:
                    counts_per_date[date] = 1
        
        one_result = []
        sorted_counts = sorted(counts_per_date.iteritems(), key=operator.itemgetter(0))
        for k, v in sorted_counts:
            print k
            time = int(k.strftime('%s'))
            one_result.append([time, v])
        to_return[single_word] = one_result
    return HttpResponse(json.dumps(to_return))
        
'''
        if classify_one_view.main('http://www.techcrunch.com', single_word):
            word_coll = db[single_word]
            threshold = .01
            counts_per_date = {}
            for entry in word_coll.find().sort('date', DESCENDING):
                date = entry['date']
                percentage = entry['percentage']
                if percentage > threshold:
                    if date in counts_per_date:
                        counts_per_date[date] += 1
                    else:
                        counts_per_date[date] = 1 '''
    

def html5_timeline(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('html5_timeline.html', c)


def get_relevant_articles(request):
    try:
        word = request.REQUEST['word']
        date = request.REQUEST['date']
    except:
        json_data = simplejson.loads(request.raw_post_data)
        word = json_data['word']
        date = json_data['date']
    date_time_obj = datetime.fromtimestamp(int(date))
    begin_time = datetime.fromtimestamp(int(date) - 129600)
    end_time = datetime.fromtimestamp(int(date) + 129600)
    heap = []
    for body_obj in body_words.find({'word' : word, 'date' : {"$lt": end_time}, 'date' : {"$gt": begin_time}}):
        article = articles.find_one({'_id' : body_obj['article_id']})
        heap.append((rank(word, article, body_obj), article))
    heapq.heapify(heap)
    top_five = heapq.nlargest(35, heap)
    result = []
    put_in = set()
    count = 0
    for ranker, article in top_five:
        if count == 10:
            break
        count += 1
        if article['title'] in put_in:
            continue
        else:
            put_in.add(article['title'])
        result.append({'url' : article['url'], 'title' : article['title']})
    return HttpResponse(json.dumps(result))
    


def rank(user_input, article, body_obj):
    score = 0
    if user_input in article['title']:
        score += 10
    score += body_obj['total_num_matched']
    score *= body_obj['total_num_words']
    return score
