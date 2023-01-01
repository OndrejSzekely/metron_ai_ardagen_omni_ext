"""
Provides an extension of the OV Replicator distribution functions.
"""

from typing import List, Optional, Any
from pxr import Sdf
from .metron_shared import param_validators as param_val
from .utils import get_data_type


def shuffle(  # pylint: disable=unused-argument
    choices: List[str],
    seed: Optional[int] = -1,
    name: Optional[str] = None,
) -> Any:
    """
    Reshufles the list of items into a new permutation.

    Args:
        choices (List[Any]): Values in the distribution to choose from.
        seed (Optional[int]): A seed to use for the sampling.

    Returns:
        Any (og.Node): Created OmniGraph Node. Datatype can't be put in explicitly, because of the OV limitations.
    """
    param_val.check_type(choices, List[Any])
    param_val.check_type(seed, Optional[int])

    import omni.replicator.core as rep  # pylint: disable=import-outside-toplevel

    if isinstance(choices[0], Sdf.Path):
        # There is no corresponding og.BaseDataType for Sdf.Path so converted to string.
        # TODO: Refine the construct later, to avoid mypy ex: "str" has no attribute "pathString". pylint: disable=fixme
        choices = [i.pathString for i in choices]  # type: ignore

    data_type = get_data_type(choices)
    array_node = rep.utils.create_node("omni.replicator.core.OgnArray", arrayType=data_type)
    array_node.get_attribute("inputs:array").set(choices)
    # num_samples = len(choices)

    reshufle_node = rep.utils.create_node("metron.ai.ardagen.SampleShuffle", seed=seed)

    array_node.get_attribute("inputs:array").connect(reshufle_node.get_attribute("inputs:choices"), True)

    return reshufle_node


# Defines what is imported when `from distribution import *` is called.
__all__ = ["shuffle"]
