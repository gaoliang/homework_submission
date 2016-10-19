from django.conf.urls import url
from django.views.generic import TemplateView

from auth_system.views import UserControl

urlpatterns = [
    url(r'^login/', TemplateView.as_view(template_name="demo/login.html"), name='login'),
    url(r'^register/$', TemplateView.as_view(template_name="demo/register.html"), name='register'),
    url(r'^changepassword/$', TemplateView.as_view(template_name="demo/changepassword.html"), name='change_password'),
    url(r'^forgetpassword/$', TemplateView.as_view(template_name="demo/forgetpassword.html"), name='forget_password'),
    url(r'^resetpassword/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        TemplateView.as_view(template_name="demo/resetpassword.html")),
    url(r'^data/(?P<slug>\w+)$', UserControl.as_view(), name='data'),
]
