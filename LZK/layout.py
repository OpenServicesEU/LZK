from crispy_forms.bootstrap import StrictButton


class IconButton(StrictButton):
    template = "%s/layout/iconbutton.html"

    def __init__(self, icon: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.icon = icon
