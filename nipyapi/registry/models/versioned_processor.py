# coding: utf-8

"""
    Apache NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 1.23.2
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class VersionedProcessor(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """


    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'identifier': 'str',
        'instance_identifier': 'str',
        'name': 'str',
        'comments': 'str',
        'position': 'Position',
        'type': 'str',
        'bundle': 'Bundle',
        'properties': 'dict(str, str)',
        'property_descriptors': 'dict(str, VersionedPropertyDescriptor)',
        'style': 'dict(str, str)',
        'annotation_data': 'str',
        'scheduling_period': 'str',
        'scheduling_strategy': 'str',
        'execution_node': 'str',
        'penalty_duration': 'str',
        'yield_duration': 'str',
        'bulletin_level': 'str',
        'run_duration_millis': 'int',
        'concurrently_schedulable_task_count': 'int',
        'auto_terminated_relationships': 'list[str]',
        'scheduled_state': 'str',
        'retry_count': 'int',
        'retried_relationships': 'list[str]',
        'backoff_mechanism': 'str',
        'max_backoff_period': 'str',
        'component_type': 'str',
        'group_identifier': 'str'
    }

    attribute_map = {
        'identifier': 'identifier',
        'instance_identifier': 'instanceIdentifier',
        'name': 'name',
        'comments': 'comments',
        'position': 'position',
        'type': 'type',
        'bundle': 'bundle',
        'properties': 'properties',
        'property_descriptors': 'propertyDescriptors',
        'style': 'style',
        'annotation_data': 'annotationData',
        'scheduling_period': 'schedulingPeriod',
        'scheduling_strategy': 'schedulingStrategy',
        'execution_node': 'executionNode',
        'penalty_duration': 'penaltyDuration',
        'yield_duration': 'yieldDuration',
        'bulletin_level': 'bulletinLevel',
        'run_duration_millis': 'runDurationMillis',
        'concurrently_schedulable_task_count': 'concurrentlySchedulableTaskCount',
        'auto_terminated_relationships': 'autoTerminatedRelationships',
        'scheduled_state': 'scheduledState',
        'retry_count': 'retryCount',
        'retried_relationships': 'retriedRelationships',
        'backoff_mechanism': 'backoffMechanism',
        'max_backoff_period': 'maxBackoffPeriod',
        'component_type': 'componentType',
        'group_identifier': 'groupIdentifier'
    }

    def __init__(self, identifier=None, instance_identifier=None, name=None, comments=None, position=None, type=None, bundle=None, properties=None, property_descriptors=None, style=None, annotation_data=None, scheduling_period=None, scheduling_strategy=None, execution_node=None, penalty_duration=None, yield_duration=None, bulletin_level=None, run_duration_millis=None, concurrently_schedulable_task_count=None, auto_terminated_relationships=None, scheduled_state=None, retry_count=None, retried_relationships=None, backoff_mechanism=None, max_backoff_period=None, component_type=None, group_identifier=None):
        """
        VersionedProcessor - a model defined in Swagger
        """

        self._identifier = None
        self._instance_identifier = None
        self._name = None
        self._comments = None
        self._position = None
        self._type = None
        self._bundle = None
        self._properties = None
        self._property_descriptors = None
        self._style = None
        self._annotation_data = None
        self._scheduling_period = None
        self._scheduling_strategy = None
        self._execution_node = None
        self._penalty_duration = None
        self._yield_duration = None
        self._bulletin_level = None
        self._run_duration_millis = None
        self._concurrently_schedulable_task_count = None
        self._auto_terminated_relationships = None
        self._scheduled_state = None
        self._retry_count = None
        self._retried_relationships = None
        self._backoff_mechanism = None
        self._max_backoff_period = None
        self._component_type = None
        self._group_identifier = None

        if identifier is not None:
          self.identifier = identifier
        if instance_identifier is not None:
          self.instance_identifier = instance_identifier
        if name is not None:
          self.name = name
        if comments is not None:
          self.comments = comments
        if position is not None:
          self.position = position
        if type is not None:
          self.type = type
        if bundle is not None:
          self.bundle = bundle
        if properties is not None:
          self.properties = properties
        if property_descriptors is not None:
          self.property_descriptors = property_descriptors
        if style is not None:
          self.style = style
        if annotation_data is not None:
          self.annotation_data = annotation_data
        if scheduling_period is not None:
          self.scheduling_period = scheduling_period
        if scheduling_strategy is not None:
          self.scheduling_strategy = scheduling_strategy
        if execution_node is not None:
          self.execution_node = execution_node
        if penalty_duration is not None:
          self.penalty_duration = penalty_duration
        if yield_duration is not None:
          self.yield_duration = yield_duration
        if bulletin_level is not None:
          self.bulletin_level = bulletin_level
        if run_duration_millis is not None:
          self.run_duration_millis = run_duration_millis
        if concurrently_schedulable_task_count is not None:
          self.concurrently_schedulable_task_count = concurrently_schedulable_task_count
        if auto_terminated_relationships is not None:
          self.auto_terminated_relationships = auto_terminated_relationships
        if scheduled_state is not None:
          self.scheduled_state = scheduled_state
        if retry_count is not None:
          self.retry_count = retry_count
        if retried_relationships is not None:
          self.retried_relationships = retried_relationships
        if backoff_mechanism is not None:
          self.backoff_mechanism = backoff_mechanism
        if max_backoff_period is not None:
          self.max_backoff_period = max_backoff_period
        if component_type is not None:
          self.component_type = component_type
        if group_identifier is not None:
          self.group_identifier = group_identifier

    @property
    def identifier(self):
        """
        Gets the identifier of this VersionedProcessor.
        The component's unique identifier

        :return: The identifier of this VersionedProcessor.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this VersionedProcessor.
        The component's unique identifier

        :param identifier: The identifier of this VersionedProcessor.
        :type: str
        """

        self._identifier = identifier

    @property
    def instance_identifier(self):
        """
        Gets the instance_identifier of this VersionedProcessor.
        The instance ID of an existing component that is described by this VersionedComponent, or null if this is not mapped to an instantiated component

        :return: The instance_identifier of this VersionedProcessor.
        :rtype: str
        """
        return self._instance_identifier

    @instance_identifier.setter
    def instance_identifier(self, instance_identifier):
        """
        Sets the instance_identifier of this VersionedProcessor.
        The instance ID of an existing component that is described by this VersionedComponent, or null if this is not mapped to an instantiated component

        :param instance_identifier: The instance_identifier of this VersionedProcessor.
        :type: str
        """

        self._instance_identifier = instance_identifier

    @property
    def name(self):
        """
        Gets the name of this VersionedProcessor.
        The component's name

        :return: The name of this VersionedProcessor.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this VersionedProcessor.
        The component's name

        :param name: The name of this VersionedProcessor.
        :type: str
        """

        self._name = name

    @property
    def comments(self):
        """
        Gets the comments of this VersionedProcessor.
        The user-supplied comments for the component

        :return: The comments of this VersionedProcessor.
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """
        Sets the comments of this VersionedProcessor.
        The user-supplied comments for the component

        :param comments: The comments of this VersionedProcessor.
        :type: str
        """

        self._comments = comments

    @property
    def position(self):
        """
        Gets the position of this VersionedProcessor.
        The component's position on the graph

        :return: The position of this VersionedProcessor.
        :rtype: Position
        """
        return self._position

    @position.setter
    def position(self, position):
        """
        Sets the position of this VersionedProcessor.
        The component's position on the graph

        :param position: The position of this VersionedProcessor.
        :type: Position
        """

        self._position = position

    @property
    def type(self):
        """
        Gets the type of this VersionedProcessor.
        The type of the extension component

        :return: The type of this VersionedProcessor.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this VersionedProcessor.
        The type of the extension component

        :param type: The type of this VersionedProcessor.
        :type: str
        """

        self._type = type

    @property
    def bundle(self):
        """
        Gets the bundle of this VersionedProcessor.
        Information about the bundle from which the component came

        :return: The bundle of this VersionedProcessor.
        :rtype: Bundle
        """
        return self._bundle

    @bundle.setter
    def bundle(self, bundle):
        """
        Sets the bundle of this VersionedProcessor.
        Information about the bundle from which the component came

        :param bundle: The bundle of this VersionedProcessor.
        :type: Bundle
        """

        self._bundle = bundle

    @property
    def properties(self):
        """
        Gets the properties of this VersionedProcessor.
        The properties for the component. Properties whose value is not set will only contain the property name.

        :return: The properties of this VersionedProcessor.
        :rtype: dict(str, str)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this VersionedProcessor.
        The properties for the component. Properties whose value is not set will only contain the property name.

        :param properties: The properties of this VersionedProcessor.
        :type: dict(str, str)
        """

        self._properties = properties

    @property
    def property_descriptors(self):
        """
        Gets the property_descriptors of this VersionedProcessor.
        The property descriptors for the component.

        :return: The property_descriptors of this VersionedProcessor.
        :rtype: dict(str, VersionedPropertyDescriptor)
        """
        return self._property_descriptors

    @property_descriptors.setter
    def property_descriptors(self, property_descriptors):
        """
        Sets the property_descriptors of this VersionedProcessor.
        The property descriptors for the component.

        :param property_descriptors: The property_descriptors of this VersionedProcessor.
        :type: dict(str, VersionedPropertyDescriptor)
        """

        self._property_descriptors = property_descriptors

    @property
    def style(self):
        """
        Gets the style of this VersionedProcessor.
        Stylistic data for rendering in a UI

        :return: The style of this VersionedProcessor.
        :rtype: dict(str, str)
        """
        return self._style

    @style.setter
    def style(self, style):
        """
        Sets the style of this VersionedProcessor.
        Stylistic data for rendering in a UI

        :param style: The style of this VersionedProcessor.
        :type: dict(str, str)
        """

        self._style = style

    @property
    def annotation_data(self):
        """
        Gets the annotation_data of this VersionedProcessor.
        The annotation data for the processor used to relay configuration between a custom UI and the procesosr.

        :return: The annotation_data of this VersionedProcessor.
        :rtype: str
        """
        return self._annotation_data

    @annotation_data.setter
    def annotation_data(self, annotation_data):
        """
        Sets the annotation_data of this VersionedProcessor.
        The annotation data for the processor used to relay configuration between a custom UI and the procesosr.

        :param annotation_data: The annotation_data of this VersionedProcessor.
        :type: str
        """

        self._annotation_data = annotation_data

    @property
    def scheduling_period(self):
        """
        Gets the scheduling_period of this VersionedProcessor.
        The frequency with which to schedule the processor. The format of the value will depend on th value of schedulingStrategy.

        :return: The scheduling_period of this VersionedProcessor.
        :rtype: str
        """
        return self._scheduling_period

    @scheduling_period.setter
    def scheduling_period(self, scheduling_period):
        """
        Sets the scheduling_period of this VersionedProcessor.
        The frequency with which to schedule the processor. The format of the value will depend on th value of schedulingStrategy.

        :param scheduling_period: The scheduling_period of this VersionedProcessor.
        :type: str
        """

        self._scheduling_period = scheduling_period

    @property
    def scheduling_strategy(self):
        """
        Gets the scheduling_strategy of this VersionedProcessor.
        Indicates whether the processor should be scheduled to run in event or timer driven mode.

        :return: The scheduling_strategy of this VersionedProcessor.
        :rtype: str
        """
        return self._scheduling_strategy

    @scheduling_strategy.setter
    def scheduling_strategy(self, scheduling_strategy):
        """
        Sets the scheduling_strategy of this VersionedProcessor.
        Indicates whether the processor should be scheduled to run in event or timer driven mode.

        :param scheduling_strategy: The scheduling_strategy of this VersionedProcessor.
        :type: str
        """

        self._scheduling_strategy = scheduling_strategy

    @property
    def execution_node(self):
        """
        Gets the execution_node of this VersionedProcessor.
        Indicates the node where the process will execute.

        :return: The execution_node of this VersionedProcessor.
        :rtype: str
        """
        return self._execution_node

    @execution_node.setter
    def execution_node(self, execution_node):
        """
        Sets the execution_node of this VersionedProcessor.
        Indicates the node where the process will execute.

        :param execution_node: The execution_node of this VersionedProcessor.
        :type: str
        """

        self._execution_node = execution_node

    @property
    def penalty_duration(self):
        """
        Gets the penalty_duration of this VersionedProcessor.
        The amout of time that is used when the process penalizes a flowfile.

        :return: The penalty_duration of this VersionedProcessor.
        :rtype: str
        """
        return self._penalty_duration

    @penalty_duration.setter
    def penalty_duration(self, penalty_duration):
        """
        Sets the penalty_duration of this VersionedProcessor.
        The amout of time that is used when the process penalizes a flowfile.

        :param penalty_duration: The penalty_duration of this VersionedProcessor.
        :type: str
        """

        self._penalty_duration = penalty_duration

    @property
    def yield_duration(self):
        """
        Gets the yield_duration of this VersionedProcessor.
        The amount of time that must elapse before this processor is scheduled again after yielding.

        :return: The yield_duration of this VersionedProcessor.
        :rtype: str
        """
        return self._yield_duration

    @yield_duration.setter
    def yield_duration(self, yield_duration):
        """
        Sets the yield_duration of this VersionedProcessor.
        The amount of time that must elapse before this processor is scheduled again after yielding.

        :param yield_duration: The yield_duration of this VersionedProcessor.
        :type: str
        """

        self._yield_duration = yield_duration

    @property
    def bulletin_level(self):
        """
        Gets the bulletin_level of this VersionedProcessor.
        The level at which the processor will report bulletins.

        :return: The bulletin_level of this VersionedProcessor.
        :rtype: str
        """
        return self._bulletin_level

    @bulletin_level.setter
    def bulletin_level(self, bulletin_level):
        """
        Sets the bulletin_level of this VersionedProcessor.
        The level at which the processor will report bulletins.

        :param bulletin_level: The bulletin_level of this VersionedProcessor.
        :type: str
        """

        self._bulletin_level = bulletin_level

    @property
    def run_duration_millis(self):
        """
        Gets the run_duration_millis of this VersionedProcessor.
        The run duration for the processor in milliseconds.

        :return: The run_duration_millis of this VersionedProcessor.
        :rtype: int
        """
        return self._run_duration_millis

    @run_duration_millis.setter
    def run_duration_millis(self, run_duration_millis):
        """
        Sets the run_duration_millis of this VersionedProcessor.
        The run duration for the processor in milliseconds.

        :param run_duration_millis: The run_duration_millis of this VersionedProcessor.
        :type: int
        """

        self._run_duration_millis = run_duration_millis

    @property
    def concurrently_schedulable_task_count(self):
        """
        Gets the concurrently_schedulable_task_count of this VersionedProcessor.
        The number of tasks that should be concurrently schedule for the processor. If the processor doesn't allow parallol processing then any positive input will be ignored.

        :return: The concurrently_schedulable_task_count of this VersionedProcessor.
        :rtype: int
        """
        return self._concurrently_schedulable_task_count

    @concurrently_schedulable_task_count.setter
    def concurrently_schedulable_task_count(self, concurrently_schedulable_task_count):
        """
        Sets the concurrently_schedulable_task_count of this VersionedProcessor.
        The number of tasks that should be concurrently schedule for the processor. If the processor doesn't allow parallol processing then any positive input will be ignored.

        :param concurrently_schedulable_task_count: The concurrently_schedulable_task_count of this VersionedProcessor.
        :type: int
        """

        self._concurrently_schedulable_task_count = concurrently_schedulable_task_count

    @property
    def auto_terminated_relationships(self):
        """
        Gets the auto_terminated_relationships of this VersionedProcessor.
        The names of all relationships that cause a flow file to be terminated if the relationship is not connected elsewhere. This property differs from the 'isAutoTerminate' property of the RelationshipDTO in that the RelationshipDTO is meant to depict the current configuration, whereas this property can be set in a DTO when updating a Processor in order to change which Relationships should be auto-terminated.

        :return: The auto_terminated_relationships of this VersionedProcessor.
        :rtype: list[str]
        """
        return self._auto_terminated_relationships

    @auto_terminated_relationships.setter
    def auto_terminated_relationships(self, auto_terminated_relationships):
        """
        Sets the auto_terminated_relationships of this VersionedProcessor.
        The names of all relationships that cause a flow file to be terminated if the relationship is not connected elsewhere. This property differs from the 'isAutoTerminate' property of the RelationshipDTO in that the RelationshipDTO is meant to depict the current configuration, whereas this property can be set in a DTO when updating a Processor in order to change which Relationships should be auto-terminated.

        :param auto_terminated_relationships: The auto_terminated_relationships of this VersionedProcessor.
        :type: list[str]
        """

        self._auto_terminated_relationships = auto_terminated_relationships

    @property
    def scheduled_state(self):
        """
        Gets the scheduled_state of this VersionedProcessor.
        The scheduled state of the component

        :return: The scheduled_state of this VersionedProcessor.
        :rtype: str
        """
        return self._scheduled_state

    @scheduled_state.setter
    def scheduled_state(self, scheduled_state):
        """
        Sets the scheduled_state of this VersionedProcessor.
        The scheduled state of the component

        :param scheduled_state: The scheduled_state of this VersionedProcessor.
        :type: str
        """
        allowed_values = ["ENABLED", "DISABLED", "RUNNING"]
        if scheduled_state not in allowed_values:
            raise ValueError(
                "Invalid value for `scheduled_state` ({0}), must be one of {1}"
                .format(scheduled_state, allowed_values)
            )

        self._scheduled_state = scheduled_state

    @property
    def retry_count(self):
        """
        Gets the retry_count of this VersionedProcessor.
        Overall number of retries.

        :return: The retry_count of this VersionedProcessor.
        :rtype: int
        """
        return self._retry_count

    @retry_count.setter
    def retry_count(self, retry_count):
        """
        Sets the retry_count of this VersionedProcessor.
        Overall number of retries.

        :param retry_count: The retry_count of this VersionedProcessor.
        :type: int
        """

        self._retry_count = retry_count

    @property
    def retried_relationships(self):
        """
        Gets the retried_relationships of this VersionedProcessor.
        All the relationships should be retried.

        :return: The retried_relationships of this VersionedProcessor.
        :rtype: list[str]
        """
        return self._retried_relationships

    @retried_relationships.setter
    def retried_relationships(self, retried_relationships):
        """
        Sets the retried_relationships of this VersionedProcessor.
        All the relationships should be retried.

        :param retried_relationships: The retried_relationships of this VersionedProcessor.
        :type: list[str]
        """

        self._retried_relationships = retried_relationships

    @property
    def backoff_mechanism(self):
        """
        Gets the backoff_mechanism of this VersionedProcessor.
        Determines whether the FlowFile should be penalized or the processor should be yielded between retries.

        :return: The backoff_mechanism of this VersionedProcessor.
        :rtype: str
        """
        return self._backoff_mechanism

    @backoff_mechanism.setter
    def backoff_mechanism(self, backoff_mechanism):
        """
        Sets the backoff_mechanism of this VersionedProcessor.
        Determines whether the FlowFile should be penalized or the processor should be yielded between retries.

        :param backoff_mechanism: The backoff_mechanism of this VersionedProcessor.
        :type: str
        """
        allowed_values = ["PENALIZE_FLOWFILE", "YIELD_PROCESSOR"]
        if backoff_mechanism not in allowed_values:
            raise ValueError(
                "Invalid value for `backoff_mechanism` ({0}), must be one of {1}"
                .format(backoff_mechanism, allowed_values)
            )

        self._backoff_mechanism = backoff_mechanism

    @property
    def max_backoff_period(self):
        """
        Gets the max_backoff_period of this VersionedProcessor.
        Maximum amount of time to be waited during a retry period.

        :return: The max_backoff_period of this VersionedProcessor.
        :rtype: str
        """
        return self._max_backoff_period

    @max_backoff_period.setter
    def max_backoff_period(self, max_backoff_period):
        """
        Sets the max_backoff_period of this VersionedProcessor.
        Maximum amount of time to be waited during a retry period.

        :param max_backoff_period: The max_backoff_period of this VersionedProcessor.
        :type: str
        """

        self._max_backoff_period = max_backoff_period

    @property
    def component_type(self):
        """
        Gets the component_type of this VersionedProcessor.

        :return: The component_type of this VersionedProcessor.
        :rtype: str
        """
        return self._component_type

    @component_type.setter
    def component_type(self, component_type):
        """
        Sets the component_type of this VersionedProcessor.

        :param component_type: The component_type of this VersionedProcessor.
        :type: str
        """
        allowed_values = ["CONNECTION", "PROCESSOR", "PROCESS_GROUP", "REMOTE_PROCESS_GROUP", "INPUT_PORT", "OUTPUT_PORT", "REMOTE_INPUT_PORT", "REMOTE_OUTPUT_PORT", "FUNNEL", "LABEL", "CONTROLLER_SERVICE", "REPORTING_TASK", "PARAMETER_CONTEXT", "PARAMETER_PROVIDER", "TEMPLATE", "FLOW_REGISTRY_CLIENT"]
        if component_type not in allowed_values:
            raise ValueError(
                "Invalid value for `component_type` ({0}), must be one of {1}"
                .format(component_type, allowed_values)
            )

        self._component_type = component_type

    @property
    def group_identifier(self):
        """
        Gets the group_identifier of this VersionedProcessor.
        The ID of the Process Group that this component belongs to

        :return: The group_identifier of this VersionedProcessor.
        :rtype: str
        """
        return self._group_identifier

    @group_identifier.setter
    def group_identifier(self, group_identifier):
        """
        Sets the group_identifier of this VersionedProcessor.
        The ID of the Process Group that this component belongs to

        :param group_identifier: The group_identifier of this VersionedProcessor.
        :type: str
        """

        self._group_identifier = group_identifier

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        if not isinstance(other, VersionedProcessor):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
