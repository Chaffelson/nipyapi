# coding: utf-8

"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.27.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class PropertyAllowableValue(object):
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
        'value': 'str',
        'display_name': 'str',
        'description': 'str'
    }

    attribute_map = {
        'value': 'value',
        'display_name': 'displayName',
        'description': 'description'
    }

    def __init__(self, value=None, display_name=None, description=None):
        """
        PropertyAllowableValue - a model defined in Swagger
        """

        self._value = None
        self._display_name = None
        self._description = None

        self.value = value
        if display_name is not None:
          self.display_name = display_name
        if description is not None:
          self.description = description

    @property
    def value(self):
        """
        Gets the value of this PropertyAllowableValue.
        The internal value

        :return: The value of this PropertyAllowableValue.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this PropertyAllowableValue.
        The internal value

        :param value: The value of this PropertyAllowableValue.
        :type: str
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")

        self._value = value

    @property
    def display_name(self):
        """
        Gets the display_name of this PropertyAllowableValue.
        The display name of the value, if different from the internal value

        :return: The display_name of this PropertyAllowableValue.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this PropertyAllowableValue.
        The display name of the value, if different from the internal value

        :param display_name: The display_name of this PropertyAllowableValue.
        :type: str
        """

        self._display_name = display_name

    @property
    def description(self):
        """
        Gets the description of this PropertyAllowableValue.
        The description of the value, e.g., the behavior it produces.

        :return: The description of this PropertyAllowableValue.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this PropertyAllowableValue.
        The description of the value, e.g., the behavior it produces.

        :param description: The description of this PropertyAllowableValue.
        :type: str
        """

        self._description = description

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
        if not isinstance(other, PropertyAllowableValue):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
