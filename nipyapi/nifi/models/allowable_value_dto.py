"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class AllowableValueDTO(object):
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
        'display_name': 'str',
        'value': 'str',
        'description': 'str'
    }

    attribute_map = {
        'display_name': 'displayName',
        'value': 'value',
        'description': 'description'
    }

    def __init__(self, display_name=None, value=None, description=None):
        """
        AllowableValueDTO - a model defined in Swagger
        """

        self._display_name = None
        self._value = None
        self._description = None

        if display_name is not None:
          self.display_name = display_name
        if value is not None:
          self.value = value
        if description is not None:
          self.description = description

    @property
    def display_name(self):
        """
        Gets the display_name of this AllowableValueDTO.
        A human readable value that is allowed for the property descriptor.

        :return: The display_name of this AllowableValueDTO.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name):
        """
        Sets the display_name of this AllowableValueDTO.
        A human readable value that is allowed for the property descriptor.

        :param display_name: The display_name of this AllowableValueDTO.
        :type: str
        """

        self._display_name = display_name

    @property
    def value(self):
        """
        Gets the value of this AllowableValueDTO.
        A value that is allowed for the property descriptor.

        :return: The value of this AllowableValueDTO.
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        Sets the value of this AllowableValueDTO.
        A value that is allowed for the property descriptor.

        :param value: The value of this AllowableValueDTO.
        :type: str
        """

        self._value = value

    @property
    def description(self):
        """
        Gets the description of this AllowableValueDTO.
        A description for this allowable value.

        :return: The description of this AllowableValueDTO.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this AllowableValueDTO.
        A description for this allowable value.

        :param description: The description of this AllowableValueDTO.
        :type: str
        """

        self._description = description

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
        if not isinstance(other, AllowableValueDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
