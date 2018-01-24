# coding: utf-8

"""
    NiFi Rest Api

    The Rest Api provides programmatic access to command and control a NiFi instance in real time. Start and                                              stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.5.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class BatchSize(object):
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
        'count': 'int',
        'size': 'str',
        'duration': 'str'
    }

    attribute_map = {
        'count': 'count',
        'size': 'size',
        'duration': 'duration'
    }

    def __init__(self, count=None, size=None, duration=None):
        """
        BatchSize - a model defined in Swagger
        """

        self._count = None
        self._size = None
        self._duration = None

        if count is not None:
          self.count = count
        if size is not None:
          self.size = size
        if duration is not None:
          self.duration = duration

    @property
    def count(self):
        """
        Gets the count of this BatchSize.
        Preferred number of flow files to include in a transaction.

        :return: The count of this BatchSize.
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """
        Sets the count of this BatchSize.
        Preferred number of flow files to include in a transaction.

        :param count: The count of this BatchSize.
        :type: int
        """

        self._count = count

    @property
    def size(self):
        """
        Gets the size of this BatchSize.
        Preferred number of bytes to include in a transaction.

        :return: The size of this BatchSize.
        :rtype: str
        """
        return self._size

    @size.setter
    def size(self, size):
        """
        Sets the size of this BatchSize.
        Preferred number of bytes to include in a transaction.

        :param size: The size of this BatchSize.
        :type: str
        """

        self._size = size

    @property
    def duration(self):
        """
        Gets the duration of this BatchSize.
        Preferred amount of time that a transaction should span.

        :return: The duration of this BatchSize.
        :rtype: str
        """
        return self._duration

    @duration.setter
    def duration(self, duration):
        """
        Sets the duration of this BatchSize.
        Preferred amount of time that a transaction should span.

        :param duration: The duration of this BatchSize.
        :type: str
        """

        self._duration = duration

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
        if not isinstance(other, BatchSize):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other