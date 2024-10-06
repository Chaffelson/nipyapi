# coding: utf-8

"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.27.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ParameterProviderConfigurationDTO(object):
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
        'parameter_provider_id': 'str',
        'parameter_provider_name': 'str',
        'parameter_group_name': 'str',
        'synchronized': 'bool'
    }

    attribute_map = {
        'parameter_provider_id': 'parameterProviderId',
        'parameter_provider_name': 'parameterProviderName',
        'parameter_group_name': 'parameterGroupName',
        'synchronized': 'synchronized'
    }

    def __init__(self, parameter_provider_id=None, parameter_provider_name=None, parameter_group_name=None, synchronized=None):
        """
        ParameterProviderConfigurationDTO - a model defined in Swagger
        """

        self._parameter_provider_id = None
        self._parameter_provider_name = None
        self._parameter_group_name = None
        self._synchronized = None

        if parameter_provider_id is not None:
          self.parameter_provider_id = parameter_provider_id
        if parameter_provider_name is not None:
          self.parameter_provider_name = parameter_provider_name
        if parameter_group_name is not None:
          self.parameter_group_name = parameter_group_name
        if synchronized is not None:
          self.synchronized = synchronized

    @property
    def parameter_provider_id(self):
        """
        Gets the parameter_provider_id of this ParameterProviderConfigurationDTO.
        The ID of the Parameter Provider

        :return: The parameter_provider_id of this ParameterProviderConfigurationDTO.
        :rtype: str
        """
        return self._parameter_provider_id

    @parameter_provider_id.setter
    def parameter_provider_id(self, parameter_provider_id):
        """
        Sets the parameter_provider_id of this ParameterProviderConfigurationDTO.
        The ID of the Parameter Provider

        :param parameter_provider_id: The parameter_provider_id of this ParameterProviderConfigurationDTO.
        :type: str
        """

        self._parameter_provider_id = parameter_provider_id

    @property
    def parameter_provider_name(self):
        """
        Gets the parameter_provider_name of this ParameterProviderConfigurationDTO.
        The name of the Parameter Provider

        :return: The parameter_provider_name of this ParameterProviderConfigurationDTO.
        :rtype: str
        """
        return self._parameter_provider_name

    @parameter_provider_name.setter
    def parameter_provider_name(self, parameter_provider_name):
        """
        Sets the parameter_provider_name of this ParameterProviderConfigurationDTO.
        The name of the Parameter Provider

        :param parameter_provider_name: The parameter_provider_name of this ParameterProviderConfigurationDTO.
        :type: str
        """

        self._parameter_provider_name = parameter_provider_name

    @property
    def parameter_group_name(self):
        """
        Gets the parameter_group_name of this ParameterProviderConfigurationDTO.
        The Parameter Group name that maps to the Parameter Context

        :return: The parameter_group_name of this ParameterProviderConfigurationDTO.
        :rtype: str
        """
        return self._parameter_group_name

    @parameter_group_name.setter
    def parameter_group_name(self, parameter_group_name):
        """
        Sets the parameter_group_name of this ParameterProviderConfigurationDTO.
        The Parameter Group name that maps to the Parameter Context

        :param parameter_group_name: The parameter_group_name of this ParameterProviderConfigurationDTO.
        :type: str
        """

        self._parameter_group_name = parameter_group_name

    @property
    def synchronized(self):
        """
        Gets the synchronized of this ParameterProviderConfigurationDTO.
        True if the Parameter Context should receive the parameters from the mapped Parameter Group

        :return: The synchronized of this ParameterProviderConfigurationDTO.
        :rtype: bool
        """
        return self._synchronized

    @synchronized.setter
    def synchronized(self, synchronized):
        """
        Sets the synchronized of this ParameterProviderConfigurationDTO.
        True if the Parameter Context should receive the parameters from the mapped Parameter Group

        :param synchronized: The synchronized of this ParameterProviderConfigurationDTO.
        :type: bool
        """

        self._synchronized = synchronized

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
        if not isinstance(other, ParameterProviderConfigurationDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
