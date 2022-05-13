# coding: utf-8

"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.16.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class GCDiagnosticsSnapshotDTO(object):
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
        'timestamp': 'datetime',
        'collection_count': 'int',
        'collection_millis': 'int'
    }

    attribute_map = {
        'timestamp': 'timestamp',
        'collection_count': 'collectionCount',
        'collection_millis': 'collectionMillis'
    }

    def __init__(self, timestamp=None, collection_count=None, collection_millis=None):
        """
        GCDiagnosticsSnapshotDTO - a model defined in Swagger
        """

        self._timestamp = None
        self._collection_count = None
        self._collection_millis = None

        if timestamp is not None:
          self.timestamp = timestamp
        if collection_count is not None:
          self.collection_count = collection_count
        if collection_millis is not None:
          self.collection_millis = collection_millis

    @property
    def timestamp(self):
        """
        Gets the timestamp of this GCDiagnosticsSnapshotDTO.
        The timestamp of when the Snapshot was taken

        :return: The timestamp of this GCDiagnosticsSnapshotDTO.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Sets the timestamp of this GCDiagnosticsSnapshotDTO.
        The timestamp of when the Snapshot was taken

        :param timestamp: The timestamp of this GCDiagnosticsSnapshotDTO.
        :type: datetime
        """

        self._timestamp = timestamp

    @property
    def collection_count(self):
        """
        Gets the collection_count of this GCDiagnosticsSnapshotDTO.
        The number of times that Garbage Collection has occurred

        :return: The collection_count of this GCDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._collection_count

    @collection_count.setter
    def collection_count(self, collection_count):
        """
        Sets the collection_count of this GCDiagnosticsSnapshotDTO.
        The number of times that Garbage Collection has occurred

        :param collection_count: The collection_count of this GCDiagnosticsSnapshotDTO.
        :type: int
        """

        self._collection_count = collection_count

    @property
    def collection_millis(self):
        """
        Gets the collection_millis of this GCDiagnosticsSnapshotDTO.
        The number of milliseconds that the Garbage Collector spent performing Garbage Collection duties

        :return: The collection_millis of this GCDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._collection_millis

    @collection_millis.setter
    def collection_millis(self, collection_millis):
        """
        Sets the collection_millis of this GCDiagnosticsSnapshotDTO.
        The number of milliseconds that the Garbage Collector spent performing Garbage Collection duties

        :param collection_millis: The collection_millis of this GCDiagnosticsSnapshotDTO.
        :type: int
        """

        self._collection_millis = collection_millis

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
        if not isinstance(other, GCDiagnosticsSnapshotDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
