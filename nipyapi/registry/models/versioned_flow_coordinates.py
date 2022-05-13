# coding: utf-8

"""
    Apache NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 1.16.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class VersionedFlowCoordinates(object):
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
        'registry_url': 'str',
        'bucket_id': 'str',
        'flow_id': 'str',
        'version': 'int',
        'latest': 'bool'
    }

    attribute_map = {
        'registry_url': 'registryUrl',
        'bucket_id': 'bucketId',
        'flow_id': 'flowId',
        'version': 'version',
        'latest': 'latest'
    }

    def __init__(self, registry_url=None, bucket_id=None, flow_id=None, version=None, latest=None):
        """
        VersionedFlowCoordinates - a model defined in Swagger
        """

        self._registry_url = None
        self._bucket_id = None
        self._flow_id = None
        self._version = None
        self._latest = None

        if registry_url is not None:
          self.registry_url = registry_url
        if bucket_id is not None:
          self.bucket_id = bucket_id
        if flow_id is not None:
          self.flow_id = flow_id
        if version is not None:
          self.version = version
        if latest is not None:
          self.latest = latest

    @property
    def registry_url(self):
        """
        Gets the registry_url of this VersionedFlowCoordinates.
        The URL of the Flow Registry that contains the flow

        :return: The registry_url of this VersionedFlowCoordinates.
        :rtype: str
        """
        return self._registry_url

    @registry_url.setter
    def registry_url(self, registry_url):
        """
        Sets the registry_url of this VersionedFlowCoordinates.
        The URL of the Flow Registry that contains the flow

        :param registry_url: The registry_url of this VersionedFlowCoordinates.
        :type: str
        """

        self._registry_url = registry_url

    @property
    def bucket_id(self):
        """
        Gets the bucket_id of this VersionedFlowCoordinates.
        The UUID of the bucket that the flow resides in

        :return: The bucket_id of this VersionedFlowCoordinates.
        :rtype: str
        """
        return self._bucket_id

    @bucket_id.setter
    def bucket_id(self, bucket_id):
        """
        Sets the bucket_id of this VersionedFlowCoordinates.
        The UUID of the bucket that the flow resides in

        :param bucket_id: The bucket_id of this VersionedFlowCoordinates.
        :type: str
        """

        self._bucket_id = bucket_id

    @property
    def flow_id(self):
        """
        Gets the flow_id of this VersionedFlowCoordinates.
        The UUID of the flow

        :return: The flow_id of this VersionedFlowCoordinates.
        :rtype: str
        """
        return self._flow_id

    @flow_id.setter
    def flow_id(self, flow_id):
        """
        Sets the flow_id of this VersionedFlowCoordinates.
        The UUID of the flow

        :param flow_id: The flow_id of this VersionedFlowCoordinates.
        :type: str
        """

        self._flow_id = flow_id

    @property
    def version(self):
        """
        Gets the version of this VersionedFlowCoordinates.
        The version of the flow

        :return: The version of this VersionedFlowCoordinates.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this VersionedFlowCoordinates.
        The version of the flow

        :param version: The version of this VersionedFlowCoordinates.
        :type: int
        """

        self._version = version

    @property
    def latest(self):
        """
        Gets the latest of this VersionedFlowCoordinates.
        Whether or not these coordinates point to the latest version of the flow

        :return: The latest of this VersionedFlowCoordinates.
        :rtype: bool
        """
        return self._latest

    @latest.setter
    def latest(self, latest):
        """
        Sets the latest of this VersionedFlowCoordinates.
        Whether or not these coordinates point to the latest version of the flow

        :param latest: The latest of this VersionedFlowCoordinates.
        :type: bool
        """

        self._latest = latest

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
        if not isinstance(other, VersionedFlowCoordinates):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
