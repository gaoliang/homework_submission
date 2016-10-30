from django.conf.urls import url
from django.views.generic import TemplateView

from auth_system.views import UserControl, Confirm, login, register, forget_password,reset_password
from auth_system.views import logout

urlpatterns = [
    url(r'^confirm/(?P<slug>\w+)', Confirm.as_view(), name='confirm'),
    url(r'^login/', login, name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^changepassword/$', TemplateView.as_view(template_name="demo/changepassword.html"), name='change_password'),
    url(r'^forgetpassword/$', forget_password, name='forget_password'),
    url(r'^resetpassword/(?P<token>\w+.[-_\w]*\w+.[-_\w]*\w+)/$', reset_password, name='reset_password'),
    url(r'^data/(?P<slug>\w+)$', UserControl.as_view(), name='data'),
]
