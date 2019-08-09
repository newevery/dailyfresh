from django.shortcuts import render, redirect
from django.urls import reverse
import re
from apps.user.models import User
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serialzer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.http import HttpResponse
from celery_task.tasks import send_register_active_email
from django.contrib.auth import authenticate, login


# Create your views here.
# /user/register

class RegisterView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        username = request.POST.get("user_name")
        password = request.POST.get("pwd")
        email = request.POST.get("email")
        allow = request.POST.get('allow')
        if not all([username, password, email]):
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user:
            return render(request, 'register.html', {'errmsg': '用户已存在'})
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        serialzer = Serialzer(settings.SECRET_KEY, 3600)
        print(user.id)
        info = {"confirm": user.id}
        token = serialzer.dumps(info)
        token = token.decode('utf-8')

        # send_mail(subject,message,sender,reciver,html_message=html_message)
        send_register_active_email.delay(email, username, token)
        return redirect(reverse('index'))


class ActiveView(View):
    def get(self, request, token):
        serialzer = Serialzer(settings.SECRET_KEY, 3600)
        try:
            info = serialzer.loads(token)
            user_id = info['confirm']
            print(user_id)
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()
            return redirect(reverse('login'))
        except SignatureExpired as e:
            return HttpResponse('激活链接失效')


class LoginView(View):
    def get(self, request):
        if 'username' in request.COOKIES:
            username=request.COOKIES.get('username')
            checked='checked'
        else:
            username=''
            checked=''
        return render(request, 'login.html',{'username':username,'checked':checked})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("pwd")

        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                print('登陆成功')
                login(request, user)
                response = redirect(reverse('index'))
                remember = request.POST.get('remember')
                if remember == 'on':
                    response.set_cookie('username', username, max_age=7 * 24 * 3600)
                else:
                    response.delete_cookie('username')
                return render(request, 'index.html')

            else:
                print('用户未激活')
                return render(request, 'login.html', {'errmsg': '用户未激活'})
        else:
            return render(request, 'login.html', {'errmsg': '用户账号密码错误'})
