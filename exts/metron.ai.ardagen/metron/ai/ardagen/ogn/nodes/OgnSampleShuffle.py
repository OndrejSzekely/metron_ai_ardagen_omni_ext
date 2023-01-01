# pylint: disable=invalid-name
"""
Implements shuffling node.
"""
import typing
import numpy as np
import omni.graph.core as og
import omni.replicator.core as rep


class OgnSampleShuffleInternalState:  # pylint: disable=too-few-public-methods
    """
    Node's internal state representation.
    """

    def __init__(self) -> None:
        self.rng = rep.rng.ReplicatorRNG()


class OgnSampleShuffle:
    """
    OGN Shuffling node.
    """

    @staticmethod
    def internal_state() -> OgnSampleShuffleInternalState:
        """
        Returns internal state.

        Returns:
            OgnSampleShuffleInternalState: Internal state class instance.
        """
        return OgnSampleShuffleInternalState()

    @staticmethod
    def release(node: typing.Any) -> None:
        """

        Args:
            node (og.Node): Node to be released.
        """
        rep.rng.release(node.get_prim_path())

    @staticmethod
    def compute(db: typing.Any) -> bool:
        """
        Compute method.

        Args:
            db (Any): Database structure.

        Returns:
            bool: Success state of the operation.
        """
        state = db.internal_state
        choices = db.inputs.choices.array_value()

        if len(choices) == 0:
            return False

        is_seed_valid = db.inputs.seed is not None
        is_seed_changed = state.rng is None or db.inputs.seed != state.rng.seed
        if is_seed_valid and is_seed_changed:
            node_id = db.inputs.nodeId if db.node.get_attribute_exists("inputs:nodeId") else 0
            state.rng.initialize(db.inputs.seed, db.node, node_id)

        shuffled = np.copy(choices)
        state.rng.generator.shuffle(shuffled, axis=0)

        db.outputs.samples = shuffled
        return True

    @staticmethod
    def initialize(graph_context: typing.Any, node: typing.Any) -> None:  # pylint: disable=unused-argument
        """
        Init method.

        Args:
            graph_context (Any): Graph context.
            node (Any): Node.
        """
        connected_function_callback = OgnSampleShuffle.on_connected_callback
        node.register_on_connected_callback(connected_function_callback)

    @staticmethod
    def on_connected_callback(upstream_attr: typing.Any, downstream_attr: typing.Any) -> None:
        """
        Connected callback.

        Args:
            upstream_attr (Any): N/A.
            downstream_attr (Any): N/A.
        """
        if downstream_attr.get_name() == "inputs:choices":
            if downstream_attr.get_resolved_type().base_type == og.BaseDataType.UNKNOWN:
                upstream_resolved_type = upstream_attr.get_resolved_type()
                if upstream_resolved_type.base_type != og.BaseDataType.UNKNOWN:
                    downstream_attr.set_resolved_type(upstream_resolved_type)

        # Resolve output attr based on the downstream attr
        if upstream_attr.get_name() == "outputs:samples":
            if upstream_attr.get_resolved_type().base_type == og.BaseDataType.UNKNOWN:
                if downstream_attr.get_resolved_type().base_type != og.BaseDataType.UNKNOWN:
                    og.AttributeValueHelper(upstream_attr).resolve_type(downstream_attr.get_resolved_type())
                else:
                    node = upstream_attr.get_node()
                    choices_attr = node.get_attribute("inputs:choices")
                    og.AttributeValueHelper(upstream_attr).resolve_type(choices_attr.get_resolved_type())
