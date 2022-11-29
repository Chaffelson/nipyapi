# coding: utf-8

"""
    Apache NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 1.19.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ControllerServiceDefinition(object):
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
        'class_name': 'str',
        'group_id': 'str',
        'artifact_id': 'str',
        'version': 'str'
    }

    attribute_map = {
        'class_name': 'className',
        'group_id': 'groupId',
        'artifact_id': 'artifactId',
        'version': 'version'
    }

    def __init__(self, class_name=None, group_id=None, artifact_id=None, version=None):
        """
        ControllerServiceDefinition - a model defined in Swagger
        """

        self._class_name = None
        self._group_id = None
        self._artifact_id = None
        self._version = None

        if class_name is not None:
          self.class_name = class_name
        if group_id is not None:
          self.group_id = group_id
        if artifact_id is not None:
          self.artifact_id = artifact_id
        if version is not None:
          self.version = version

    @property
    def class_name(self):
        """
        Gets the class_name of this ControllerServiceDefinition.
        The class name of the service API

        :return: The class_name of this ControllerServiceDefinition.
        :rtype: str
        """
        return self._class_name

    @class_name.setter
    def class_name(self, class_name):
        """
        Sets the class_name of this ControllerServiceDefinition.
        The class name of the service API

        :param class_name: The class_name of this ControllerServiceDefinition.
        :type: str
        """

        self._class_name = class_name

    @property
    def group_id(self):
        """
        Gets the group_id of this ControllerServiceDefinition.
        The group id of the service API

        :return: The group_id of this ControllerServiceDefinition.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """
        Sets the group_id of this ControllerServiceDefinition.
        The group id of the service API

        :param group_id: The group_id of this ControllerServiceDefinition.
        :type: str
        """

        self._group_id = group_id

    @property
    def artifact_id(self):
        """
        Gets the artifact_id of this ControllerServiceDefinition.
        The artifact id of the service API

        :return: The artifact_id of this ControllerServiceDefinition.
        :rtype: str
        """
        return self._artifact_id

    @artifact_id.setter
    def artifact_id(self, artifact_id):
        """
        Sets the artifact_id of this ControllerServiceDefinition.
        The artifact id of the service API

        :param artifact_id: The artifact_id of this ControllerServiceDefinition.
        :type: str
        """

        self._artifact_id = artifact_id

    @property
    def version(self):
        """
        Gets the version of this ControllerServiceDefinition.
        The version of the service API

        :return: The version of this ControllerServiceDefinition.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this ControllerServiceDefinition.
        The version of the service API

        :param version: The version of this ControllerServiceDefinition.
        :type: str
        """

        self._version = version

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
        if not isinstance(other, ControllerServiceDefinition):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
