from django.conf import settings as original_settings

from submission_system.models import Courser


def coursers(request):
    return {'coursers': Courser.objects.all()}
