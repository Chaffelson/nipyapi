# coding: utf-8

"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.19.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ControllerServiceTypesEntity(object):
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
        'controller_service_types': 'list[DocumentedTypeDTO]'
    }

    attribute_map = {
        'controller_service_types': 'controllerServiceTypes'
    }

    def __init__(self, controller_service_types=None):
        """
        ControllerServiceTypesEntity - a model defined in Swagger
        """

        self._controller_service_types = None

        if controller_service_types is not None:
          self.controller_service_types = controller_service_types

    @property
    def controller_service_types(self):
        """
        Gets the controller_service_types of this ControllerServiceTypesEntity.

        :return: The controller_service_types of this ControllerServiceTypesEntity.
        :rtype: list[DocumentedTypeDTO]
        """
        return self._controller_service_types

    @controller_service_types.setter
    def controller_service_types(self, controller_service_types):
        """
        Sets the controller_service_types of this ControllerServiceTypesEntity.

        :param controller_service_types: The controller_service_types of this ControllerServiceTypesEntity.
        :type: list[DocumentedTypeDTO]
        """

        self._controller_service_types = controller_service_types

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
        if not isinstance(other, ControllerServiceTypesEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
