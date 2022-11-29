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


class AllowableValueEntity(object):
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
        'allowable_value': 'AllowableValueDTO',
        'can_read': 'bool'
    }

    attribute_map = {
        'allowable_value': 'allowableValue',
        'can_read': 'canRead'
    }

    def __init__(self, allowable_value=None, can_read=None):
        """
        AllowableValueEntity - a model defined in Swagger
        """

        self._allowable_value = None
        self._can_read = None

        if allowable_value is not None:
          self.allowable_value = allowable_value
        if can_read is not None:
          self.can_read = can_read

    @property
    def allowable_value(self):
        """
        Gets the allowable_value of this AllowableValueEntity.

        :return: The allowable_value of this AllowableValueEntity.
        :rtype: AllowableValueDTO
        """
        return self._allowable_value

    @allowable_value.setter
    def allowable_value(self, allowable_value):
        """
        Sets the allowable_value of this AllowableValueEntity.

        :param allowable_value: The allowable_value of this AllowableValueEntity.
        :type: AllowableValueDTO
        """

        self._allowable_value = allowable_value

    @property
    def can_read(self):
        """
        Gets the can_read of this AllowableValueEntity.
        Indicates whether the user can read a given resource.

        :return: The can_read of this AllowableValueEntity.
        :rtype: bool
        """
        return self._can_read

    @can_read.setter
    def can_read(self, can_read):
        """
        Sets the can_read of this AllowableValueEntity.
        Indicates whether the user can read a given resource.

        :param can_read: The can_read of this AllowableValueEntity.
        :type: bool
        """

        self._can_read = can_read

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
        if not isinstance(other, AllowableValueEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
