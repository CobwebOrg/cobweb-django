"""
Settings for cobweb Django site.

By default use production – test and debug
environments should invoke the respective modules, which import production then
make minimal changes.
"""

from .production import *  # noqa
