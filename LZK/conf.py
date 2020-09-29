from django.conf import settings
from appconf import AppConf


class LZKAppConf(AppConf):
    IMPORT_SHEET_ACRONYMS = "Abkürzungen gesamt"
    IMPORT_SHEET_OBJECTIVES = "Lernziele gesamt_Datenbank"
    IMPORT_SHEET_UFIDS = "ufid_IMS_Gesamtliste 2019"
    IMPORT_VALUE_TRUE = "ja"
    IMPORT_VALUE_FALSE = "nein"

    class Meta:
        prefix = "LZK"
