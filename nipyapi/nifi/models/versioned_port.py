# coding: utf-8

"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.16.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class VersionedPort(object):
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
        'concurrently_schedulable_task_count': 'int',
        'scheduled_state': 'str',
        'allow_remote_access': 'bool',
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
        'concurrently_schedulable_task_count': 'concurrentlySchedulableTaskCount',
        'scheduled_state': 'scheduledState',
        'allow_remote_access': 'allowRemoteAccess',
        'component_type': 'componentType',
        'group_identifier': 'groupIdentifier'
    }

    def __init__(self, identifier=None, instance_identifier=None, name=None, comments=None, position=None, type=None, concurrently_schedulable_task_count=None, scheduled_state=None, allow_remote_access=None, component_type=None, group_identifier=None):
        """
        VersionedPort - a model defined in Swagger
        """

        self._identifier = None
        self._instance_identifier = None
        self._name = None
        self._comments = None
        self._position = None
        self._type = None
        self._concurrently_schedulable_task_count = None
        self._scheduled_state = None
        self._allow_remote_access = None
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
        if concurrently_schedulable_task_count is not None:
          self.concurrently_schedulable_task_count = concurrently_schedulable_task_count
        if scheduled_state is not None:
          self.scheduled_state = scheduled_state
        if allow_remote_access is not None:
          self.allow_remote_access = allow_remote_access
        if component_type is not None:
          self.component_type = component_type
        if group_identifier is not None:
          self.group_identifier = group_identifier

    @property
    def identifier(self):
        """
        Gets the identifier of this VersionedPort.
        The component's unique identifier

        :return: The identifier of this VersionedPort.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this VersionedPort.
        The component's unique identifier

        :param identifier: The identifier of this VersionedPort.
        :type: str
        """

        self._identifier = identifier

    @property
    def instance_identifier(self):
        """
        Gets the instance_identifier of this VersionedPort.
        The instance ID of an existing component that is described by this VersionedComponent, or null if this is not mapped to an instantiated component

        :return: The instance_identifier of this VersionedPort.
        :rtype: str
        """
        return self._instance_identifier

    @instance_identifier.setter
    def instance_identifier(self, instance_identifier):
        """
        Sets the instance_identifier of this VersionedPort.
        The instance ID of an existing component that is described by this VersionedComponent, or null if this is not mapped to an instantiated component

        :param instance_identifier: The instance_identifier of this VersionedPort.
        :type: str
        """

        self._instance_identifier = instance_identifier

    @property
    def name(self):
        """
        Gets the name of this VersionedPort.
        The component's name

        :return: The name of this VersionedPort.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this VersionedPort.
        The component's name

        :param name: The name of this VersionedPort.
        :type: str
        """

        self._name = name

    @property
    def comments(self):
        """
        Gets the comments of this VersionedPort.
        The user-supplied comments for the component

        :return: The comments of this VersionedPort.
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """
        Sets the comments of this VersionedPort.
        The user-supplied comments for the component

        :param comments: The comments of this VersionedPort.
        :type: str
        """

        self._comments = comments

    @property
    def position(self):
        """
        Gets the position of this VersionedPort.
        The component's position on the graph

        :return: The position of this VersionedPort.
        :rtype: Position
        """
        return self._position

    @position.setter
    def position(self, position):
        """
        Sets the position of this VersionedPort.
        The component's position on the graph

        :param position: The position of this VersionedPort.
        :type: Position
        """

        self._position = position

    @property
    def type(self):
        """
        Gets the type of this VersionedPort.
        The type of port.

        :return: The type of this VersionedPort.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this VersionedPort.
        The type of port.

        :param type: The type of this VersionedPort.
        :type: str
        """
        allowed_values = ["INPUT_PORT", "OUTPUT_PORT"]
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def concurrently_schedulable_task_count(self):
        """
        Gets the concurrently_schedulable_task_count of this VersionedPort.
        The number of tasks that should be concurrently scheduled for the port.

        :return: The concurrently_schedulable_task_count of this VersionedPort.
        :rtype: int
        """
        return self._concurrently_schedulable_task_count

    @concurrently_schedulable_task_count.setter
    def concurrently_schedulable_task_count(self, concurrently_schedulable_task_count):
        """
        Sets the concurrently_schedulable_task_count of this VersionedPort.
        The number of tasks that should be concurrently scheduled for the port.

        :param concurrently_schedulable_task_count: The concurrently_schedulable_task_count of this VersionedPort.
        :type: int
        """

        self._concurrently_schedulable_task_count = concurrently_schedulable_task_count

    @property
    def scheduled_state(self):
        """
        Gets the scheduled_state of this VersionedPort.
        The scheduled state of the component

        :return: The scheduled_state of this VersionedPort.
        :rtype: str
        """
        return self._scheduled_state

    @scheduled_state.setter
    def scheduled_state(self, scheduled_state):
        """
        Sets the scheduled_state of this VersionedPort.
        The scheduled state of the component

        :param scheduled_state: The scheduled_state of this VersionedPort.
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
    def allow_remote_access(self):
        """
        Gets the allow_remote_access of this VersionedPort.
        Whether or not this port allows remote access for site-to-site

        :return: The allow_remote_access of this VersionedPort.
        :rtype: bool
        """
        return self._allow_remote_access

    @allow_remote_access.setter
    def allow_remote_access(self, allow_remote_access):
        """
        Sets the allow_remote_access of this VersionedPort.
        Whether or not this port allows remote access for site-to-site

        :param allow_remote_access: The allow_remote_access of this VersionedPort.
        :type: bool
        """

        self._allow_remote_access = allow_remote_access

    @property
    def component_type(self):
        """
        Gets the component_type of this VersionedPort.

        :return: The component_type of this VersionedPort.
        :rtype: str
        """
        return self._component_type

    @component_type.setter
    def component_type(self, component_type):
        """
        Sets the component_type of this VersionedPort.

        :param component_type: The component_type of this VersionedPort.
        :type: str
        """
        allowed_values = ["CONNECTION", "PROCESSOR", "PROCESS_GROUP", "REMOTE_PROCESS_GROUP", "INPUT_PORT", "OUTPUT_PORT", "REMOTE_INPUT_PORT", "REMOTE_OUTPUT_PORT", "FUNNEL", "LABEL", "CONTROLLER_SERVICE", "REPORTING_TASK", "PARAMETER_CONTEXT", "TEMPLATE"]
        if component_type not in allowed_values:
            raise ValueError(
                "Invalid value for `component_type` ({0}), must be one of {1}"
                .format(component_type, allowed_values)
            )

        self._component_type = component_type

    @property
    def group_identifier(self):
        """
        Gets the group_identifier of this VersionedPort.
        The ID of the Process Group that this component belongs to

        :return: The group_identifier of this VersionedPort.
        :rtype: str
        """
        return self._group_identifier

    @group_identifier.setter
    def group_identifier(self, group_identifier):
        """
        Sets the group_identifier of this VersionedPort.
        The ID of the Process Group that this component belongs to

        :param group_identifier: The group_identifier of this VersionedPort.
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
        if not isinstance(other, VersionedPort):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
