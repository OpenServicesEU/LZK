from appconf import AppConf
from django.conf import settings


class LZKPrivateAppConf(AppConf):
    IMPORT_SHEET_ACRONYMS = "Abkürzungen gesamt"
    IMPORT_SHEET_OBJECTIVES = "Lernziele gesamt_Datenbank"
    IMPORT_SHEET_UFIDS = "ufid_IMS_Gesamtliste 2019"
    IMPORT_VALUE_TRUE = "ja"
    IMPORT_VALUE_FALSE = "nein"
    EMAIL_FROM = None

    class Meta:
        prefix = "LZK"
