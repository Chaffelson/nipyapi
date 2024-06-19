# coding: utf-8

"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.26.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class RemotePortRunStatusEntity(object):
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
        'revision': 'RevisionDTO',
        'state': 'str',
        'disconnected_node_acknowledged': 'bool'
    }

    attribute_map = {
        'revision': 'revision',
        'state': 'state',
        'disconnected_node_acknowledged': 'disconnectedNodeAcknowledged'
    }

    def __init__(self, revision=None, state=None, disconnected_node_acknowledged=None):
        """
        RemotePortRunStatusEntity - a model defined in Swagger
        """

        self._revision = None
        self._state = None
        self._disconnected_node_acknowledged = None

        if revision is not None:
          self.revision = revision
        if state is not None:
          self.state = state
        if disconnected_node_acknowledged is not None:
          self.disconnected_node_acknowledged = disconnected_node_acknowledged

    @property
    def revision(self):
        """
        Gets the revision of this RemotePortRunStatusEntity.
        The revision for this request/response. The revision is required for any mutable flow requests and is included in all responses.

        :return: The revision of this RemotePortRunStatusEntity.
        :rtype: RevisionDTO
        """
        return self._revision

    @revision.setter
    def revision(self, revision):
        """
        Sets the revision of this RemotePortRunStatusEntity.
        The revision for this request/response. The revision is required for any mutable flow requests and is included in all responses.

        :param revision: The revision of this RemotePortRunStatusEntity.
        :type: RevisionDTO
        """

        self._revision = revision

    @property
    def state(self):
        """
        Gets the state of this RemotePortRunStatusEntity.
        The run status of the RemotePort.

        :return: The state of this RemotePortRunStatusEntity.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this RemotePortRunStatusEntity.
        The run status of the RemotePort.

        :param state: The state of this RemotePortRunStatusEntity.
        :type: str
        """
        allowed_values = ["TRANSMITTING", "STOPPED"]
        if state not in allowed_values:
            raise ValueError(
                "Invalid value for `state` ({0}), must be one of {1}"
                .format(state, allowed_values)
            )

        self._state = state

    @property
    def disconnected_node_acknowledged(self):
        """
        Gets the disconnected_node_acknowledged of this RemotePortRunStatusEntity.
        Acknowledges that this node is disconnected to allow for mutable requests to proceed.

        :return: The disconnected_node_acknowledged of this RemotePortRunStatusEntity.
        :rtype: bool
        """
        return self._disconnected_node_acknowledged

    @disconnected_node_acknowledged.setter
    def disconnected_node_acknowledged(self, disconnected_node_acknowledged):
        """
        Sets the disconnected_node_acknowledged of this RemotePortRunStatusEntity.
        Acknowledges that this node is disconnected to allow for mutable requests to proceed.

        :param disconnected_node_acknowledged: The disconnected_node_acknowledged of this RemotePortRunStatusEntity.
        :type: bool
        """

        self._disconnected_node_acknowledged = disconnected_node_acknowledged

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
        if not isinstance(other, RemotePortRunStatusEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
