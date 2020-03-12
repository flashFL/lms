from django.shortcuts import render, redirect, HttpResponse
from app01 import models
import json
import datetime

# Create your views here.
def required_login(func):
    def inner(*args, **kwargs):
        request = args[0]
        if request.session.get('is_login'):
            return func(*args, **kwargs)
        else:
            if request.is_ajzx():
                return HttpResponse(json.dumps({'status': 0}))
            return redirect('/login/')
    return inner


@required_login
def book_list(request):
    all_book = models.Book.objects.all().order_by('pk')
    return render(request, 'book_list.html', {'all_book': all_book})


@required_login
def add_book(request):
    error = ''
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        author = request.POST.get('author')
        publisher = request.POST.get('publisher')
        if not book_name or not author or not publisher:
            error = '*不能输入为空'
        if models.Book.objects.filter(book_name=book_name, author=author, publisher=publisher):
            error = '提交失败！该书已存在'
        if not error:
            models.Book.objects.create(book_name=book_name, author=author, publisher=publisher)
            return redirect('/book_list/')
    return render(request, 'add_book.html', {'error': error})


@required_login
def del_book(request):
    pk = request.GET.get('id')
    obj = models.Book.objects.filter(pk=pk)
    obj.delete()
    return redirect('/book_list/')


@required_login
def edit_book(request):
    error = ''
    pk = request.GET.get('id')
    obj = models.Book.objects.get(pk=pk)
    if request.method == 'POST':
        obj.book_name = request.POST.get('book_name')
        obj.author = request.POST.get('author')
        obj.publisher = request.POST.get('publisher')
        if not obj.book_name or not obj.author or not obj.publisher:
            error = '*不能输入为空'
        if not error:
            obj.save()
            return redirect('/book_list/')
    return render(request, 'edit_book.html', {'obj': obj, 'error': error})


def login(request):
    error = ''
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        user = models.User.objects.filter(user_name=user_name, pwd=pwd)
        if user:
            request.session['is_login'] = True
            request.session['user_name'] = user_name
            # request.session['last_time'] = str(user.last_time)
            user.last_time = datetime.datetime.now()
            return redirect('/book_list/')
        else:
            error = '账号或密码错误，请重新输入！'
    return render(request, 'login.html', {'error': error})


def register(request):
    error = ''
    if request.method == 'POST':
        user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        if not user_name or not pwd:
            error = '*输入不能为空'
        if models.User.objects.filter(user_name=user_name):
            error = '该账号已存在，请重新输入'
        if not error:
            models.User.objects.create(user_name=user_name, pwd=pwd, last_time=datetime.datetime.now())
            return render(request, 'page_jump.html')
    return render(request, 'register.html', {'error': error})


@required_login
def logout(request):
    request.session.flush()
    return redirect('/login/')