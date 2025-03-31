"""
    Apache NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class ComponentDifference(object):
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
        'value_a': 'str',
        'value_b': 'str',
        'change_description': 'str',
        'difference_type': 'str',
        'difference_type_description': 'str'
    }

    attribute_map = {
        'value_a': 'valueA',
        'value_b': 'valueB',
        'change_description': 'changeDescription',
        'difference_type': 'differenceType',
        'difference_type_description': 'differenceTypeDescription'
    }

    def __init__(self, value_a=None, value_b=None, change_description=None, difference_type=None, difference_type_description=None):
        """
        ComponentDifference - a model defined in Swagger
        """

        self._value_a = None
        self._value_b = None
        self._change_description = None
        self._difference_type = None
        self._difference_type_description = None

        if value_a is not None:
          self.value_a = value_a
        if value_b is not None:
          self.value_b = value_b
        if change_description is not None:
          self.change_description = change_description
        if difference_type is not None:
          self.difference_type = difference_type
        if difference_type_description is not None:
          self.difference_type_description = difference_type_description

    @property
    def value_a(self):
        """
        Gets the value_a of this ComponentDifference.
        The earlier value from the difference.

        :return: The value_a of this ComponentDifference.
        :rtype: str
        """
        return self._value_a

    @value_a.setter
    def value_a(self, value_a):
        """
        Sets the value_a of this ComponentDifference.
        The earlier value from the difference.

        :param value_a: The value_a of this ComponentDifference.
        :type: str
        """

        self._value_a = value_a

    @property
    def value_b(self):
        """
        Gets the value_b of this ComponentDifference.
        The newer value from the difference.

        :return: The value_b of this ComponentDifference.
        :rtype: str
        """
        return self._value_b

    @value_b.setter
    def value_b(self, value_b):
        """
        Sets the value_b of this ComponentDifference.
        The newer value from the difference.

        :param value_b: The value_b of this ComponentDifference.
        :type: str
        """

        self._value_b = value_b

    @property
    def change_description(self):
        """
        Gets the change_description of this ComponentDifference.
        The description of the change.

        :return: The change_description of this ComponentDifference.
        :rtype: str
        """
        return self._change_description

    @change_description.setter
    def change_description(self, change_description):
        """
        Sets the change_description of this ComponentDifference.
        The description of the change.

        :param change_description: The change_description of this ComponentDifference.
        :type: str
        """

        self._change_description = change_description

    @property
    def difference_type(self):
        """
        Gets the difference_type of this ComponentDifference.
        The key to the difference.

        :return: The difference_type of this ComponentDifference.
        :rtype: str
        """
        return self._difference_type

    @difference_type.setter
    def difference_type(self, difference_type):
        """
        Sets the difference_type of this ComponentDifference.
        The key to the difference.

        :param difference_type: The difference_type of this ComponentDifference.
        :type: str
        """

        self._difference_type = difference_type

    @property
    def difference_type_description(self):
        """
        Gets the difference_type_description of this ComponentDifference.
        The description of the change type.

        :return: The difference_type_description of this ComponentDifference.
        :rtype: str
        """
        return self._difference_type_description

    @difference_type_description.setter
    def difference_type_description(self, difference_type_description):
        """
        Sets the difference_type_description of this ComponentDifference.
        The description of the change type.

        :param difference_type_description: The difference_type_description of this ComponentDifference.
        :type: str
        """

        self._difference_type_description = difference_type_description

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in self.swagger_types.items():
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
        if not isinstance(other, ComponentDifference):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
