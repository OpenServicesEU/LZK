from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.urls import reverse_lazy as reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from crispy_forms.bootstrap import StrictButton


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
