"""
A data layer for the Elemental CMS.
"""

import os
from setuptools import setup


HERE = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(HERE, 'README.md'), 'r') as f:
    __long_description__ = f.read()

__on_rtd__ = os.environ.get('READTHEDOCS', None) == 'True'

__project__ = 'elemental-client'

__version__ = '0.2'

__release__ = '0.2.0dev0'

__classifiers__ = [
    'Development Status :: 1 - Planning',
    'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
    'Intended Audience :: Developers',
    'Environment :: Web Environment'
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

__author__ = 'Matt Robinson'

__author_email__ = 'matt@technicalartisan.com'

__url__ = 'https://github.com/artPlusPlus/elemental-client'

__license__ = [
    c.rsplit('::', 1)[1].strip()
    for c in __classifiers__
    if c.startswith('License ::')
][0]

__keywords__ = [
    'elemental',
    'cms',
    'client'
]

__packages__ = [
    'elemental_client'
]

__platforms__ = 'ALL'

__requires__ = [
    'requests',
    'elemental-core',
    'elemental-kinds'
]

__test_suite__ = 'tests'

__tests_require__ = [
    'pytest'
]

__extra_requires__ = {
    'doc': ['sphinx>=1.3.0']
}

__entry_points__ = {}


def main():
    setup(
        name                = __project__,
        version             = __version__,
        description         = __doc__,
        long_description    = __long_description__,
        classifiers         = __classifiers__,
        author              = __author__,
        author_email        = __author_email__,
        url                 = __url__,
        license             = __license__,
        keywords            = __keywords__,
        packages            = __packages__,
        platforms           = __platforms__,
        test_suite          = __test_suite__,
        tests_require       = __tests_require__,
        install_requires    = __requires__,
        extras_require      = __extra_requires__,
        entry_points        = __entry_points__
    )


if __name__ == '__main__':
    main()
