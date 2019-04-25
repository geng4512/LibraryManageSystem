from django.shortcuts import render, redirect


from django.http import HttpResponse
from . import models
from .forms import UserForm
from .forms import RegisterForm
from .forms import SearchForm
from .forms import ISBNForm
from .forms import ReviewForm
import hashlib
import datetime

def Encode(s, salt = 'geng4512'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def index(request):
    pass
    return render(request, 'login/index.html', locals())


def login(request):
    if request.session.get('is_login', None):
        return redirect('/index')

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.READER.objects.get(ACCOUNT=username)
                if user.PASSWORD == Encode(password):
                    request.session['is_login'] = True
                    request.session['user_id'] = user.ACCOUNT
                    request.session['user_name'] = user.NAME
                    return redirect('/index/')
                else:
                    message = "密码不正确！"
            except:
                message = "用户不存在！"
        return render(request, 'login/login.html', locals())

    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        # 登录状态不允许注册。你可以修改这条原则！
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            name = register_form.cleaned_data['name']
            if password1 != password2:  # 判断两次密码是否相同
                message = "两次输入的密码不同！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.READER.objects.filter(ACCOUNT = username)
                if same_name_user:  # 用户名不唯一
                    message = '用户已经存在，请重新选择用户名！'
                    return render(request, 'login/register.html', locals())

                # 当一切都OK的情况下，创建新用户

                new_user = models.READER.objects.create(ACCOUNT=username, PASSWORD=Encode(password1), NAME=name)
                new_user.save()
                return redirect('/login/')  # 自动跳转到登录页面
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        return redirect('/index/')
    request.session.flush()

    return redirect('/index/')

def search(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        message = "请检查填写的内容！"
        if search_form.is_valid():  # 获取数据
            bookname = search_form.cleaned_data['bookname']
            booklist = models.BOOKS.objects.filter(NAME__contains = bookname)
            return render(request, 'login/result.html/', locals())
    search_form = SearchForm()
    return render(request, 'login/search.html', locals())

def borrow(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    if request.method == "POST":
        isbn_form = ISBNForm(request.POST)
        message = "请检查填写的内容！"
        if isbn_form.is_valid():  # 获取数据
            isbn = isbn_form.cleaned_data['ISBN']
            book = models.BOOKS.objects.get(ISBN = isbn)
            USERNAME = request.session.get('user_id', None)
            if models.BORROR.objects.filter(ISBN = book, ACCOUNT = USERNAME).exists():
                message = "你已经借了这本书啦！"
            elif book.NUM > 0:
                message = "借书成功！"
                book.NUM = book.NUM - 1
                book.save()
                models.BORROR.objects.create(ISBN = book, ACCOUNT = models.READER.objects.get(ACCOUNT=USERNAME), DEADLINE = datetime.datetime.now() + datetime.timedelta(days=30))
            else :
                message = "目前图书馆里没有这本书！"
            return render(request, 'login/borrow.html/', locals())
    isbn_form = ISBNForm()
    return render(request, 'login/borrow.html', locals())

def renew(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    if request.method == "POST":
        isbn_form = ISBNForm(request.POST)
        message = "请检查填写的内容！"
        if isbn_form.is_valid():  # 获取数据
            isbn = isbn_form.cleaned_data['ISBN']
            book = models.BOOKS.objects.get(ISBN=isbn)
            USERNAME = request.session.get('user_id', None)
            if not models.BORROR.objects.filter(ISBN=book, ACCOUNT=USERNAME).exists():
                message = "你还没有借过这本书，不能续借！"
            else :
                message = "续借成功！"
                models.BORROR.objects.filter(ISBN=book, ACCOUNT=USERNAME).update(DEADLINE = datetime.datetime.now() + datetime.timedelta(days=30))
            return render(request, 'login/renew.html/', locals())
    isbn_form = ISBNForm()
    return render(request, 'login/renew.html', locals())

def mybooks(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    USERNAME = request.session.get('user_id', None)
    booklist = models.BORROR.objects.filter(ACCOUNT = USERNAME)
    return render(request, 'login/mybooklist.html/', locals())

def returnBooks(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    if request.method == "POST":
        isbn_form = ISBNForm(request.POST)
        message = "请检查填写的内容！"
        if isbn_form.is_valid():  # 获取数据
            isbn = isbn_form.cleaned_data['ISBN']
            book = models.BOOKS.objects.get(ISBN=isbn)
            USERNAME = request.session.get('user_id', None)
            if not models.BORROR.objects.filter(ISBN=book, ACCOUNT=USERNAME).exists():
                message = "你还没有借过这本书，不能还书！"
            else:
                myborrow = models.BORROR.objects.get(ISBN=book, ACCOUNT=USERNAME)
                message = "归还成功！"
                myborrow.ISBN.NUM += 1
                myborrow.ISBN.save()
                myborrow.delete()
            return render(request, 'login/return.html/', locals())
    isbn_form = ISBNForm()
    return render(request, 'login/return.html', locals())

def bookReview(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        message = "请检查填写的内容！"
        if review_form.is_valid():  # 获取数据
            isbn = review_form.cleaned_data['ISBN']
            if not models.BOOKS.objects.filter(ISBN=isbn).exists():
                message = "没有这本书！"
                return render(request, 'login/review.html/', locals())
            book = models.BOOKS.objects.get(ISBN=isbn)
            USERNAME = request.session.get('user_id', None)
            reader = models.READER.objects.get(ACCOUNT = USERNAME)
            score = review_form.cleaned_data['score']
            comment = review_form.cleaned_data['comment']
            models.REVIEW.objects.create(
                ISBN = book,
                ACCOUNT = reader,
                SCORE = score,
                COMMENT = comment
            )
            message = "评论成功"
            return render(request, 'login/review.html/', locals())
    review_form = ReviewForm()
    return render(request, 'login/review.html', locals())

def SearchReview(request):
    if not request.session.get('is_login', None):
        return redirect("/login/")
    if request.method == "POST":
        isbn_form = ISBNForm(request.POST)
        message = "请检查填写的内容！"
        if isbn_form.is_valid():  # 获取数据
            isbn = isbn_form.cleaned_data['ISBN']
            reviewlist = models.REVIEW.objects.filter(ISBN = isbn)
            return render(request, 'login/bookstate.html/', locals())
    isbn_form = ISBNForm()
    return render(request, 'login/searchreview.html', locals())
