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


class GarbageCollectionDiagnosticsDTO(object):
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
        'memory_manager_name': 'str',
        'snapshots': 'list[GCDiagnosticsSnapshotDTO]'
    }

    attribute_map = {
        'memory_manager_name': 'memoryManagerName',
        'snapshots': 'snapshots'
    }

    def __init__(self, memory_manager_name=None, snapshots=None):
        """
        GarbageCollectionDiagnosticsDTO - a model defined in Swagger
        """

        self._memory_manager_name = None
        self._snapshots = None

        if memory_manager_name is not None:
          self.memory_manager_name = memory_manager_name
        if snapshots is not None:
          self.snapshots = snapshots

    @property
    def memory_manager_name(self):
        """
        Gets the memory_manager_name of this GarbageCollectionDiagnosticsDTO.
        The name of the Memory Manager that this Garbage Collection information pertains to

        :return: The memory_manager_name of this GarbageCollectionDiagnosticsDTO.
        :rtype: str
        """
        return self._memory_manager_name

    @memory_manager_name.setter
    def memory_manager_name(self, memory_manager_name):
        """
        Sets the memory_manager_name of this GarbageCollectionDiagnosticsDTO.
        The name of the Memory Manager that this Garbage Collection information pertains to

        :param memory_manager_name: The memory_manager_name of this GarbageCollectionDiagnosticsDTO.
        :type: str
        """

        self._memory_manager_name = memory_manager_name

    @property
    def snapshots(self):
        """
        Gets the snapshots of this GarbageCollectionDiagnosticsDTO.
        A list of snapshots that have been taken to determine the health of the JVM's heap

        :return: The snapshots of this GarbageCollectionDiagnosticsDTO.
        :rtype: list[GCDiagnosticsSnapshotDTO]
        """
        return self._snapshots

    @snapshots.setter
    def snapshots(self, snapshots):
        """
        Sets the snapshots of this GarbageCollectionDiagnosticsDTO.
        A list of snapshots that have been taken to determine the health of the JVM's heap

        :param snapshots: The snapshots of this GarbageCollectionDiagnosticsDTO.
        :type: list[GCDiagnosticsSnapshotDTO]
        """

        self._snapshots = snapshots

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
        if not isinstance(other, GarbageCollectionDiagnosticsDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
