from __future__ import absolute_import
from __future__ import unicode_literals

import inspect
import pkgutil


def discover(package, cls_match_func):
    """Returns a set of classes in the directory matched by cls_match_func

    Args:
        path - A Python package
        cls_match_func - Function taking a class and returning true if the
            class is to be included in the output.
    """
    matched_classes = set()

    for _, module_name, _ in pkgutil.walk_packages(
            package.__path__,
            prefix=package.__name__ + '.',
    ):
        module = __import__(module_name, fromlist=[str('__trash')], level=0)

        # Check all the classes in that module
        for _, imported_class in inspect.getmembers(module, inspect.isclass):
            # Don't include things that are only there due to a side-effect of
            # importing
            if imported_class.__module__ != module.__name__:
                continue

            if cls_match_func(imported_class):
                matched_classes.add(imported_class)

    return matched_classes
