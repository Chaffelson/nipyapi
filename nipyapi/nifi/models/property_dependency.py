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


class PropertyDependency(object):
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
        'property_name': 'str',
        'property_display_name': 'str',
        'dependent_values': 'list[str]'
    }

    attribute_map = {
        'property_name': 'propertyName',
        'property_display_name': 'propertyDisplayName',
        'dependent_values': 'dependentValues'
    }

    def __init__(self, property_name=None, property_display_name=None, dependent_values=None):
        """
        PropertyDependency - a model defined in Swagger
        """

        self._property_name = None
        self._property_display_name = None
        self._dependent_values = None

        if property_name is not None:
          self.property_name = property_name
        if property_display_name is not None:
          self.property_display_name = property_display_name
        if dependent_values is not None:
          self.dependent_values = dependent_values

    @property
    def property_name(self):
        """
        Gets the property_name of this PropertyDependency.
        The name of the property that is depended upon

        :return: The property_name of this PropertyDependency.
        :rtype: str
        """
        return self._property_name

    @property_name.setter
    def property_name(self, property_name):
        """
        Sets the property_name of this PropertyDependency.
        The name of the property that is depended upon

        :param property_name: The property_name of this PropertyDependency.
        :type: str
        """

        self._property_name = property_name

    @property
    def property_display_name(self):
        """
        Gets the property_display_name of this PropertyDependency.
        The name of the property that is depended upon

        :return: The property_display_name of this PropertyDependency.
        :rtype: str
        """
        return self._property_display_name

    @property_display_name.setter
    def property_display_name(self, property_display_name):
        """
        Sets the property_display_name of this PropertyDependency.
        The name of the property that is depended upon

        :param property_display_name: The property_display_name of this PropertyDependency.
        :type: str
        """

        self._property_display_name = property_display_name

    @property
    def dependent_values(self):
        """
        Gets the dependent_values of this PropertyDependency.
        The values that satisfy the dependency

        :return: The dependent_values of this PropertyDependency.
        :rtype: list[str]
        """
        return self._dependent_values

    @dependent_values.setter
    def dependent_values(self, dependent_values):
        """
        Sets the dependent_values of this PropertyDependency.
        The values that satisfy the dependency

        :param dependent_values: The dependent_values of this PropertyDependency.
        :type: list[str]
        """

        self._dependent_values = dependent_values

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
        if not isinstance(other, PropertyDependency):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
