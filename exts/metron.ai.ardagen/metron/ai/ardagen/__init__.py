"""
Initialization of the package.
"""
import importlib as _importlib
import omni.replicator.core as _rep
from .extension import ArDaGenExt  # noqa: F401 (Needed for the package import)
from .ogn import *  # noqa: F401, F403 (Needed for the package import)
from .distribution import __all__ as _distribution_all


def _register_replicator_distributions() -> None:
    """
    Registers all ArDaGen Extension custom distribution functions into Replicator.
    """

    ext_dist_module = _importlib.import_module(".distribution", package=__name__)

    for dist_func_name in _distribution_all:
        dist_func = getattr(ext_dist_module, dist_func_name)
        _rep.distribution.register(dist_func)


_register_replicator_distributions()
