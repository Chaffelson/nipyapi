# coding: utf-8

"""
    Apache NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 1.16.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class DefaultSettings(object):
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
        'yield_duration': 'str',
        'penalty_duration': 'str',
        'bulletin_level': 'str'
    }

    attribute_map = {
        'yield_duration': 'yieldDuration',
        'penalty_duration': 'penaltyDuration',
        'bulletin_level': 'bulletinLevel'
    }

    def __init__(self, yield_duration=None, penalty_duration=None, bulletin_level=None):
        """
        DefaultSettings - a model defined in Swagger
        """

        self._yield_duration = None
        self._penalty_duration = None
        self._bulletin_level = None

        if yield_duration is not None:
          self.yield_duration = yield_duration
        if penalty_duration is not None:
          self.penalty_duration = penalty_duration
        if bulletin_level is not None:
          self.bulletin_level = bulletin_level

    @property
    def yield_duration(self):
        """
        Gets the yield_duration of this DefaultSettings.
        The default yield duration

        :return: The yield_duration of this DefaultSettings.
        :rtype: str
        """
        return self._yield_duration

    @yield_duration.setter
    def yield_duration(self, yield_duration):
        """
        Sets the yield_duration of this DefaultSettings.
        The default yield duration

        :param yield_duration: The yield_duration of this DefaultSettings.
        :type: str
        """

        self._yield_duration = yield_duration

    @property
    def penalty_duration(self):
        """
        Gets the penalty_duration of this DefaultSettings.
        The default penalty duration

        :return: The penalty_duration of this DefaultSettings.
        :rtype: str
        """
        return self._penalty_duration

    @penalty_duration.setter
    def penalty_duration(self, penalty_duration):
        """
        Sets the penalty_duration of this DefaultSettings.
        The default penalty duration

        :param penalty_duration: The penalty_duration of this DefaultSettings.
        :type: str
        """

        self._penalty_duration = penalty_duration

    @property
    def bulletin_level(self):
        """
        Gets the bulletin_level of this DefaultSettings.
        The default bulletin level

        :return: The bulletin_level of this DefaultSettings.
        :rtype: str
        """
        return self._bulletin_level

    @bulletin_level.setter
    def bulletin_level(self, bulletin_level):
        """
        Sets the bulletin_level of this DefaultSettings.
        The default bulletin level

        :param bulletin_level: The bulletin_level of this DefaultSettings.
        :type: str
        """

        self._bulletin_level = bulletin_level

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
        if not isinstance(other, DefaultSettings):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
