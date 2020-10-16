from appconf import AppConf
from django.conf import settings


class LZKAppConf(AppConf):
    COPYRIGHT = "Some Company"

    class Meta:
        prefix = "LZK"
