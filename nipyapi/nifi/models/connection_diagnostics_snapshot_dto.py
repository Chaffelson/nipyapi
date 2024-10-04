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


class ConnectionDiagnosticsSnapshotDTO(object):
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
        'total_flow_file_count': 'int',
        'total_byte_count': 'int',
        'node_identifier': 'str',
        'local_queue_partition': 'LocalQueuePartitionDTO',
        'remote_queue_partitions': 'list[RemoteQueuePartitionDTO]'
    }

    attribute_map = {
        'total_flow_file_count': 'totalFlowFileCount',
        'total_byte_count': 'totalByteCount',
        'node_identifier': 'nodeIdentifier',
        'local_queue_partition': 'localQueuePartition',
        'remote_queue_partitions': 'remoteQueuePartitions'
    }

    def __init__(self, total_flow_file_count=None, total_byte_count=None, node_identifier=None, local_queue_partition=None, remote_queue_partitions=None):
        """
        ConnectionDiagnosticsSnapshotDTO - a model defined in Swagger
        """

        self._total_flow_file_count = None
        self._total_byte_count = None
        self._node_identifier = None
        self._local_queue_partition = None
        self._remote_queue_partitions = None

        if total_flow_file_count is not None:
          self.total_flow_file_count = total_flow_file_count
        if total_byte_count is not None:
          self.total_byte_count = total_byte_count
        if node_identifier is not None:
          self.node_identifier = node_identifier
        if local_queue_partition is not None:
          self.local_queue_partition = local_queue_partition
        if remote_queue_partitions is not None:
          self.remote_queue_partitions = remote_queue_partitions

    @property
    def total_flow_file_count(self):
        """
        Gets the total_flow_file_count of this ConnectionDiagnosticsSnapshotDTO.
        Total number of FlowFiles owned by the Connection

        :return: The total_flow_file_count of this ConnectionDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._total_flow_file_count

    @total_flow_file_count.setter
    def total_flow_file_count(self, total_flow_file_count):
        """
        Sets the total_flow_file_count of this ConnectionDiagnosticsSnapshotDTO.
        Total number of FlowFiles owned by the Connection

        :param total_flow_file_count: The total_flow_file_count of this ConnectionDiagnosticsSnapshotDTO.
        :type: int
        """

        self._total_flow_file_count = total_flow_file_count

    @property
    def total_byte_count(self):
        """
        Gets the total_byte_count of this ConnectionDiagnosticsSnapshotDTO.
        Total number of bytes that make up the content for the FlowFiles owned by this Connection

        :return: The total_byte_count of this ConnectionDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._total_byte_count

    @total_byte_count.setter
    def total_byte_count(self, total_byte_count):
        """
        Sets the total_byte_count of this ConnectionDiagnosticsSnapshotDTO.
        Total number of bytes that make up the content for the FlowFiles owned by this Connection

        :param total_byte_count: The total_byte_count of this ConnectionDiagnosticsSnapshotDTO.
        :type: int
        """

        self._total_byte_count = total_byte_count

    @property
    def node_identifier(self):
        """
        Gets the node_identifier of this ConnectionDiagnosticsSnapshotDTO.
        The Node Identifier that this information pertains to

        :return: The node_identifier of this ConnectionDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._node_identifier

    @node_identifier.setter
    def node_identifier(self, node_identifier):
        """
        Sets the node_identifier of this ConnectionDiagnosticsSnapshotDTO.
        The Node Identifier that this information pertains to

        :param node_identifier: The node_identifier of this ConnectionDiagnosticsSnapshotDTO.
        :type: str
        """

        self._node_identifier = node_identifier

    @property
    def local_queue_partition(self):
        """
        Gets the local_queue_partition of this ConnectionDiagnosticsSnapshotDTO.
        The local queue partition, from which components can pull FlowFiles on this node.

        :return: The local_queue_partition of this ConnectionDiagnosticsSnapshotDTO.
        :rtype: LocalQueuePartitionDTO
        """
        return self._local_queue_partition

    @local_queue_partition.setter
    def local_queue_partition(self, local_queue_partition):
        """
        Sets the local_queue_partition of this ConnectionDiagnosticsSnapshotDTO.
        The local queue partition, from which components can pull FlowFiles on this node.

        :param local_queue_partition: The local_queue_partition of this ConnectionDiagnosticsSnapshotDTO.
        :type: LocalQueuePartitionDTO
        """

        self._local_queue_partition = local_queue_partition

    @property
    def remote_queue_partitions(self):
        """
        Gets the remote_queue_partitions of this ConnectionDiagnosticsSnapshotDTO.

        :return: The remote_queue_partitions of this ConnectionDiagnosticsSnapshotDTO.
        :rtype: list[RemoteQueuePartitionDTO]
        """
        return self._remote_queue_partitions

    @remote_queue_partitions.setter
    def remote_queue_partitions(self, remote_queue_partitions):
        """
        Sets the remote_queue_partitions of this ConnectionDiagnosticsSnapshotDTO.

        :param remote_queue_partitions: The remote_queue_partitions of this ConnectionDiagnosticsSnapshotDTO.
        :type: list[RemoteQueuePartitionDTO]
        """

        self._remote_queue_partitions = remote_queue_partitions

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
        if not isinstance(other, ConnectionDiagnosticsSnapshotDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
