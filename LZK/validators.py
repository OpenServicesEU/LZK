import mimetypes
from pathlib import PurePath
from zipfile import BadZipFile

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _
from openpyxl import load_workbook
from openpyxl.utils.exceptions import InvalidFileException


@deconstructible
class FileValidator:
    """
    Validator for files, checking the size, extension and mimetype.
    Initialization parameters:
        extensions: iterable with allowed file extensions
            ie. ('txt', 'doc')
        mimetypes: iterable with allowed mimetypes
            ie. ('image/png', )
    Usage example::
        MyModel(models.Model):
            myfile = FileField(
                validators=(
                    FileValidator(mimetypes=['audio/flac'], ...),
                ),
            )
    """

    extension_message = _(
        "Extension '%(extension)s' not allowed. Allowed extensions are: '%(extensions)s.'"
    )
    mimetype_message = _(
        "MIME type '%(mimetype)s' is not valid. Allowed types are: %(mimetypes)s."
    )

    def __init__(self, extensions=None, mimetypes=None):
        self.extensions = extensions
        self.mimetypes = mimetypes

    def __call__(self, value):
        """
        Check the extension, content type and file size.
        """

        # Check the extension
        ext = PurePath(value.name).suffix.lstrip(".")
        if self.extensions and ext not in self.extensions:
            message = self.extension_message % {
                "extension": ext,
                "extensions": ", ".join(self.extensions),
            }

            raise ValidationError(message)

        # Check the content type
        mimetype, _ = mimetypes.guess_type(value.name)
        if mimetype and self.mimetypes and mimetype not in self.mimetypes:
            message = self.mimetype_message % {
                "mimetype": mimetype,
                "mimetypes": ", ".join(self.mimetypes),
            }

            raise ValidationError(message)


@deconstructible
class XlsxFileValidator:
    """
    Validator for files, checking if it can be loaded using openpyxl.
    Usage example::
        MyModel(models.Model):
            myfile = FileField(
                validators=(
                    XlsxFileValidator(sheets=['name of sheet', ...]),
                ),
            )
    """

    def __init__(self, sheets=None):
        self.sheets = sheets

    def __call__(self, value):
        """
        Try to open the file and scan for sheets if required.
        """
        try:
            wb = load_workbook(value, read_only=True, keep_links=False, data_only=True)
            if self.sheets:
                for s in self.sheets:
                    try:
                        wb.get_sheet_by_name(s)
                    except KeyError as e:
                        raise ValidationError(
                            _("Document does not contain a sheet named {s}.").format(
                                s=s
                            )
                        ) from e
        except (BadZipFile, InvalidFileException) as e:
            raise ValidationError(_("File is no a valid XLS document.")) from e
