# coding:utf-8
import base64
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.conf import settings as django_settings
from django.views.generic import View
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode

from .forms import VmaigUserCreationForm
from .models import MyUser
import json
from django.http import HttpResponse, Http404
import logging
import re
from itsdangerous import URLSafeTimedSerializer as utsr

# logger
logger = logging.getLogger(__name__)


class Confirm(View):
    """
    用于处理前端验证表单时的ajax请求
    """
    pass


class UserControl(View):
    def post(self, request, *args, **kwargs):
        # 获取要对用户进行什么操作
        slug = self.kwargs.get('slug')

        if slug == 'login':
            return self.login(request)
        elif slug == "logout":
            return self.logout(request)
        elif slug == "register":
            return self.register(request)
        elif slug == "changepassword":
            return self.changepassword(request)
        elif slug == "forgetpassword":
            return self.forgetpassword(request)
        elif slug == "resetpassword":
            return self.resetpassword(request)

        raise PermissionDenied

    def get(self, request, *args, **kwargs):
        # 如果是get请求直接返回404页面
        raise Http404

    def login(self, request):
        errors = []
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
            user = auth.authenticate(username=email, password=password)
        elif email:
            try:
                user = MyUser._default_manager.get(id_num=email)
                user = auth.authenticate(username=user.email, password=password)
            except:
                user = None
        else:
            user = None

        if user is not None:
            auth.login(request, user)
        else:
            errors.append("密码或者用户名不正确")

        mydict = {"errors": errors}
        return HttpResponse(json.dumps(mydict), content_type="application/json")

    def logout(self, request):
        if not request.user.is_authenticated():
            logger.error(u'[UserControl]用户未登录')
            raise PermissionDenied
        else:
            auth.logout(request)
            return HttpResponse('OK')

    def register(self, request):
        username = self.request.POST.get("username", "")
        password1 = self.request.POST.get("password1", "")
        id_num = self.request.POST.get('id_num', "")
        password2 = self.request.POST.get("password2", "")
        email = self.request.POST.get("email", "")

        form = VmaigUserCreationForm(request.POST)

        errors = []
        # 验证表单是否正确
        if form.is_valid():
            # 下列代码只在注册需要接收邮件时使用
            # current_site = get_current_site(request)
            # site_name = current_site.name
            # domain = current_site.domain
            # title = u"欢迎注册计算机语言作业平台！"
            # message = u"你好！ %s ,感谢注册计算机语言作业平台 ！\n\n" % (username) + \
            #           u"请牢记以下信息：\n" + \
            #           u"用户名：%s \n" % id_num + \
            #           u"昵称：%s" % username + "\n" + \
            #           u"邮箱：%s" % email + "\n" + \
            #           u"网站：http://%s" % domain + "/test\n\n"
            # from_email = 'fornjupt@163.com'
            # try:
            #     send_mail(title, message, from_email, [email])
            # except Exception as e:
            #     logger.error(u'[UserControl]用户注册邮件发送失败:[%s]/[%s]' % (username, email))
            #     print(e)
            #     return HttpResponse(u"发送邮件错误!\n注册失败", status=500)

            new_user = form.save()
            user = auth.authenticate(username=email, password=password2)
            auth.login(request, user)

        else:
            # 如果表单不正确,保存错误到errors列表中
            for k, v in form.errors.items():
                # v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())

        mydict = {"errors": errors}

        return HttpResponse(json.dumps(mydict), content_type="application/json")

    def changepassword(self, request):
        if not request.user.is_authenticated():
            logger.error(u'[UserControl]用户未登录')
            raise PermissionDenied

        form = PasswordChangeForm(request.user, request.POST)

        errors = []
        # 验证表单是否正确
        if form.is_valid():
            user = form.save()
            auth.logout(request)
        else:
            # 如果表单不正确,保存错误到errors列表中
            for k, v in form.errors.items():
                # v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())

        mydict = {"errors": errors}
        return HttpResponse(json.dumps(mydict), content_type="application/json")

    def forgetpassword(self, request):
        username = self.request.POST.get("username", "")
        email = self.request.POST.get("email", "")

        form = VmaigPasswordRestForm(request.POST)

        errors = []

        # 验证表单是否正确
        if form.is_valid():
            token_generator = default_token_generator
            from_email = None
            opts = {
                'token_generator': token_generator,
                'from_email': from_email,
                'request': request,
            }
            user = form.save(**opts)

        else:
            # 如果表单不正确,保存错误到errors列表中
            for k, v in form.errors.items():
                # v.as_text() 详见django.forms.util.ErrorList 中
                errors.append(v.as_text())

        mydict = {"errors": errors}
        return HttpResponse(json.dumps(mydict), content_type="application/json")

    def resetpassword(self, request):
        uidb64 = self.request.POST.get("uidb64", "")
        token = self.request.POST.get("token", "")
        password1 = self.request.POST.get("password1", "")
        password2 = self.request.POST.get("password2", "")

        try:
            uid = urlsafe_base64_decode(uidb64)
            user = MyUser._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, MyUser.DoesNotExist):
            user = None

        token_generator = default_token_generator

        if user is not None and token_generator.check_token(user, token):
            form = SetPasswordForm(user, request.POST)
            errors = []
            if form.is_valid():
                user = form.save()
            else:
                # 如果表单不正确,保存错误到errors列表中
                for k, v in form.errors.items():
                    # v.as_text() 详见django.forms.util.ErrorList 中
                    errors.append(v.as_text())

            mydict = {"errors": errors}
            return HttpResponse(json.dumps(mydict), content_type="application/json")
        else:
            logger.error(u'[UserControl]用户重置密码连接错误:[%s]/[%s]' % (uidb64, token))
            return HttpResponse("密码重设失败!\n密码重置链接无效，可能是因为它已使用。可以请求一次新的密码重置.", status=403)


