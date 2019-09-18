# -*- coding: utf-8 -*-

"""
Utility methods for MongoDB ORM, built on top of mongoengine.
"""


from ._version import __version__

__short_description__ = "Utility methods for MongoDB ORM, built on top of mongoengine."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__maintainer__ = "Sanhe Hu"
__maintainer_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"


try:
    from .document import ExtendedDocument
except ImportError:  # pragma: no cover
    pass