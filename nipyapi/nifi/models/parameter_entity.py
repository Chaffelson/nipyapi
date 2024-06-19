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


class ParameterEntity(object):
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
        'can_write': 'bool',
        'parameter': 'ParameterDTO'
    }

    attribute_map = {
        'can_write': 'canWrite',
        'parameter': 'parameter'
    }

    def __init__(self, can_write=None, parameter=None):
        """
        ParameterEntity - a model defined in Swagger
        """

        self._can_write = None
        self._parameter = None

        if can_write is not None:
          self.can_write = can_write
        if parameter is not None:
          self.parameter = parameter

    @property
    def can_write(self):
        """
        Gets the can_write of this ParameterEntity.
        Indicates whether the user can write a given resource.

        :return: The can_write of this ParameterEntity.
        :rtype: bool
        """
        return self._can_write

    @can_write.setter
    def can_write(self, can_write):
        """
        Sets the can_write of this ParameterEntity.
        Indicates whether the user can write a given resource.

        :param can_write: The can_write of this ParameterEntity.
        :type: bool
        """

        self._can_write = can_write

    @property
    def parameter(self):
        """
        Gets the parameter of this ParameterEntity.
        The parameter information

        :return: The parameter of this ParameterEntity.
        :rtype: ParameterDTO
        """
        return self._parameter

    @parameter.setter
    def parameter(self, parameter):
        """
        Sets the parameter of this ParameterEntity.
        The parameter information

        :param parameter: The parameter of this ParameterEntity.
        :type: ParameterDTO
        """

        self._parameter = parameter

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
        if not isinstance(other, ParameterEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
