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


class FlowRegistryBucket(object):
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
        'identifier': 'str',
        'name': 'str',
        'description': 'str',
        'created_timestamp': 'int',
        'permissions': 'FlowRegistryPermissions'
    }

    attribute_map = {
        'identifier': 'identifier',
        'name': 'name',
        'description': 'description',
        'created_timestamp': 'createdTimestamp',
        'permissions': 'permissions'
    }

    def __init__(self, identifier=None, name=None, description=None, created_timestamp=None, permissions=None):
        """
        FlowRegistryBucket - a model defined in Swagger
        """

        self._identifier = None
        self._name = None
        self._description = None
        self._created_timestamp = None
        self._permissions = None

        if identifier is not None:
          self.identifier = identifier
        if name is not None:
          self.name = name
        if description is not None:
          self.description = description
        if created_timestamp is not None:
          self.created_timestamp = created_timestamp
        if permissions is not None:
          self.permissions = permissions

    @property
    def identifier(self):
        """
        Gets the identifier of this FlowRegistryBucket.

        :return: The identifier of this FlowRegistryBucket.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this FlowRegistryBucket.

        :param identifier: The identifier of this FlowRegistryBucket.
        :type: str
        """

        self._identifier = identifier

    @property
    def name(self):
        """
        Gets the name of this FlowRegistryBucket.

        :return: The name of this FlowRegistryBucket.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this FlowRegistryBucket.

        :param name: The name of this FlowRegistryBucket.
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this FlowRegistryBucket.

        :return: The description of this FlowRegistryBucket.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this FlowRegistryBucket.

        :param description: The description of this FlowRegistryBucket.
        :type: str
        """

        self._description = description

    @property
    def created_timestamp(self):
        """
        Gets the created_timestamp of this FlowRegistryBucket.

        :return: The created_timestamp of this FlowRegistryBucket.
        :rtype: int
        """
        return self._created_timestamp

    @created_timestamp.setter
    def created_timestamp(self, created_timestamp):
        """
        Sets the created_timestamp of this FlowRegistryBucket.

        :param created_timestamp: The created_timestamp of this FlowRegistryBucket.
        :type: int
        """

        self._created_timestamp = created_timestamp

    @property
    def permissions(self):
        """
        Gets the permissions of this FlowRegistryBucket.

        :return: The permissions of this FlowRegistryBucket.
        :rtype: FlowRegistryPermissions
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """
        Sets the permissions of this FlowRegistryBucket.

        :param permissions: The permissions of this FlowRegistryBucket.
        :type: FlowRegistryPermissions
        """

        self._permissions = permissions

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
        if not isinstance(other, FlowRegistryBucket):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other