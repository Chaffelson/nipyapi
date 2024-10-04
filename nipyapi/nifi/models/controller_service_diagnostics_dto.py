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


class ControllerServiceDiagnosticsDTO(object):
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
        'controller_service': 'ControllerServiceEntity',
        'class_loader_diagnostics': 'ClassLoaderDiagnosticsDTO'
    }

    attribute_map = {
        'controller_service': 'controllerService',
        'class_loader_diagnostics': 'classLoaderDiagnostics'
    }

    def __init__(self, controller_service=None, class_loader_diagnostics=None):
        """
        ControllerServiceDiagnosticsDTO - a model defined in Swagger
        """

        self._controller_service = None
        self._class_loader_diagnostics = None

        if controller_service is not None:
          self.controller_service = controller_service
        if class_loader_diagnostics is not None:
          self.class_loader_diagnostics = class_loader_diagnostics

    @property
    def controller_service(self):
        """
        Gets the controller_service of this ControllerServiceDiagnosticsDTO.
        The Controller Service

        :return: The controller_service of this ControllerServiceDiagnosticsDTO.
        :rtype: ControllerServiceEntity
        """
        return self._controller_service

    @controller_service.setter
    def controller_service(self, controller_service):
        """
        Sets the controller_service of this ControllerServiceDiagnosticsDTO.
        The Controller Service

        :param controller_service: The controller_service of this ControllerServiceDiagnosticsDTO.
        :type: ControllerServiceEntity
        """

        self._controller_service = controller_service

    @property
    def class_loader_diagnostics(self):
        """
        Gets the class_loader_diagnostics of this ControllerServiceDiagnosticsDTO.
        Information about the Controller Service's Class Loader

        :return: The class_loader_diagnostics of this ControllerServiceDiagnosticsDTO.
        :rtype: ClassLoaderDiagnosticsDTO
        """
        return self._class_loader_diagnostics

    @class_loader_diagnostics.setter
    def class_loader_diagnostics(self, class_loader_diagnostics):
        """
        Sets the class_loader_diagnostics of this ControllerServiceDiagnosticsDTO.
        Information about the Controller Service's Class Loader

        :param class_loader_diagnostics: The class_loader_diagnostics of this ControllerServiceDiagnosticsDTO.
        :type: ClassLoaderDiagnosticsDTO
        """

        self._class_loader_diagnostics = class_loader_diagnostics

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
        if not isinstance(other, ControllerServiceDiagnosticsDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
