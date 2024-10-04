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


class ClassLoaderDiagnosticsDTO(object):
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
        'bundle': 'BundleDTO',
        'parent_class_loader': 'ClassLoaderDiagnosticsDTO'
    }

    attribute_map = {
        'bundle': 'bundle',
        'parent_class_loader': 'parentClassLoader'
    }

    def __init__(self, bundle=None, parent_class_loader=None):
        """
        ClassLoaderDiagnosticsDTO - a model defined in Swagger
        """

        self._bundle = None
        self._parent_class_loader = None

        if bundle is not None:
          self.bundle = bundle
        if parent_class_loader is not None:
          self.parent_class_loader = parent_class_loader

    @property
    def bundle(self):
        """
        Gets the bundle of this ClassLoaderDiagnosticsDTO.
        Information about the Bundle that the ClassLoader belongs to, if any

        :return: The bundle of this ClassLoaderDiagnosticsDTO.
        :rtype: BundleDTO
        """
        return self._bundle

    @bundle.setter
    def bundle(self, bundle):
        """
        Sets the bundle of this ClassLoaderDiagnosticsDTO.
        Information about the Bundle that the ClassLoader belongs to, if any

        :param bundle: The bundle of this ClassLoaderDiagnosticsDTO.
        :type: BundleDTO
        """

        self._bundle = bundle

    @property
    def parent_class_loader(self):
        """
        Gets the parent_class_loader of this ClassLoaderDiagnosticsDTO.
        A ClassLoaderDiagnosticsDTO that provides information about the parent ClassLoader

        :return: The parent_class_loader of this ClassLoaderDiagnosticsDTO.
        :rtype: ClassLoaderDiagnosticsDTO
        """
        return self._parent_class_loader

    @parent_class_loader.setter
    def parent_class_loader(self, parent_class_loader):
        """
        Sets the parent_class_loader of this ClassLoaderDiagnosticsDTO.
        A ClassLoaderDiagnosticsDTO that provides information about the parent ClassLoader

        :param parent_class_loader: The parent_class_loader of this ClassLoaderDiagnosticsDTO.
        :type: ClassLoaderDiagnosticsDTO
        """

        self._parent_class_loader = parent_class_loader

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
        if not isinstance(other, ClassLoaderDiagnosticsDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
