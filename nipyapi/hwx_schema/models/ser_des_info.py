# coding: utf-8

"""

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class SerDesInfo(object):
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
        'id': 'int',
        'timestamp': 'int',
        'ser_des_pair': 'SerDesPair'
    }

    attribute_map = {
        'id': 'id',
        'timestamp': 'timestamp',
        'ser_des_pair': 'serDesPair'
    }

    def __init__(self, id=None, timestamp=None, ser_des_pair=None):
        """
        SerDesInfo - a model defined in Swagger
        """

        self._id = None
        self._timestamp = None
        self._ser_des_pair = None

        if id is not None:
          self.id = id
        if timestamp is not None:
          self.timestamp = timestamp
        if ser_des_pair is not None:
          self.ser_des_pair = ser_des_pair

    @property
    def id(self):
        """
        Gets the id of this SerDesInfo.

        :return: The id of this SerDesInfo.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this SerDesInfo.

        :param id: The id of this SerDesInfo.
        :type: int
        """

        self._id = id

    @property
    def timestamp(self):
        """
        Gets the timestamp of this SerDesInfo.

        :return: The timestamp of this SerDesInfo.
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Sets the timestamp of this SerDesInfo.

        :param timestamp: The timestamp of this SerDesInfo.
        :type: int
        """

        self._timestamp = timestamp

    @property
    def ser_des_pair(self):
        """
        Gets the ser_des_pair of this SerDesInfo.

        :return: The ser_des_pair of this SerDesInfo.
        :rtype: SerDesPair
        """
        return self._ser_des_pair

    @ser_des_pair.setter
    def ser_des_pair(self, ser_des_pair):
        """
        Sets the ser_des_pair of this SerDesInfo.

        :param ser_des_pair: The ser_des_pair of this SerDesInfo.
        :type: SerDesPair
        """

        self._ser_des_pair = ser_des_pair

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
        if not isinstance(other, SerDesInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other