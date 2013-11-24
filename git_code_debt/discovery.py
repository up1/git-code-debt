
from git_code_debt.metrics.base import DiffParserBase
from git_code_debt_util.discovery import discover

def is_metric_cls(cls):
    """A metric class is defined as follows:

        - It inherits DiffParserBase
        - It is not DiffParserBase
        - It does not have __metric__ = False
    """
    return (
        cls is not DiffParserBase and
        cls.__dict__.get('__metric__', True) and
        issubclass(cls, DiffParserBase)
    )

def get_metric_parsers(metrics_packages=tuple(), include_defaults=True):
    """Gets all of the metric parsers.

    Args:
        metrics_packages - Defaults to no extra packages. An iterable of
            metric containing packages.  A metric inherits DiffParserBase
            and does not have __metric__ = False
            A metric package must be imported using import a.b.c
        include_defaults - Whether to include the generic metric parsers
    """
    metric_parsers = set()

    if include_defaults:
        import git_code_debt.metrics
        metric_parsers.update(discover(git_code_debt.metrics, is_metric_cls))

    for metrics_package in metrics_packages:
        metric_parsers.update(discover(metrics_package, is_metric_cls))
    return metric_parsers

