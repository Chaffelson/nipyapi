# coding: utf-8

"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.17.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class AttributeDTO(object):
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
        'name': 'str',
        'value': 'str',
        'previous_value': 'str'
    }

    attribute_map = {
        'name': 'name',
        'value': 'value',
        'previous_value': 'previousValue'
    }

    def __init__(self, name=None, value=None, previous_value=None):
        """
        AttributeDTO - a model defined in Swagger
        """

        self._name = None
        self._value = None
        self._previous_value = None

        if name is not None:
          self.name = name
        if value is not None:
          self.value = value
        if previous_value is not None:
          self.previous_value = previous_value

    @property
    def name(self):
        """
        Gets the name of this AttributeDTO.
        The attribute name.

        :return: The name of this AttributeDTO.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this AttributeDTO.
        The attribute name.

        :param name: The name of this AttributeDTO.
        :type: str
        """

        self._name = name

    @property
    def value(self):
        """
        Gets the value of this AttributeDTO.
        The attribute value.

        :return: The value of this AttributeDTO.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this AttributeDTO.
        The attribute value.

        :param value: The value of this AttributeDTO.
        :type: str
        """

        self._value = value

    @property
    def previous_value(self):
        """
        Gets the previous_value of this AttributeDTO.
        The value of the attribute before the event took place.

        :return: The previous_value of this AttributeDTO.
        :rtype: str
        """
        return self._previous_value

    @previous_value.setter
    def previous_value(self, previous_value):
        """
        Sets the previous_value of this AttributeDTO.
        The value of the attribute before the event took place.

        :param previous_value: The previous_value of this AttributeDTO.
        :type: str
        """

        self._previous_value = previous_value

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
        if not isinstance(other, AttributeDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
