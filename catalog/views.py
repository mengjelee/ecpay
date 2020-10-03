from django.shortcuts import render

# Create your views here.
from .models import User, Class #Book, Author, BookInstance, Genre,
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
                response = HttpResponseRedirect('../homepage/')
                response.set_cookie("user_id", user.user_id)
                response.set_cookie("user_name", user.name)
                response.set_cookie("user_email", user.email)
                if user.status == 1:
                    response.set_cookie("user_status", "Teacher")
                else:
                    response.set_cookie("user_status", "Student")
                response.set_cookie("user_card_number", user.card_number)
                return response
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
            messages.success(request, '註冊成功！')
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

def homepage(request):
    if request.COOKIES != None: 
        try:
            user_name = request.COOKIES['user_name']
        except:
            return HttpResponse('No user name.') 
    context = {
        'user_name': user_name
    }
    return render(request, 'homepage.html', context)

def editdata(request):
    if request.method == 'GET':
        if request.COOKIES != None: 
            try:
                context = {
                    'user_name': request.COOKIES['user_name'],
                    'user_email': request.COOKIES['user_email'],
                    'user_status': request.COOKIES['user_status'],
                    'user_card_number': request.COOKIES['user_card_number'],
                }
            except:
                return HttpResponse('User undifined.') 
        return render(request, 'editdata.html', context)
    elif request.method == 'POST':
        user_id = request.COOKIES['user_id']
        if User.objects.filter(user_id = user_id).exists():
            user = User.objects.get(user_id = user_id)
            user.name = request.POST.get('name')
            user.email = request.POST.get('email')
            user.card_number = request.POST.get('card_number')
            user.save()
            messages.success(request, '資料修改成功')
            response = HttpResponseRedirect('../homepage/')
            response.set_cookie("user_name", user.name)
            response.set_cookie("user_email", user.email)
            response.set_cookie("user_card_number", user.card_number)
            return response
        else:
            messages.error(request, '資料修改失敗')
            return HttpResponseRedirect(reverse('editdata'))

def changepw(request):
    if request.method == 'GET':
        return render(request, 'changepw.html')
        '''
        if request.method == 'GET':
            if request.COOKIES != None: 
                try:
                    context = {
                        'user_id': request.COOKIES['user_id'],
                    }
                except:
                    return HttpResponse('User undifined.') 
            return render(request, 'changepw.html', context)
        '''
    elif request.method == 'POST':
        password = request.POST.get('pw')
        newpw = request.POST.get('newpw')
        confirmpw = request.POST.get('confirmpw')
        if password == newpw or newpw != confirmpw:
            messages.error(request, '請重新輸入密碼')
            return HttpResponseRedirect(reverse('changepw'))
        user_id = request.COOKIES['user_id']
        if User.objects.filter(user_id = user_id).exists():
            user = User.objects.get(user_id = user_id)
            if password == user.password:
                user.password = newpw
                user.save() #儲存
                messages.success(request, '密碼修改成功，請重新登錄！')
                response = HttpResponseRedirect('../login/')
                return response
            else:
                messages.error(request, '請重新輸入密碼')
                return HttpResponseRedirect(reverse('changepw'))