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


class PortStatusDTO(object):
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
        'id': 'str',
        'group_id': 'str',
        'name': 'str',
        'transmitting': 'bool',
        'run_status': 'str',
        'stats_last_refreshed': 'str',
        'aggregate_snapshot': 'PortStatusSnapshotDTO',
        'node_snapshots': 'list[NodePortStatusSnapshotDTO]'
    }

    attribute_map = {
        'id': 'id',
        'group_id': 'groupId',
        'name': 'name',
        'transmitting': 'transmitting',
        'run_status': 'runStatus',
        'stats_last_refreshed': 'statsLastRefreshed',
        'aggregate_snapshot': 'aggregateSnapshot',
        'node_snapshots': 'nodeSnapshots'
    }

    def __init__(self, id=None, group_id=None, name=None, transmitting=None, run_status=None, stats_last_refreshed=None, aggregate_snapshot=None, node_snapshots=None):
        """
        PortStatusDTO - a model defined in Swagger
        """

        self._id = None
        self._group_id = None
        self._name = None
        self._transmitting = None
        self._run_status = None
        self._stats_last_refreshed = None
        self._aggregate_snapshot = None
        self._node_snapshots = None

        if id is not None:
          self.id = id
        if group_id is not None:
          self.group_id = group_id
        if name is not None:
          self.name = name
        if transmitting is not None:
          self.transmitting = transmitting
        if run_status is not None:
          self.run_status = run_status
        if stats_last_refreshed is not None:
          self.stats_last_refreshed = stats_last_refreshed
        if aggregate_snapshot is not None:
          self.aggregate_snapshot = aggregate_snapshot
        if node_snapshots is not None:
          self.node_snapshots = node_snapshots

    @property
    def id(self):
        """
        Gets the id of this PortStatusDTO.
        The id of the port.

        :return: The id of this PortStatusDTO.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this PortStatusDTO.
        The id of the port.

        :param id: The id of this PortStatusDTO.
        :type: str
        """

        self._id = id

    @property
    def group_id(self):
        """
        Gets the group_id of this PortStatusDTO.
        The id of the parent process group of the port.

        :return: The group_id of this PortStatusDTO.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """
        Sets the group_id of this PortStatusDTO.
        The id of the parent process group of the port.

        :param group_id: The group_id of this PortStatusDTO.
        :type: str
        """

        self._group_id = group_id

    @property
    def name(self):
        """
        Gets the name of this PortStatusDTO.
        The name of the port.

        :return: The name of this PortStatusDTO.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this PortStatusDTO.
        The name of the port.

        :param name: The name of this PortStatusDTO.
        :type: str
        """

        self._name = name

    @property
    def transmitting(self):
        """
        Gets the transmitting of this PortStatusDTO.
        Whether the port has incoming or outgoing connections to a remote NiFi.

        :return: The transmitting of this PortStatusDTO.
        :rtype: bool
        """
        return self._transmitting

    @transmitting.setter
    def transmitting(self, transmitting):
        """
        Sets the transmitting of this PortStatusDTO.
        Whether the port has incoming or outgoing connections to a remote NiFi.

        :param transmitting: The transmitting of this PortStatusDTO.
        :type: bool
        """

        self._transmitting = transmitting

    @property
    def run_status(self):
        """
        Gets the run_status of this PortStatusDTO.
        The run status of the port.

        :return: The run_status of this PortStatusDTO.
        :rtype: str
        """
        return self._run_status

    @run_status.setter
    def run_status(self, run_status):
        """
        Sets the run_status of this PortStatusDTO.
        The run status of the port.

        :param run_status: The run_status of this PortStatusDTO.
        :type: str
        """
        allowed_values = ["Running", "Stopped", "Validating", "Disabled", "Invalid"]
        if run_status not in allowed_values:
            raise ValueError(
                "Invalid value for `run_status` ({0}), must be one of {1}"
                .format(run_status, allowed_values)
            )

        self._run_status = run_status

    @property
    def stats_last_refreshed(self):
        """
        Gets the stats_last_refreshed of this PortStatusDTO.
        The time the status for the process group was last refreshed.

        :return: The stats_last_refreshed of this PortStatusDTO.
        :rtype: str
        """
        return self._stats_last_refreshed

    @stats_last_refreshed.setter
    def stats_last_refreshed(self, stats_last_refreshed):
        """
        Sets the stats_last_refreshed of this PortStatusDTO.
        The time the status for the process group was last refreshed.

        :param stats_last_refreshed: The stats_last_refreshed of this PortStatusDTO.
        :type: str
        """

        self._stats_last_refreshed = stats_last_refreshed

    @property
    def aggregate_snapshot(self):
        """
        Gets the aggregate_snapshot of this PortStatusDTO.
        A status snapshot that represents the aggregate stats of all nodes in the cluster. If the NiFi instance is a standalone instance, rather than a cluster, this represents the stats of the single instance.

        :return: The aggregate_snapshot of this PortStatusDTO.
        :rtype: PortStatusSnapshotDTO
        """
        return self._aggregate_snapshot

    @aggregate_snapshot.setter
    def aggregate_snapshot(self, aggregate_snapshot):
        """
        Sets the aggregate_snapshot of this PortStatusDTO.
        A status snapshot that represents the aggregate stats of all nodes in the cluster. If the NiFi instance is a standalone instance, rather than a cluster, this represents the stats of the single instance.

        :param aggregate_snapshot: The aggregate_snapshot of this PortStatusDTO.
        :type: PortStatusSnapshotDTO
        """

        self._aggregate_snapshot = aggregate_snapshot

    @property
    def node_snapshots(self):
        """
        Gets the node_snapshots of this PortStatusDTO.
        A status snapshot for each node in the cluster. If the NiFi instance is a standalone instance, rather than a cluster, this may be null.

        :return: The node_snapshots of this PortStatusDTO.
        :rtype: list[NodePortStatusSnapshotDTO]
        """
        return self._node_snapshots

    @node_snapshots.setter
    def node_snapshots(self, node_snapshots):
        """
        Sets the node_snapshots of this PortStatusDTO.
        A status snapshot for each node in the cluster. If the NiFi instance is a standalone instance, rather than a cluster, this may be null.

        :param node_snapshots: The node_snapshots of this PortStatusDTO.
        :type: list[NodePortStatusSnapshotDTO]
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
        if not isinstance(other, PortStatusDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
