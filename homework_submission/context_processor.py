from django.conf import settings as original_settings

from submission_system.models import Courser


def coursers(request):
    cs_coursers = Courser.objects.filter(part__name="计算机部")
    ee_coursers = Courser.objects.filter(part__name="电子部")
    web_coursers = Courser.objects.filter(part__name="网络部")
    return {"cs_coursers": cs_coursers, "ee_coursers": ee_coursers, "web_coursers": web_coursers}
