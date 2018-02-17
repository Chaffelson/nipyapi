# coding: utf-8

"""
    NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 0.2.0-SNAPSHOT
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ThePositionOfAComponentOnTheGraph(object):
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
        'x': 'float',
        'y': 'float'
    }

    attribute_map = {
        'x': 'x',
        'y': 'y'
    }

    def __init__(self, x=None, y=None):
        """
        ThePositionOfAComponentOnTheGraph - a model defined in Swagger
        """

        self._x = None
        self._y = None

        if x is not None:
          self.x = x
        if y is not None:
          self.y = y

    @property
    def x(self):
        """
        Gets the x of this ThePositionOfAComponentOnTheGraph.
        The x coordinate.

        :return: The x of this ThePositionOfAComponentOnTheGraph.
        :rtype: float
        """
        return self._x

    @x.setter
    def x(self, x):
        """
        Sets the x of this ThePositionOfAComponentOnTheGraph.
        The x coordinate.

        :param x: The x of this ThePositionOfAComponentOnTheGraph.
        :type: float
        """

        self._x = x

    @property
    def y(self):
        """
        Gets the y of this ThePositionOfAComponentOnTheGraph.
        The y coordinate.

        :return: The y of this ThePositionOfAComponentOnTheGraph.
        :rtype: float
        """
        return self._y

    @y.setter
    def y(self, y):
        """
        Sets the y of this ThePositionOfAComponentOnTheGraph.
        The y coordinate.

        :param y: The y of this ThePositionOfAComponentOnTheGraph.
        :type: float
        """

        self._y = y

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
        if not isinstance(other, ThePositionOfAComponentOnTheGraph):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
