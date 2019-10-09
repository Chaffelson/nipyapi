# coding: utf-8

"""
    Apache NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 0.5.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class Permissions(object):
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
        'can_read': 'bool',
        'can_write': 'bool',
        'can_delete': 'bool'
    }

    attribute_map = {
        'can_read': 'canRead',
        'can_write': 'canWrite',
        'can_delete': 'canDelete'
    }

    def __init__(self, can_read=None, can_write=None, can_delete=None):
        """
        Permissions - a model defined in Swagger
        """

        self._can_read = None
        self._can_write = None
        self._can_delete = None

        if can_read is not None:
          self.can_read = can_read
        if can_write is not None:
          self.can_write = can_write
        if can_delete is not None:
          self.can_delete = can_delete

    @property
    def can_read(self):
        """
        Gets the can_read of this Permissions.
        Indicates whether the user can read a given resource.

        :return: The can_read of this Permissions.
        :rtype: bool
        """
        return self._can_read

    @can_read.setter
    def can_read(self, can_read):
        """
        Sets the can_read of this Permissions.
        Indicates whether the user can read a given resource.

        :param can_read: The can_read of this Permissions.
        :type: bool
        """

        self._can_read = can_read

    @property
    def can_write(self):
        """
        Gets the can_write of this Permissions.
        Indicates whether the user can write a given resource.

        :return: The can_write of this Permissions.
        :rtype: bool
        """
        return self._can_write

    @can_write.setter
    def can_write(self, can_write):
        """
        Sets the can_write of this Permissions.
        Indicates whether the user can write a given resource.

        :param can_write: The can_write of this Permissions.
        :type: bool
        """

        self._can_write = can_write

    @property
    def can_delete(self):
        """
        Gets the can_delete of this Permissions.
        Indicates whether the user can delete a given resource.

        :return: The can_delete of this Permissions.
        :rtype: bool
        """
        return self._can_delete

    @can_delete.setter
    def can_delete(self, can_delete):
        """
        Sets the can_delete of this Permissions.
        Indicates whether the user can delete a given resource.

        :param can_delete: The can_delete of this Permissions.
        :type: bool
        """

        self._can_delete = can_delete

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
        if not isinstance(other, Permissions):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