def login(request):
    """
    处理登陆相关事项
    :param request: 请求
    :return: get请求时，返回用户到登陆界面，post请求时，验证账户并登陆
    """
    if request.method == 'POST':
        username = request.POST.get("username", "")
        password = request.POST.get("passwd", "")
        if username:
            user = auth.authenticate(username=username.lower(), password=password)  # 默认username是邮箱的情况
            if user is None:
                try:
                    user = MyUser.objects.get(id_num=username)
                    print(user)
                    print(user.email)
                    user = auth.authenticate(username=user.email, password=password)  # 如果用户名不是邮箱的情况
                except:
                    user = None
        else:
            user = None

        if user is not None:
            if user.is_active:
                auth.login(request, user)
                # 如果用户不记住登陆，则设置为关闭浏览器之后清除登陆状态
                if request.POST.get('remember_login') != 'true':
                    request.session.set_expiry(0)
                    pass
                else:
                    request.session.set_expiry(7 * 86400)
                return JsonResponse({'valid': True})
            else:
                return JsonResponse({'valid': False, 'info': '账户尚未激活'})
        else:
            return JsonResponse({'valid': False, 'info': '账户或密码错误'})


def logout(request):
    auth.logout(request)
    return JsonResponse({"valid": True})


def register(request):
    username = request.POST.get("nickname", "")
    password = request.POST.get("password", "")
    id_num = request.POST.get('username', "")
    email = request.POST.get("email", "")
    try:
        MyUser.objects.get(id_num=id_num)
        return JsonResponse({'valid': False, "info": "用户名已被注册"})
    except ObjectDoesNotExist:
        try:
            MyUser.objects.get(email__iexact=email)
            return JsonResponse({'valid': False, "info": "邮箱已被注册"})
        except ObjectDoesNotExist:
            pass
    user = MyUser.objects.create_user(email=email, id_num=id_num, username=username, password=password)
    user.save()
    auth.login(request, user)
    return JsonResponse({'valid': True})


def forget_password(request):
    current_site = get_current_site(request)
    email = request.POST.get("email", "")
    try:
        user = MyUser.objects.get(email__iexact=email)
        token = token_confirm.generate_validate_token(email)
        message = "\n".join([u'{0}'.format(email), u'请访问该链接，完成重置密码：',
                             '/'.join([current_site.domain, 'accounts', 'resetpassword', token])])
        send_mail(u'校科协作业平台密码重置', message, 'gaoliangim@qq.com', [email], fail_silently=False)
        return JsonResponse({'valid': True, 'info': "请查收相关邮件以继续"})
    except ObjectDoesNotExist:
        return JsonResponse({"valid": False, "info": "此Email尚未注册本平台！"})


class Token:
    """
    与激活用户相关的token类
    """

    def __init__(self, security_key):
        self.security_key = security_key
        self.salt = base64.encodebytes(security_key.encode())

    def generate_validate_token(self, username):
        """
        生成token
        :param username: 用户名
        :return: 生成的token
        """
        serializer = utsr(self.security_key)
        return serializer.dumps(username, self.salt)

    def confirm_validate_token(self, token, expiration=3600):
        """
        验证token
        :param token: 用户注册时激活邮件中包含的url中的token
        :param expiration: token超时时间
        :return token对应的用户名
        """
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt, max_age=expiration)

    def remove_validate_token(self, token):
        """
        删除token
        :param token: 用户注册时激活邮件中包含的url中的token
        :return: token对应的用户名
        """
        serializer = utsr(self.security_key)
        return serializer.loads(token, salt=self.salt)


token_confirm = Token(django_settings.SECRET_KEY)  # 定义为全局变量


def reset_password(request, token):
    """
    激活用户
    :param request: 请求
    :param token: 用户收到邮件中的url里包含的token
    :return: 登入用户，重定向到主页
    """
    try:
        email = token_confirm.confirm_validate_token(token)
    except:
        email = token_confirm.remove_validate_token(token)
        return render(request, 'message.html', {'message': u"对不起，链接已过期，请重新找回密码"})
    try:
        user = MyUser.objects.get(email__iexact=email)
    except MyUser.DoesNotExist:
        return render(request, 'message.html', {'message': u"对不起，您所验证的用户不存在，请查正再试"})
    if request.method == "POST":
        password = request.POST['password']
        user.set_password(password)
        print(user.password)
        user.save()
        return JsonResponse({"valid": True})
    return render(request, 'demo/resetpassword.html')
