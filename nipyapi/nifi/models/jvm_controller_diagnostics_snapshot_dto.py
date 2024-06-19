# coding: utf-8

"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.26.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class JVMControllerDiagnosticsSnapshotDTO(object):
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
        'primary_node': 'bool',
        'cluster_coordinator': 'bool',
        'max_timer_driven_threads': 'int',
        'max_event_driven_threads': 'int'
    }

    attribute_map = {
        'primary_node': 'primaryNode',
        'cluster_coordinator': 'clusterCoordinator',
        'max_timer_driven_threads': 'maxTimerDrivenThreads',
        'max_event_driven_threads': 'maxEventDrivenThreads'
    }

    def __init__(self, primary_node=None, cluster_coordinator=None, max_timer_driven_threads=None, max_event_driven_threads=None):
        """
        JVMControllerDiagnosticsSnapshotDTO - a model defined in Swagger
        """

        self._primary_node = None
        self._cluster_coordinator = None
        self._max_timer_driven_threads = None
        self._max_event_driven_threads = None

        if primary_node is not None:
          self.primary_node = primary_node
        if cluster_coordinator is not None:
          self.cluster_coordinator = cluster_coordinator
        if max_timer_driven_threads is not None:
          self.max_timer_driven_threads = max_timer_driven_threads
        if max_event_driven_threads is not None:
          self.max_event_driven_threads = max_event_driven_threads

    @property
    def primary_node(self):
        """
        Gets the primary_node of this JVMControllerDiagnosticsSnapshotDTO.
        Whether or not this node is primary node

        :return: The primary_node of this JVMControllerDiagnosticsSnapshotDTO.
        :rtype: bool
        """
        return self._primary_node

    @primary_node.setter
    def primary_node(self, primary_node):
        """
        Sets the primary_node of this JVMControllerDiagnosticsSnapshotDTO.
        Whether or not this node is primary node

        :param primary_node: The primary_node of this JVMControllerDiagnosticsSnapshotDTO.
        :type: bool
        """

        self._primary_node = primary_node

    @property
    def cluster_coordinator(self):
        """
        Gets the cluster_coordinator of this JVMControllerDiagnosticsSnapshotDTO.
        Whether or not this node is cluster coordinator

        :return: The cluster_coordinator of this JVMControllerDiagnosticsSnapshotDTO.
        :rtype: bool
        """
        return self._cluster_coordinator

    @cluster_coordinator.setter
    def cluster_coordinator(self, cluster_coordinator):
        """
        Sets the cluster_coordinator of this JVMControllerDiagnosticsSnapshotDTO.
        Whether or not this node is cluster coordinator

        :param cluster_coordinator: The cluster_coordinator of this JVMControllerDiagnosticsSnapshotDTO.
        :type: bool
        """

        self._cluster_coordinator = cluster_coordinator

    @property
    def max_timer_driven_threads(self):
        """
        Gets the max_timer_driven_threads of this JVMControllerDiagnosticsSnapshotDTO.
        The maximum number of timer-driven threads

        :return: The max_timer_driven_threads of this JVMControllerDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._max_timer_driven_threads

    @max_timer_driven_threads.setter
    def max_timer_driven_threads(self, max_timer_driven_threads):
        """
        Sets the max_timer_driven_threads of this JVMControllerDiagnosticsSnapshotDTO.
        The maximum number of timer-driven threads

        :param max_timer_driven_threads: The max_timer_driven_threads of this JVMControllerDiagnosticsSnapshotDTO.
        :type: int
        """

        self._max_timer_driven_threads = max_timer_driven_threads

    @property
    def max_event_driven_threads(self):
        """
        Gets the max_event_driven_threads of this JVMControllerDiagnosticsSnapshotDTO.
        The maximum number of event-driven threads

        :return: The max_event_driven_threads of this JVMControllerDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._max_event_driven_threads

    @max_event_driven_threads.setter
    def max_event_driven_threads(self, max_event_driven_threads):
        """
        Sets the max_event_driven_threads of this JVMControllerDiagnosticsSnapshotDTO.
        The maximum number of event-driven threads

        :param max_event_driven_threads: The max_event_driven_threads of this JVMControllerDiagnosticsSnapshotDTO.
        :type: int
        """

        self._max_event_driven_threads = max_event_driven_threads

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
        if not isinstance(other, JVMControllerDiagnosticsSnapshotDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
