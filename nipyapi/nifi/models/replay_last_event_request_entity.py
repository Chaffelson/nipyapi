# coding: utf-8

"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.19.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ReplayLastEventRequestEntity(object):
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
        'component_id': 'str',
        'nodes': 'str'
    }

    attribute_map = {
        'component_id': 'componentId',
        'nodes': 'nodes'
    }

    def __init__(self, component_id=None, nodes=None):
        """
        ReplayLastEventRequestEntity - a model defined in Swagger
        """

        self._component_id = None
        self._nodes = None

        if component_id is not None:
          self.component_id = component_id
        if nodes is not None:
          self.nodes = nodes

    @property
    def component_id(self):
        """
        Gets the component_id of this ReplayLastEventRequestEntity.
        The UUID of the component whose last event should be replayed.

        :return: The component_id of this ReplayLastEventRequestEntity.
        :rtype: str
        """
        return self._component_id

    @component_id.setter
    def component_id(self, component_id):
        """
        Sets the component_id of this ReplayLastEventRequestEntity.
        The UUID of the component whose last event should be replayed.

        :param component_id: The component_id of this ReplayLastEventRequestEntity.
        :type: str
        """

        self._component_id = component_id

    @property
    def nodes(self):
        """
        Gets the nodes of this ReplayLastEventRequestEntity.
        Which nodes are to replay their last provenance event.

        :return: The nodes of this ReplayLastEventRequestEntity.
        :rtype: str
        """
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        """
        Sets the nodes of this ReplayLastEventRequestEntity.
        Which nodes are to replay their last provenance event.

        :param nodes: The nodes of this ReplayLastEventRequestEntity.
        :type: str
        """
        allowed_values = ["ALL", "PRIMARY"]
        if nodes not in allowed_values:
            raise ValueError(
                "Invalid value for `nodes` ({0}), must be one of {1}"
                .format(nodes, allowed_values)
            )

        self._nodes = nodes

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
        if not isinstance(other, ReplayLastEventRequestEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
