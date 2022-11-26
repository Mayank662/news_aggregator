from django.shortcuts import render, redirect
from .models import UserData
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup as Bsoup

# Create your views here.
def register(request):
    
    if request.method == 'GET': 
        return render(request, 'register.html')

    elif request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        isuserexist = UserData.objects.filter(email = email)

        if isuserexist:
            return HttpResponse('Email Already Exists!')

        if pass1 != pass2:
            return HttpResponse('Both password need to be similar')

        user_obj = UserData(first_name = fname, last_name = lname, email = email, password = pass1)
        user_obj.save()

        return redirect('/scrape')
        
def login(request):
    
    if request.method == 'GET':
        return render(request, 'login.html')
    
    elif request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = UserData.objects.get(email = email, password = password)
            user_data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'pk': user.pk
            }

            # setting session for the user
            request.session['user_data'] = user_data
            return redirect('/scrape')

        except:
            return HttpResponse('Invalid')
            
def logout(request):
    request.session.flush()
    return redirect('/')

def scrape(request):
    
    if request.session.get('user_data'):
        user_data = request.session.get('user_data')
    else:
        return redirect('/')

    session = requests.Session()
    session.headers = {"User-Agent": "Googlebot/2.1 (+http://www.google.com/bot.html)"}
    url = 'https://timesofindia.indiatimes.com/india'
    content = session.get(url, verify=False).content

    soup = Bsoup(content, 'html.parser')
    data = soup.find('ul',attrs={'class':'cvs_wdt clearfix'})
    news_list = []
    for each_ul in data:
        each_news_dict = {
            'title': each_ul.text,
            'link': each_ul.a['href']
        }
        news_list.append(each_news_dict)

    context = {
        'user_data': user_data,
        'news_data': news_list
    }

    return render(request, 'news.html', context)