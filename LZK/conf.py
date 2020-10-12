from appconf import AppConf
from django.conf import settings


class LZKAppConf(AppConf):
    class Meta:
        prefix = "LZK"
