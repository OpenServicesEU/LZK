from crispy_forms.bootstrap import StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div, Field, Layout
from django import forms
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.urls import reverse_lazy as reverse

from .models import Comment


class AuthenticationForm(BaseAuthenticationForm):
    helper = FormHelper()
    helper.form_method = "POST"
    helper.form_action = reverse("login")
    helper.form_tag = True
    helper.html5_required = True
    helper.layout = Layout(
        Field("username"),
        Field("password"),
        Div(
            StrictButton("Login", css_class="btn-primary btn-block", type="submit"),
            css_class="form-group",
        ),
    )


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.form_action = reverse(
            "comment-ability",
            kwargs={"pk": kwargs.get("instance").ability.pk},
        )

    class Meta:
        model = Comment
        fields = ("comment",)

    helper = FormHelper()
    helper.form_method = "POST"
    helper.form_tag = True
    helper.html5_required = True
    helper.layout = Layout(
        Field("comment"),
        Div(
            StrictButton(
                "Submit feedback",
                css_class="btn-primary btn-block",
                type="submit",
            ),
            css_class="form-group",
        ),
    )
