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


class ConnectableDTO(object):
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
        'id': 'str',
        'versioned_component_id': 'str',
        'type': 'str',
        'group_id': 'str',
        'name': 'str',
        'running': 'bool',
        'transmitting': 'bool',
        'exists': 'bool',
        'comments': 'str'
    }

    attribute_map = {
        'id': 'id',
        'versioned_component_id': 'versionedComponentId',
        'type': 'type',
        'group_id': 'groupId',
        'name': 'name',
        'running': 'running',
        'transmitting': 'transmitting',
        'exists': 'exists',
        'comments': 'comments'
    }

    def __init__(self, id=None, versioned_component_id=None, type=None, group_id=None, name=None, running=None, transmitting=None, exists=None, comments=None):
        """
        ConnectableDTO - a model defined in Swagger
        """

        self._id = None
        self._versioned_component_id = None
        self._type = None
        self._group_id = None
        self._name = None
        self._running = None
        self._transmitting = None
        self._exists = None
        self._comments = None

        self.id = id
        if versioned_component_id is not None:
          self.versioned_component_id = versioned_component_id
        self.type = type
        self.group_id = group_id
        if name is not None:
          self.name = name
        if running is not None:
          self.running = running
        if transmitting is not None:
          self.transmitting = transmitting
        if exists is not None:
          self.exists = exists
        if comments is not None:
          self.comments = comments

    @property
    def id(self):
        """
        Gets the id of this ConnectableDTO.
        The id of the connectable component.

        :return: The id of this ConnectableDTO.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ConnectableDTO.
        The id of the connectable component.

        :param id: The id of this ConnectableDTO.
        :type: str
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")

        self._id = id

    @property
    def versioned_component_id(self):
        """
        Gets the versioned_component_id of this ConnectableDTO.
        The ID of the corresponding component that is under version control

        :return: The versioned_component_id of this ConnectableDTO.
        :rtype: str
        """
        return self._versioned_component_id

    @versioned_component_id.setter
    def versioned_component_id(self, versioned_component_id):
        """
        Sets the versioned_component_id of this ConnectableDTO.
        The ID of the corresponding component that is under version control

        :param versioned_component_id: The versioned_component_id of this ConnectableDTO.
        :type: str
        """

        self._versioned_component_id = versioned_component_id

    @property
    def type(self):
        """
        Gets the type of this ConnectableDTO.
        The type of component the connectable is.

        :return: The type of this ConnectableDTO.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ConnectableDTO.
        The type of component the connectable is.

        :param type: The type of this ConnectableDTO.
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")
        allowed_values = ["PROCESSOR", "REMOTE_INPUT_PORT", "REMOTE_OUTPUT_PORT", "INPUT_PORT", "OUTPUT_PORT", "FUNNEL"]
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def group_id(self):
        """
        Gets the group_id of this ConnectableDTO.
        The id of the group that the connectable component resides in

        :return: The group_id of this ConnectableDTO.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """
        Sets the group_id of this ConnectableDTO.
        The id of the group that the connectable component resides in

        :param group_id: The group_id of this ConnectableDTO.
        :type: str
        """
        if group_id is None:
            raise ValueError("Invalid value for `group_id`, must not be `None`")

        self._group_id = group_id

    @property
    def name(self):
        """
        Gets the name of this ConnectableDTO.
        The name of the connectable component

        :return: The name of this ConnectableDTO.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ConnectableDTO.
        The name of the connectable component

        :param name: The name of this ConnectableDTO.
        :type: str
        """

        self._name = name

    @property
    def running(self):
        """
        Gets the running of this ConnectableDTO.
        Reflects the current state of the connectable component.

        :return: The running of this ConnectableDTO.
        :rtype: bool
        """
        return self._running

    @running.setter
    def running(self, running):
        """
        Sets the running of this ConnectableDTO.
        Reflects the current state of the connectable component.

        :param running: The running of this ConnectableDTO.
        :type: bool
        """

        self._running = running

    @property
    def transmitting(self):
        """
        Gets the transmitting of this ConnectableDTO.
        If the connectable component represents a remote port, indicates if the target is configured to transmit.

        :return: The transmitting of this ConnectableDTO.
        :rtype: bool
        """
        return self._transmitting

    @transmitting.setter
    def transmitting(self, transmitting):
        """
        Sets the transmitting of this ConnectableDTO.
        If the connectable component represents a remote port, indicates if the target is configured to transmit.

        :param transmitting: The transmitting of this ConnectableDTO.
        :type: bool
        """

        self._transmitting = transmitting

    @property
    def exists(self):
        """
        Gets the exists of this ConnectableDTO.
        If the connectable component represents a remote port, indicates if the target exists.

        :return: The exists of this ConnectableDTO.
        :rtype: bool
        """
        return self._exists

    @exists.setter
    def exists(self, exists):
        """
        Sets the exists of this ConnectableDTO.
        If the connectable component represents a remote port, indicates if the target exists.

        :param exists: The exists of this ConnectableDTO.
        :type: bool
        """

        self._exists = exists

    @property
    def comments(self):
        """
        Gets the comments of this ConnectableDTO.
        The comments for the connectable component.

        :return: The comments of this ConnectableDTO.
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """
        Sets the comments of this ConnectableDTO.
        The comments for the connectable component.

        :param comments: The comments of this ConnectableDTO.
        :type: str
        """

        self._comments = comments

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
        if not isinstance(other, ConnectableDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
