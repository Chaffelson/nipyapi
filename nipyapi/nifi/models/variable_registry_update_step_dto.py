"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class VariableRegistryUpdateStepDTO(object):
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
        'description': 'str',
        'complete': 'bool',
        'failure_reason': 'str'
    }

    attribute_map = {
        'description': 'description',
        'complete': 'complete',
        'failure_reason': 'failureReason'
    }

    def __init__(self, description=None, complete=None, failure_reason=None):
        """
        VariableRegistryUpdateStepDTO - a model defined in Swagger
        """

        self._description = None
        self._complete = None
        self._failure_reason = None

        if description is not None:
          self.description = description
        if complete is not None:
          self.complete = complete
        if failure_reason is not None:
          self.failure_reason = failure_reason

    @property
    def description(self):
        """
        Gets the description of this VariableRegistryUpdateStepDTO.
        Explanation of what happens in this step

        :return: The description of this VariableRegistryUpdateStepDTO.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this VariableRegistryUpdateStepDTO.
        Explanation of what happens in this step

        :param description: The description of this VariableRegistryUpdateStepDTO.
        :type: str
        """

        self._description = description

    @property
    def complete(self):
        """
        Gets the complete of this VariableRegistryUpdateStepDTO.
        Whether or not this step has completed

        :return: The complete of this VariableRegistryUpdateStepDTO.
        :rtype: bool
        """
        return self._complete

    @complete.setter
    def complete(self, complete):
        """
        Sets the complete of this VariableRegistryUpdateStepDTO.
        Whether or not this step has completed

        :param complete: The complete of this VariableRegistryUpdateStepDTO.
        :type: bool
        """

        self._complete = complete

    @property
    def failure_reason(self):
        """
        Gets the failure_reason of this VariableRegistryUpdateStepDTO.
        An explanation of why this step failed, or null if this step did not fail

        :return: The failure_reason of this VariableRegistryUpdateStepDTO.
        :rtype: str
        """
        return self._failure_reason

    @failure_reason.setter
    def failure_reason(self, failure_reason):
        """
        Sets the failure_reason of this VariableRegistryUpdateStepDTO.
        An explanation of why this step failed, or null if this step did not fail

        :param failure_reason: The failure_reason of this VariableRegistryUpdateStepDTO.
        :type: str
        """

        self._failure_reason = failure_reason

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
        if not isinstance(other, VariableRegistryUpdateStepDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
