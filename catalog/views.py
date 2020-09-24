from django.shortcuts import render

# Create your views here.
from .models import User, Class #Book, Author, BookInstance, Genre, 
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth.hashers import make_password,check_password
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages


def index(request):
    """View function for home page of site."""
    '''
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    
    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # The 'all()' is implied by default.    
    num_authors = Author.objects.count()
    
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }
    '''
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        # 如果登入成功，繫結引數到cookie中，set_cookie
        name = request.POST.get('name')
        password = request.POST.get('password')
        
        # 查詢使用者是否在資料庫中
        if User.objects.filter(name=name).exists():
            user = User.objects.get(name=name)
            if password == user.password:#check_password(password, user.password):
                user.save() #儲存
                context = {
                    'user': user
                }
                #return render(request, 'index.html',context)
                return HttpResponseRedirect('../homepage/')
        messages.error(request, '使用者帳號或密碼錯誤')
        return HttpResponseRedirect(reverse('login'))       
        return render(request, 'login.html')

def register(request):
    #form = UserCreationForm()
    if request.method == "POST":
        # 註冊
        name = request.POST.get('name')
        status = request.POST.get('status')
        email = request.POST.get('email')
        card_number = request.POST.get('card-number')        
        password = request.POST.get('password')
        c_password = request.POST.get('CPassword')
        if password == c_password:
            User.objects.create(name = name, password = password, email = email, status = status, card_number = card_number)
            return HttpResponseRedirect('../login/')
        else:
            messages.error(request, '請重新輸入密碼')
            return HttpResponseRedirect(reverse('register'))
        #return render(request, 'login.html')
        
    '''
    context = {
        'form': form
    }
    '''
    return render(request, 'register.html')