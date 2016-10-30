# coding:utf-8
from django import forms
from django.contrib import auth

from .models import MyUser
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
import base64
import logging

logger = logging.getLogger(__name__)


# 参考自django.contrib.auth.forms.UserCreationForm

class VmaigUserCreationForm(forms.ModelForm):
    # 错误信息
    error_messages = {
        'duplicate_username': u"此用户已存在.",
        'password_mismatch': u"两次密码不相同.",
        'duplicate_email': u'此email已经存在.',
        'duplicate_id_num': '用户名/学号已经注册',
        'unsuitable_length': "密码长度应该在8到16位"
    }

    username = forms.RegexField(max_length=30, regex=r'^[\w.@+-]+$',
                                # 错误信息 invalid 表示username不合法的错误信息, required 表示没填的错误信息
                                error_messages={
                                    'invalid': "该值只能包含字母、数字和字符@/./+/-/_",
                                    'required': "昵称未填"})
    email = forms.EmailField(error_messages={
        'invalid': "email格式错误",
        'required': 'email未填'})

    password1 = forms.CharField(widget=forms.PasswordInput,
                                error_messages={
                                    'required': u"密码未填",
                                    'invalid': "密码只能包含字母、数字和字符@/./+/-/_，长度8到16位"
                                })
    password2 = forms.CharField(widget=forms.PasswordInput,
                                error_messages={
                                    'required': u"确认密码未填"
                                })

    id_num = forms.CharField(max_length=20, error_messages={
        'required': "用户名/学号未填"})

    class Meta:
        model = MyUser
        fields = ("username", "email")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        # try:
        #     MyUser._default_manager.get(username=username)
        # except MyUser.DoesNotExist:
        return username
        # raise forms.ValidationError(
        #     self.error_messages["duplicate_username"]
        # )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        if len(password1) < 8 or len(password1) > 16:
            raise forms.ValidationError(
                self.error_messages["unsuitable_length"]
            )
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"]
            )
        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]

        # 判断是这个email 用户是否存在
        try:
            MyUser._default_manager.get(email=email)
        except MyUser.DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages["duplicate_email"]
        )

    def clean_id_num(self):
        id_num = self.cleaned_data['id_num']
        if id_num:
            try:
                MyUser._default_manager.get(id_num=id_num)
            except MyUser.DoesNotExist:
                return id_num
            raise forms.ValidationError(
                self.error_messages["duplicate_id_num"]
            )
        return id_num

    def save(self, commit=True):
        user = super(VmaigUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.id_num = self.cleaned_data['id_num']
        if commit:
            user.save()
        return user


class PasswordChangeForm(forms.Form):
    """
    A form that lets a user change their password by entering their old
    password.
    """

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordChangeForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user

    error_messages = {
        'all_number': "密码不能全部是数字",
        'unsuitable_length': "密码长度应该在8到16位",
        'password_mismatch': u"两次密码不相同.",
        'password_incorrect': '原密码不正确'
    }
    old_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput, error_messages={
            'required': '原密码未填'
        })

    new_password1 = forms.CharField(widget=forms.PasswordInput,
                                    error_messages={
                                        'required': u"新密码未填",
                                        'invalid': "密码只能包含字母、数字和字符@/./+/-/_，长度8到16位"
                                    })
    new_password2 = forms.CharField(widget=forms.PasswordInput,
                                    error_messages={
                                        'required': u"确认密码未填"
                                    })
    field_order = ['old_password', 'new_password1', 'new_password2']

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        if len(password1) < 8 or len(password1) > 16:
            raise forms.ValidationError(
                self.error_messages["unsuitable_length"]
            )
        if password1.isdigit():
            raise forms.ValidationError(
                self.error_messages['all_number']
            )
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages["password_mismatch"]
            )
        return password2
