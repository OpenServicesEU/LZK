from itertools import chain
from pathlib import Path

from django.conf import settings
from django.contrib.staticfiles import utils
from django.contrib.staticfiles.finders import BaseFinder
from django.core.checks import Error
from django.core.files.storage import FileSystemStorage


class ScopedFileSystemStorage(FileSystemStorage):
    def __init__(self, location, directory, *args, **kwargs):
        super().__init__(location, *args, **kwargs)
        self._directory = Path(directory)

    def path(self, path):
        p = Path(path)
        if (
            len(p.parts) >= len(self._directory.parts)
            and p.parts[: len(self._directory.parts)] == self._directory.parts
        ):
            parts = p.parts[len(self._directory.parts) :]
        else:
            parts = p.parts
        return str(Path(self.location).joinpath(*parts))

    def listdir(self, path):
        directories, files = [], []
        for e in Path(self.path(path)).glob("*"):
            if e.is_dir():
                directories.append(e.name)
            else:
                files.append(e.name)
        return directories, files


class SystemFinder(BaseFinder):
    def __init__(self, app_names=None, *args, **kwargs):
        self.storages = dict(
            enumerate(
                map(
                    lambda l: FileSystemStorage(location=l),
                    chain(*settings.SYSTEM_STATIC_PATHS.values()),
                )
            )
        )
        self.entries = dict(
            map(
                lambda k: (
                    Path(k),
                    [Path(p) for p in settings.SYSTEM_STATIC_PATHS.get(k)],
                ),
                settings.SYSTEM_STATIC_PATHS.keys(),
            )
        )
        super().__init__(*args, **kwargs)

    def check(self, **kwargs):
        if not isinstance(settings.SYSTEM_STATIC_PATHS, dict):
            yield Error(
                "The SYSTEM_STATIC_PATHS setting is not a dictionary.",
                hint="Perhaps you forgot to include it in your settings?",
                id=f"{__name__}.E001",
            )
        for virtual, paths in settings.SYSTEM_STATIC_PATHS.items():
            if len(virtual) == 0:
                yield Error(
                    f"Not a valid mapping for SYSTEM_STATIC_PATHS: {virtual}",
                    hint="Virtual path must not be empty.",
                    id=f"{__name__}.E002",
                )
            if not isinstance(paths, (tuple, list)):
                yield Error(
                    f"Not a valid mapping for SYSTEM_STATIC_PATHS: {virtual}",
                    hint="Local mapping paths should be defined as tuple or list.",
                    id=f"{__name__}.E003",
                )
            for path in paths:
                if not Path(path).exists():
                    yield Error(
                        f"Not a valid mapping for SYSTEM_STATIC_PATHS: {virtual}",
                        hint=f"Local path {path} does not exist.",
                        id=f"{__name__}.E004",
                    )
                if not Path(path).is_dir():
                    yield Error(
                        f"Not a valid mapping for SYSTEM_STATIC_PATHS: {virtual}",
                        hint=f"Local path {path} is not a directory.",
                        id=f"{__name__}.E005",
                    )

    def find(self, name, all=False):
        path = Path(name)
        matches = []
        for virtual, paths in self.entries.items():
            if path.parts[: len(virtual.parts)] != virtual.parts:
                continue
            for local in paths:
                match = local.joinpath(*path.parts[len(virtual.parts) :])
                if not match.exists():
                    continue
                if not all:
                    return str(match)
                matches.append(str(match))
        return matches

    def list(self, ignore_patterns):
        for virtual, paths in self.entries.items():
            for path in paths:
                storage = ScopedFileSystemStorage(
                    location=str(path), directory=str(virtual)
                )
                files = utils.get_files(storage, ignore_patterns)
                for name in files:
                    yield str(virtual / name), storage
