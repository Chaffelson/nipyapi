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


class ProcessGroupImportEntity(object):
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
        'process_group_revision': 'RevisionDTO',
        'disconnected_node_acknowledged': 'bool',
        'versioned_flow_snapshot': 'RegisteredFlowSnapshot'
    }

    attribute_map = {
        'process_group_revision': 'processGroupRevision',
        'disconnected_node_acknowledged': 'disconnectedNodeAcknowledged',
        'versioned_flow_snapshot': 'versionedFlowSnapshot'
    }

    def __init__(self, process_group_revision=None, disconnected_node_acknowledged=None, versioned_flow_snapshot=None):
        """
        ProcessGroupImportEntity - a model defined in Swagger
        """

        self._process_group_revision = None
        self._disconnected_node_acknowledged = None
        self._versioned_flow_snapshot = None

        if process_group_revision is not None:
          self.process_group_revision = process_group_revision
        if disconnected_node_acknowledged is not None:
          self.disconnected_node_acknowledged = disconnected_node_acknowledged
        if versioned_flow_snapshot is not None:
          self.versioned_flow_snapshot = versioned_flow_snapshot

    @property
    def process_group_revision(self):
        """
        Gets the process_group_revision of this ProcessGroupImportEntity.
        The Revision for the Process Group

        :return: The process_group_revision of this ProcessGroupImportEntity.
        :rtype: RevisionDTO
        """
        return self._process_group_revision

    @process_group_revision.setter
    def process_group_revision(self, process_group_revision):
        """
        Sets the process_group_revision of this ProcessGroupImportEntity.
        The Revision for the Process Group

        :param process_group_revision: The process_group_revision of this ProcessGroupImportEntity.
        :type: RevisionDTO
        """

        self._process_group_revision = process_group_revision

    @property
    def disconnected_node_acknowledged(self):
        """
        Gets the disconnected_node_acknowledged of this ProcessGroupImportEntity.
        Acknowledges that this node is disconnected to allow for mutable requests to proceed.

        :return: The disconnected_node_acknowledged of this ProcessGroupImportEntity.
        :rtype: bool
        """
        return self._disconnected_node_acknowledged

    @disconnected_node_acknowledged.setter
    def disconnected_node_acknowledged(self, disconnected_node_acknowledged):
        """
        Sets the disconnected_node_acknowledged of this ProcessGroupImportEntity.
        Acknowledges that this node is disconnected to allow for mutable requests to proceed.

        :param disconnected_node_acknowledged: The disconnected_node_acknowledged of this ProcessGroupImportEntity.
        :type: bool
        """

        self._disconnected_node_acknowledged = disconnected_node_acknowledged

    @property
    def versioned_flow_snapshot(self):
        """
        Gets the versioned_flow_snapshot of this ProcessGroupImportEntity.
        The Versioned Flow Snapshot to import

        :return: The versioned_flow_snapshot of this ProcessGroupImportEntity.
        :rtype: RegisteredFlowSnapshot
        """
        return self._versioned_flow_snapshot

    @versioned_flow_snapshot.setter
    def versioned_flow_snapshot(self, versioned_flow_snapshot):
        """
        Sets the versioned_flow_snapshot of this ProcessGroupImportEntity.
        The Versioned Flow Snapshot to import

        :param versioned_flow_snapshot: The versioned_flow_snapshot of this ProcessGroupImportEntity.
        :type: RegisteredFlowSnapshot
        """

        self._versioned_flow_snapshot = versioned_flow_snapshot

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
        if not isinstance(other, ProcessGroupImportEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
