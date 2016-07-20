import hashlib
import re
import os
import posixpath
from collections import OrderedDict

from storages.backends.s3boto import S3BotoStorage

from django.core.cache import (
    InvalidCacheBackendError, cache as default_cache, caches,
)
from django.contrib.staticfiles.storage import CachedFilesMixin, HashedFilesMixin, _MappingCache
from django.contrib.staticfiles.utils import matches_patterns
from django.utils.encoding import force_bytes, force_text
from django.core.files.base import ContentFile
from django.conf import settings
from django.utils.six.moves.urllib.parse import unquote

class DigggerHashedFilesMixin(HashedFilesMixin):
    patterns = (
        ("*.css", (
            r"""(url\(['"]{0,1}\s*(.*?)["']{0,1}\))""",
            (r"""(@import\s*["']\s*(.*?)["'])""", """@import url("%s")"""),
        )),
        ("*.js", (
            (r"""(["'](app\/\s*.*?)['"])""", """'%s'"""),
        )),
    )

    def __init__(self, *args, **kwargs):
        super(HashedFilesMixin, self).__init__(*args, **kwargs)
        self._patterns = OrderedDict()
        self.hashed_files = {}
        for extension, patterns in self.patterns:
            for pattern in patterns:
                if isinstance(pattern, (tuple, list)):
                    pattern, template = pattern
                else:
                    template = self.default_template
                compiled = re.compile(pattern, re.IGNORECASE)
                self._patterns.setdefault(extension, []).append((compiled, template))

    def post_process(self, paths, dry_run=False, **options):
        """
        Post process the given OrderedDict of files (called from collectstatic).

        Processing is actually two separate operations:

        1. renaming files to include a hash of their content for cache-busting,
           and copying those files to the target storage.
        2. adjusting files which contain references to other files so they
           refer to the cache-busting filenames.

        If either of these are performed on a file, then that file is considered
        post-processed.
        """
        # don't even dare to process the files if we're in dry run mode
        if dry_run:
            return

        # where to store the new paths
        hashed_files = OrderedDict()

        # build a list of adjustable files
        matches = lambda path: matches_patterns(path, self._patterns.keys())
        adjustable_paths = [path for path in paths if matches(path)]

        # then sort the files by the directory level
        path_level = lambda name: len(name.split(os.sep))
        for name in sorted(paths.keys(), key=path_level, reverse=True):

            # use the original, local file, not the copied-but-unprocessed
            # file, which might be somewhere far away, like S3
            storage, path = paths[name]
            with storage.open(path) as original_file:

                # generate the hash with the original content, even for
                # adjustable files.
                hashed_name = self.hashed_name(name, original_file)

                # then get the original's file content..
                if hasattr(original_file, 'seek'):
                    original_file.seek(0)

                hashed_file_exists = self.exists(hashed_name)
                processed = False

                # ..to apply each replacement pattern to the content
                if name in adjustable_paths:
                    content = original_file.read().decode(settings.FILE_CHARSET)
                    ext = '*{}'.format(os.path.splitext(name)[1])
                    for pattern, template in self._patterns[ext]:
                        converter = self.url_converter(name, template) if ext == '*.css' else self.require_url_converter(name, template)
                        try:
                            content = pattern.sub(converter, content)
                        except ValueError as exc:
                            yield name, None, exc
                    if hashed_file_exists:
                        self.delete(hashed_name)
                    # then save the processed result
                    content_file = ContentFile(force_bytes(content))
                    saved_name = self._save(hashed_name, content_file)
                    hashed_name = force_text(self.clean_name(saved_name))
                    processed = True
                else:
                    # or handle the case in which neither processing nor
                    # a change to the original file happened
                    if not hashed_file_exists:
                        processed = True
                        saved_name = self._save(hashed_name, original_file)
                        hashed_name = force_text(self.clean_name(saved_name))

                # and then set the cache accordingly
                hashed_files[self.hash_key(name)] = hashed_name
                yield name, hashed_name, processed

        # Finally store the processed paths
        self.hashed_files.update(hashed_files)

    def require_url_converter(self, name, template=None):
        """
        Returns the custom URL converter for the given file name.
        """

        if template is None:
            template = self.default_template

        def converter(matchobj):
            """
            Converts the matched URL depending on the parent level (`..`)
            and returns the normalized and hashed URL using the url method
            of the storage.
            """

            matched, url = matchobj.groups()
            # Completely ignore http(s) prefixed URLs,
            # fragments and data-uri URLs
            joined_result = 'js/{}.js'.format(url)
            hashed_url = self.url(unquote(joined_result), force=True)
            file_name = hashed_url.split('/')[-1:]
            relative_url = '/'.join(url.split('/')[:-1] + file_name)[:-3]

            # Return the hashed version to the file
            return template % unquote(relative_url)

        return converter


class DigggerCachedFilesMixin(DigggerHashedFilesMixin):
    def __init__(self, *args, **kwargs):
        super(DigggerCachedFilesMixin, self).__init__(*args, **kwargs)
        try:
            self.hashed_files = _MappingCache(caches['staticfiles'])
        except InvalidCacheBackendError:
            # Use the default backend
            self.hashed_files = _MappingCache(default_cache)

    def hash_key(self, name):
        key = hashlib.md5(force_bytes(self.clean_name(name))).hexdigest()
        return 'staticfiles:%s' % key


class OptimizedS3BotoStorage(CachedFilesMixin, S3BotoStorage):
    location = 'static'


class MediaS3BotoStorage(S3BotoStorage):
    location = 'media'