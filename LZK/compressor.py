from pathlib import Path
from django_pyscss import DjangoScssCompiler
from django_pyscss.compressor import DjangoScssFilter as BaseDjangoScssFilter
from django_pyscss.extension.django import DjangoExtension
from django_libsass import SassCompiler, compile, OUTPUT_STYLE, SOURCE_COMMENTS
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage

searched_locations = finders.searched_locations


class DjangoScssFilter(BaseDjangoScssFilter):
    compiler = DjangoScssCompiler(
        output_style="compressed", extensions=(DjangoExtension,)
    )


class DjangoSassCompiler(SassCompiler):
    @staticmethod
    def importer(path, prev=None):
        # import pudb; pu.db

        # if not prev:
        #    result = finders.find(path)
        #    if result:
        #        return load(path, result)
        #    else:
        #        return None

        n = Path(path)
        p = Path(prev)
        for name in (
            n.with_suffix(".scss"),
            n.with_name(f"_{n.name}").with_suffix(".scss"),
        ):
            if p.is_absolute():
                search = str(name)
            else:
                search = str(p.parent / name)
            if not staticfiles_storage.exists(search):
                continue
            with staticfiles_storage.open(search) as content:
                return [(search, content.read())]

    def input(self, **kwargs):
        if self.filename:
            return compile(
                filename=self.filename,
                output_style=OUTPUT_STYLE,
                source_comments=SOURCE_COMMENTS,
                importers=[(0, DjangoSassCompiler.importer)],
            )
        else:
            return compile(
                string=self.content,
                output_style=OUTPUT_STYLE,
                importers=[(0, DjangoSassCompiler.importer)],
            )
