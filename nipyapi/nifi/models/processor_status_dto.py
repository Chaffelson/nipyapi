# coding: utf-8

"""
    NiFi Rest Api

    The Rest Api provides programmatic access to command and control a NiFi instance in real time. Start and                                              stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.7.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ProcessorStatusDTO(object):
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
        'group_id': 'str',
        'id': 'str',
        'name': 'str',
        'type': 'str',
        'run_status': 'str',
        'stats_last_refreshed': 'str',
        'aggregate_snapshot': 'ProcessorStatusSnapshotDTO',
        'node_snapshots': 'list[NodeProcessorStatusSnapshotDTO]'
    }

    attribute_map = {
        'group_id': 'groupId',
        'id': 'id',
        'name': 'name',
        'type': 'type',
        'run_status': 'runStatus',
        'stats_last_refreshed': 'statsLastRefreshed',
        'aggregate_snapshot': 'aggregateSnapshot',
        'node_snapshots': 'nodeSnapshots'
    }

    def __init__(self, group_id=None, id=None, name=None, type=None, run_status=None, stats_last_refreshed=None, aggregate_snapshot=None, node_snapshots=None):
        """
        ProcessorStatusDTO - a model defined in Swagger
        """

        self._group_id = None
        self._id = None
        self._name = None
        self._type = None
        self._run_status = None
        self._stats_last_refreshed = None
        self._aggregate_snapshot = None
        self._node_snapshots = None

        if group_id is not None:
          self.group_id = group_id
        if id is not None:
          self.id = id
        if name is not None:
          self.name = name
        if type is not None:
          self.type = type
        if run_status is not None:
          self.run_status = run_status
        if stats_last_refreshed is not None:
          self.stats_last_refreshed = stats_last_refreshed
        if aggregate_snapshot is not None:
          self.aggregate_snapshot = aggregate_snapshot
        if node_snapshots is not None:
          self.node_snapshots = node_snapshots

    @property
    def group_id(self):
        """
        Gets the group_id of this ProcessorStatusDTO.
        The unique ID of the process group that the Processor belongs to

        :return: The group_id of this ProcessorStatusDTO.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """
        Sets the group_id of this ProcessorStatusDTO.
        The unique ID of the process group that the Processor belongs to

        :param group_id: The group_id of this ProcessorStatusDTO.
        :type: str
        """

        self._group_id = group_id

    @property
    def id(self):
        """
        Gets the id of this ProcessorStatusDTO.
        The unique ID of the Processor

        :return: The id of this ProcessorStatusDTO.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ProcessorStatusDTO.
        The unique ID of the Processor

        :param id: The id of this ProcessorStatusDTO.
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ProcessorStatusDTO.
        The name of the Processor

        :return: The name of this ProcessorStatusDTO.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ProcessorStatusDTO.
        The name of the Processor

        :param name: The name of this ProcessorStatusDTO.
        :type: str
        """

        self._name = name

    @property
    def type(self):
        """
        Gets the type of this ProcessorStatusDTO.
        The type of the Processor

        :return: The type of this ProcessorStatusDTO.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ProcessorStatusDTO.
        The type of the Processor

        :param type: The type of this ProcessorStatusDTO.
        :type: str
        """

        self._type = type

    @property
    def run_status(self):
        """
        Gets the run_status of this ProcessorStatusDTO.
        The run status of the Processor

        :return: The run_status of this ProcessorStatusDTO.
        :rtype: str
        """
        return self._run_status

    @run_status.setter
    def run_status(self, run_status):
        """
        Sets the run_status of this ProcessorStatusDTO.
        The run status of the Processor

        :param run_status: The run_status of this ProcessorStatusDTO.
        :type: str
        """
        allowed_values = ["Running", "Stopped", "Disabled", "Invalid"]
        if run_status not in allowed_values:
            raise ValueError(
                "Invalid value for `run_status` ({0}), must be one of {1}"
                .format(run_status, allowed_values)
            )

        self._run_status = run_status

    @property
    def stats_last_refreshed(self):
        """
        Gets the stats_last_refreshed of this ProcessorStatusDTO.
        The timestamp of when the stats were last refreshed

        :return: The stats_last_refreshed of this ProcessorStatusDTO.
        :rtype: str
        """
        return self._stats_last_refreshed

    @stats_last_refreshed.setter
    def stats_last_refreshed(self, stats_last_refreshed):
        """
        Sets the stats_last_refreshed of this ProcessorStatusDTO.
        The timestamp of when the stats were last refreshed

        :param stats_last_refreshed: The stats_last_refreshed of this ProcessorStatusDTO.
        :type: str
        """

        self._stats_last_refreshed = stats_last_refreshed

    @property
    def aggregate_snapshot(self):
        """
        Gets the aggregate_snapshot of this ProcessorStatusDTO.
        A status snapshot that represents the aggregate stats of all nodes in the cluster. If the NiFi instance is a standalone instance, rather than a cluster, this represents the stats of the single instance.

        :return: The aggregate_snapshot of this ProcessorStatusDTO.
        :rtype: ProcessorStatusSnapshotDTO
        """
        return self._aggregate_snapshot

    @aggregate_snapshot.setter
    def aggregate_snapshot(self, aggregate_snapshot):
        """
        Sets the aggregate_snapshot of this ProcessorStatusDTO.
        A status snapshot that represents the aggregate stats of all nodes in the cluster. If the NiFi instance is a standalone instance, rather than a cluster, this represents the stats of the single instance.

        :param aggregate_snapshot: The aggregate_snapshot of this ProcessorStatusDTO.
        :type: ProcessorStatusSnapshotDTO
        """

        self._aggregate_snapshot = aggregate_snapshot

    @property
    def node_snapshots(self):
        """
        Gets the node_snapshots of this ProcessorStatusDTO.
        A status snapshot for each node in the cluster. If the NiFi instance is a standalone instance, rather than a cluster, this may be null.

        :return: The node_snapshots of this ProcessorStatusDTO.
        :rtype: list[NodeProcessorStatusSnapshotDTO]
        """
        return self._node_snapshots

    @node_snapshots.setter
    def node_snapshots(self, node_snapshots):
        """
        Sets the node_snapshots of this ProcessorStatusDTO.
        A status snapshot for each node in the cluster. If the NiFi instance is a standalone instance, rather than a cluster, this may be null.

        :param node_snapshots: The node_snapshots of this ProcessorStatusDTO.
        :type: list[NodeProcessorStatusSnapshotDTO]
        """

        self._node_snapshots = node_snapshots

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
        if not isinstance(other, ProcessorStatusDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
