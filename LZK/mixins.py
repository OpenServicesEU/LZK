class FilterFormHelperMixin(object):
    def get_filterset(self, filterset_class):
        filterset = super().get_filterset(filterset_class)
        formhelper = getattr(self, "get_filterset_formhelper", None)
        if not callable(formhelper):
            return filterset
        filterset.form.helper = formhelper(filterset.form)
        return filterset
