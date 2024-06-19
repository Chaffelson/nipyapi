# coding: utf-8

"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.23.2
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ParameterGroupConfigurationEntity(object):
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
        'group_name': 'str',
        'parameter_context_name': 'str',
        'parameter_sensitivities': 'dict(str, str)',
        'synchronized': 'bool'
    }

    attribute_map = {
        'group_name': 'groupName',
        'parameter_context_name': 'parameterContextName',
        'parameter_sensitivities': 'parameterSensitivities',
        'synchronized': 'synchronized'
    }

    def __init__(self, group_name=None, parameter_context_name=None, parameter_sensitivities=None, synchronized=None):
        """
        ParameterGroupConfigurationEntity - a model defined in Swagger
        """

        self._group_name = None
        self._parameter_context_name = None
        self._parameter_sensitivities = None
        self._synchronized = None

        if group_name is not None:
          self.group_name = group_name
        if parameter_context_name is not None:
          self.parameter_context_name = parameter_context_name
        if parameter_sensitivities is not None:
          self.parameter_sensitivities = parameter_sensitivities
        if synchronized is not None:
          self.synchronized = synchronized

    @property
    def group_name(self):
        """
        Gets the group_name of this ParameterGroupConfigurationEntity.
        The name of the external parameter group to which the provided parameter names apply.

        :return: The group_name of this ParameterGroupConfigurationEntity.
        :rtype: str
        """
        return self._group_name

    @group_name.setter
    def group_name(self, group_name):
        """
        Sets the group_name of this ParameterGroupConfigurationEntity.
        The name of the external parameter group to which the provided parameter names apply.

        :param group_name: The group_name of this ParameterGroupConfigurationEntity.
        :type: str
        """

        self._group_name = group_name

    @property
    def parameter_context_name(self):
        """
        Gets the parameter_context_name of this ParameterGroupConfigurationEntity.
        The name of the ParameterContext that receives the parameters in this group

        :return: The parameter_context_name of this ParameterGroupConfigurationEntity.
        :rtype: str
        """
        return self._parameter_context_name

    @parameter_context_name.setter
    def parameter_context_name(self, parameter_context_name):
        """
        Sets the parameter_context_name of this ParameterGroupConfigurationEntity.
        The name of the ParameterContext that receives the parameters in this group

        :param parameter_context_name: The parameter_context_name of this ParameterGroupConfigurationEntity.
        :type: str
        """

        self._parameter_context_name = parameter_context_name

    @property
    def parameter_sensitivities(self):
        """
        Gets the parameter_sensitivities of this ParameterGroupConfigurationEntity.
        All fetched parameter names that should be applied.

        :return: The parameter_sensitivities of this ParameterGroupConfigurationEntity.
        :rtype: dict(str, str)
        """
        return self._parameter_sensitivities

    @parameter_sensitivities.setter
    def parameter_sensitivities(self, parameter_sensitivities):
        """
        Sets the parameter_sensitivities of this ParameterGroupConfigurationEntity.
        All fetched parameter names that should be applied.

        :param parameter_sensitivities: The parameter_sensitivities of this ParameterGroupConfigurationEntity.
        :type: dict(str, str)
        """
        # Added None, since that's what NiFi returns when the value is not yet set
        allowed_values = ["SENSITIVE", "NON_SENSITIVE", None]
        if not set(parameter_sensitivities.values()).issubset(set(allowed_values)):
            raise ValueError(
                "Invalid values in `parameter_sensitivities` [{0}], must be a subset of [{1}]"
                .format(", ".join(map(str, set(parameter_sensitivities.values())-set(allowed_values))),
                        ", ".join(map(str, allowed_values)))
            )

        self._parameter_sensitivities = parameter_sensitivities

    @property
    def synchronized(self):
        """
        Gets the synchronized of this ParameterGroupConfigurationEntity.
        True if this group should be synchronized to a ParameterContext, including creating one if it does not exist.

        :return: The synchronized of this ParameterGroupConfigurationEntity.
        :rtype: bool
        """
        return self._synchronized

    @synchronized.setter
    def synchronized(self, synchronized):
        """
        Sets the synchronized of this ParameterGroupConfigurationEntity.
        True if this group should be synchronized to a ParameterContext, including creating one if it does not exist.

        :param synchronized: The synchronized of this ParameterGroupConfigurationEntity.
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
        if not isinstance(other, ParameterGroupConfigurationEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
