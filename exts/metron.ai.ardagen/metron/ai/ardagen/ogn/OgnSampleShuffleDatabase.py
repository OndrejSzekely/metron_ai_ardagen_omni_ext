"""Support for simplified access to data on nodes of type metron.ai.ardagen.SampleShuffle

This node shuffles samples from a list of strings/tokens.
"""

import omni.graph.core as og
import omni.graph.core._omni_graph_core as _og
import omni.graph.tools.ogn as ogn
import traceback
from typing import Any
import sys


class OgnSampleShuffleDatabase(og.Database):
    """Helper class providing simplified access to data on nodes of type metron.ai.ardagen.SampleShuffle

    Class Members:
        node: Node being evaluated

    Attribute Value Properties:
        Inputs:
            inputs.choices
            inputs.seed
        Outputs:
            outputs.samples
    """

    # This is an internal object that provides per-class storage of a per-node data dictionary
    PER_NODE_DATA = {}
    # This is an internal object that describes unchanging attributes in a generic way
    # The values in this list are in no particular order, as a per-attribute tuple
    #     Name, Type, ExtendedTypeIndex, UiName, Description, Metadata,
    #     Is_Required, DefaultValue, Is_Deprecated, DeprecationMsg
    # You should not need to access any of this data directly, use the defined database interfaces
    INTERFACE = og.Database._get_interface(
        [
            ("inputs:choices", "any", 2, None, "The choices to be sampled", {}, True, None, False, ""),
            (
                "inputs:seed",
                "int",
                0,
                None,
                "Random Number Generator seed. A value of less than 0 will indicate using the global seed.",
                {ogn.MetadataKeys.DEFAULT: "-1"},
                True,
                -1,
                False,
                "",
            ),
            ("outputs:samples", "any", 2, None, "Shuffled results", {}, True, None, False, ""),
        ]
    )

    class ValuesForInputs(og.DynamicAttributeAccess):
        LOCAL_PROPERTY_NAMES = {"seed", "_setting_locked", "_batchedReadAttributes", "_batchedReadValues"}
        """Helper class that creates natural hierarchical access to input attributes"""

        def __init__(self, node: og.Node, attributes, dynamic_attributes: og.DynamicAttributeInterface):
            """Initialize simplified access for the attribute data"""
            context = node.get_graph().get_default_graph_context()
            super().__init__(context, node, attributes, dynamic_attributes)
            self._batchedReadAttributes = [self._attributes.seed]
            self._batchedReadValues = [-1]

        @property
        def choices(self) -> og.RuntimeAttribute:
            """Get the runtime wrapper class for the attribute inputs.choices"""
            return og.RuntimeAttribute(self._attributes.choices.get_attribute_data(), self._context, True)

        @choices.setter
        def choices(self, value_to_set: Any):
            """Assign another attribute's value to outputs.choices"""
            if isinstance(value_to_set, og.RuntimeAttribute):
                self.choices.value = value_to_set.value
            else:
                self.choices.value = value_to_set

        @property
        def seed(self):
            return self._batchedReadValues[0]

        @seed.setter
        def seed(self, value):
            self._batchedReadValues[0] = value

        def __getattr__(self, item: str):
            if item in self.LOCAL_PROPERTY_NAMES:
                return object.__getattribute__(self, item)
            else:
                return super().__getattr__(item)

        def __setattr__(self, item: str, new_value):
            if item in self.LOCAL_PROPERTY_NAMES:
                object.__setattr__(self, item, new_value)
            else:
                super().__setattr__(item, new_value)

        def _prefetch(self):
            readAttributes = self._batchedReadAttributes
            newValues = _og._prefetch_input_attributes_data(readAttributes)
            if len(readAttributes) == len(newValues):
                self._batchedReadValues = newValues

    class ValuesForOutputs(og.DynamicAttributeAccess):
        LOCAL_PROPERTY_NAMES = {}
        """Helper class that creates natural hierarchical access to output attributes"""

        def __init__(self, node: og.Node, attributes, dynamic_attributes: og.DynamicAttributeInterface):
            """Initialize simplified access for the attribute data"""
            context = node.get_graph().get_default_graph_context()
            super().__init__(context, node, attributes, dynamic_attributes)
            self._batchedWriteValues = {}

        @property
        def samples(self) -> og.RuntimeAttribute:
            """Get the runtime wrapper class for the attribute outputs.samples"""
            return og.RuntimeAttribute(self._attributes.samples.get_attribute_data(), self._context, False)

        @samples.setter
        def samples(self, value_to_set: Any):
            """Assign another attribute's value to outputs.samples"""
            if isinstance(value_to_set, og.RuntimeAttribute):
                self.samples.value = value_to_set.value
            else:
                self.samples.value = value_to_set

        def _commit(self):
            _og._commit_output_attributes_data(self._batchedWriteValues)
            self._batchedWriteValues = {}

    class ValuesForState(og.DynamicAttributeAccess):
        """Helper class that creates natural hierarchical access to state attributes"""

        def __init__(self, node: og.Node, attributes, dynamic_attributes: og.DynamicAttributeInterface):
            """Initialize simplified access for the attribute data"""
            context = node.get_graph().get_default_graph_context()
            super().__init__(context, node, attributes, dynamic_attributes)

    def __init__(self, node):
        super().__init__(node)
        dynamic_attributes = self.dynamic_attribute_data(node, og.AttributePortType.ATTRIBUTE_PORT_TYPE_INPUT)
        self.inputs = OgnSampleShuffleDatabase.ValuesForInputs(node, self.attributes.inputs, dynamic_attributes)
        dynamic_attributes = self.dynamic_attribute_data(node, og.AttributePortType.ATTRIBUTE_PORT_TYPE_OUTPUT)
        self.outputs = OgnSampleShuffleDatabase.ValuesForOutputs(node, self.attributes.outputs, dynamic_attributes)
        dynamic_attributes = self.dynamic_attribute_data(node, og.AttributePortType.ATTRIBUTE_PORT_TYPE_STATE)
        self.state = OgnSampleShuffleDatabase.ValuesForState(node, self.attributes.state, dynamic_attributes)

    class abi:
        """Class defining the ABI interface for the node type"""

        @staticmethod
        def get_node_type():
            get_node_type_function = getattr(OgnSampleShuffleDatabase.NODE_TYPE_CLASS, "get_node_type", None)
            if callable(get_node_type_function):
                return get_node_type_function()
            return "metron.ai.ardagen.SampleShuffle"

        @staticmethod
        def compute(context, node):
            try:
                per_node_data = OgnSampleShuffleDatabase.PER_NODE_DATA[node.node_id()]
                db = per_node_data.get("_db")
                if db is None:
                    db = OgnSampleShuffleDatabase(node)
                    per_node_data["_db"] = db
            except:
                db = OgnSampleShuffleDatabase(node)

            try:
                if db.inputs.choices.type.base_type == og.BaseDataType.UNKNOWN:
                    db.log_warning("Required extended attribute inputs:choices is not resolved, compute skipped")
                    return False
                if db.outputs.samples.type.base_type == og.BaseDataType.UNKNOWN:
                    db.log_warning("Required extended attribute outputs:samples is not resolved, compute skipped")
                    return False
                compute_function = getattr(OgnSampleShuffleDatabase.NODE_TYPE_CLASS, "compute", None)
                if callable(compute_function) and compute_function.__code__.co_argcount > 1:
                    return compute_function(context, node)

                db.inputs._prefetch()
                db.inputs._setting_locked = True
                with og.in_compute():
                    return OgnSampleShuffleDatabase.NODE_TYPE_CLASS.compute(db)
            except Exception as error:
                stack_trace = "".join(traceback.format_tb(sys.exc_info()[2].tb_next))
                db.log_error(f"Assertion raised in compute - {error}\n{stack_trace}", add_context=False)
            finally:
                db.inputs._setting_locked = False
                db.outputs._commit()
            return False

        @staticmethod
        def initialize(context, node):
            OgnSampleShuffleDatabase._initialize_per_node_data(node)
            initialize_function = getattr(OgnSampleShuffleDatabase.NODE_TYPE_CLASS, "initialize", None)
            if callable(initialize_function):
                initialize_function(context, node)

        @staticmethod
        def release(node):
            release_function = getattr(OgnSampleShuffleDatabase.NODE_TYPE_CLASS, "release", None)
            if callable(release_function):
                release_function(node)
            OgnSampleShuffleDatabase._release_per_node_data(node)

        @staticmethod
        def update_node_version(context, node, old_version, new_version):
            update_node_version_function = getattr(
                OgnSampleShuffleDatabase.NODE_TYPE_CLASS, "update_node_version", None
            )
            if callable(update_node_version_function):
                return update_node_version_function(context, node, old_version, new_version)
            return False

        @staticmethod
        def initialize_type(node_type):
            initialize_type_function = getattr(OgnSampleShuffleDatabase.NODE_TYPE_CLASS, "initialize_type", None)
            needs_initializing = True
            if callable(initialize_type_function):
                needs_initializing = initialize_type_function(node_type)
            if needs_initializing:
                node_type.set_metadata(ogn.MetadataKeys.EXTENSION, "metron.ai.ardagen")
                node_type.set_metadata(ogn.MetadataKeys.UI_NAME, "Shuffling Distribution")
                node_type.set_metadata(ogn.MetadataKeys.CATEGORIES, "Replicator:Core")
                node_type.set_metadata(ogn.MetadataKeys.CATEGORY_DESCRIPTIONS, "Replicator:Core,Core Replicator nodes")
                node_type.set_metadata(
                    ogn.MetadataKeys.DESCRIPTION, "This node shuffles samples from a list of strings/tokens."
                )
                node_type.set_metadata(ogn.MetadataKeys.LANGUAGE, "Python")
                __hints = node_type.get_scheduling_hints()
                if __hints is not None:
                    __hints.compute_rule = og.eComputeRule.E_ON_REQUEST
                OgnSampleShuffleDatabase.INTERFACE.add_to_node_type(node_type)
                node_type.set_has_state(True)

        @staticmethod
        def on_connection_type_resolve(node):
            on_connection_type_resolve_function = getattr(
                OgnSampleShuffleDatabase.NODE_TYPE_CLASS, "on_connection_type_resolve", None
            )
            if callable(on_connection_type_resolve_function):
                on_connection_type_resolve_function(node)

    NODE_TYPE_CLASS = None
    GENERATOR_VERSION = (1, 17, 0)
    TARGET_VERSION = (2, 64, 7)

    @staticmethod
    def register(node_type_class):
        OgnSampleShuffleDatabase.NODE_TYPE_CLASS = node_type_class
        og.register_node_type(OgnSampleShuffleDatabase.abi, 1)

    @staticmethod
    def deregister():
        og.deregister_node_type("metron.ai.ardagen.SampleShuffle")
