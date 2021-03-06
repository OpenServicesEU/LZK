from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout
from django import forms
from django.urls import reverse_lazy as reverse

from LZK.layout import IconButton

from .. import models
from ..validators import FileValidator, XlsxFileValidator
from .conf import settings


class ImportForm(forms.Form):
    file = forms.FileField(
        validators=[
            FileValidator(
                extensions=[
                    "xlsx",
                    "xlsm",
                ],
                mimetypes=[
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    "application/vnd.ms-excel.sheet.macroEnabled.12",
                ],
            ),
            XlsxFileValidator(
                sheets=[
                    settings.LZK_IMPORT_SHEET_ACRONYMS,
                    settings.LZK_IMPORT_SHEET_OBJECTIVES,
                    settings.LZK_IMPORT_SHEET_UFIDS,
                ]
            ),
        ]
    )

    helper = FormHelper()
    helper.form_method = "POST"
    helper.form_action = reverse("private:import")
    helper.form_tag = True
    helper.html5_required = True
    helper.layout = Layout(
        Field("file"),
        Div(
            IconButton(
                "fa fa-upload",
                "Import",
                css_class="btn-primary btn-block",
                type="submit",
            ),
            css_class="form-group",
        ),
    )


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = models.Feedback
        fields = (
            "university",
            "subjects",
            "activities",
        )

    helper = FormHelper()
    helper.form_method = "POST"
    helper.form_action = reverse("private:feedback-create")
    helper.form_tag = True
    helper.html5_required = True
    helper.layout = Layout(
        Field("university"),
        Field("subjects"),
        Field("activities"),
        Div(
            IconButton(
                "fa fa-paper-plane-o",
                "Send request for feedback",
                css_class="btn-primary btn-block",
                type="submit",
            ),
            css_class="form-group",
        ),
    )
