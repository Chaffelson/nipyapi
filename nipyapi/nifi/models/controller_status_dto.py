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


class ControllerStatusDTO(object):
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
        'active_thread_count': 'int',
        'terminated_thread_count': 'int',
        'queued': 'str',
        'flow_files_queued': 'int',
        'bytes_queued': 'int',
        'running_count': 'int',
        'stopped_count': 'int',
        'invalid_count': 'int',
        'disabled_count': 'int',
        'active_remote_port_count': 'int',
        'inactive_remote_port_count': 'int',
        'up_to_date_count': 'int',
        'locally_modified_count': 'int',
        'stale_count': 'int',
        'locally_modified_and_stale_count': 'int',
        'sync_failure_count': 'int'
    }

    attribute_map = {
        'active_thread_count': 'activeThreadCount',
        'terminated_thread_count': 'terminatedThreadCount',
        'queued': 'queued',
        'flow_files_queued': 'flowFilesQueued',
        'bytes_queued': 'bytesQueued',
        'running_count': 'runningCount',
        'stopped_count': 'stoppedCount',
        'invalid_count': 'invalidCount',
        'disabled_count': 'disabledCount',
        'active_remote_port_count': 'activeRemotePortCount',
        'inactive_remote_port_count': 'inactiveRemotePortCount',
        'up_to_date_count': 'upToDateCount',
        'locally_modified_count': 'locallyModifiedCount',
        'stale_count': 'staleCount',
        'locally_modified_and_stale_count': 'locallyModifiedAndStaleCount',
        'sync_failure_count': 'syncFailureCount'
    }

    def __init__(self, active_thread_count=None, terminated_thread_count=None, queued=None, flow_files_queued=None, bytes_queued=None, running_count=None, stopped_count=None, invalid_count=None, disabled_count=None, active_remote_port_count=None, inactive_remote_port_count=None, up_to_date_count=None, locally_modified_count=None, stale_count=None, locally_modified_and_stale_count=None, sync_failure_count=None):
        """
        ControllerStatusDTO - a model defined in Swagger
        """

        self._active_thread_count = None
        self._terminated_thread_count = None
        self._queued = None
        self._flow_files_queued = None
        self._bytes_queued = None
        self._running_count = None
        self._stopped_count = None
        self._invalid_count = None
        self._disabled_count = None
        self._active_remote_port_count = None
        self._inactive_remote_port_count = None
        self._up_to_date_count = None
        self._locally_modified_count = None
        self._stale_count = None
        self._locally_modified_and_stale_count = None
        self._sync_failure_count = None

        if active_thread_count is not None:
          self.active_thread_count = active_thread_count
        if terminated_thread_count is not None:
          self.terminated_thread_count = terminated_thread_count
        if queued is not None:
          self.queued = queued
        if flow_files_queued is not None:
          self.flow_files_queued = flow_files_queued
        if bytes_queued is not None:
          self.bytes_queued = bytes_queued
        if running_count is not None:
          self.running_count = running_count
        if stopped_count is not None:
          self.stopped_count = stopped_count
        if invalid_count is not None:
          self.invalid_count = invalid_count
        if disabled_count is not None:
          self.disabled_count = disabled_count
        if active_remote_port_count is not None:
          self.active_remote_port_count = active_remote_port_count
        if inactive_remote_port_count is not None:
          self.inactive_remote_port_count = inactive_remote_port_count
        if up_to_date_count is not None:
          self.up_to_date_count = up_to_date_count
        if locally_modified_count is not None:
          self.locally_modified_count = locally_modified_count
        if stale_count is not None:
          self.stale_count = stale_count
        if locally_modified_and_stale_count is not None:
          self.locally_modified_and_stale_count = locally_modified_and_stale_count
        if sync_failure_count is not None:
          self.sync_failure_count = sync_failure_count

    @property
    def active_thread_count(self):
        """
        Gets the active_thread_count of this ControllerStatusDTO.
        The number of active threads in the NiFi.

        :return: The active_thread_count of this ControllerStatusDTO.
        :rtype: int
        """
        return self._active_thread_count

    @active_thread_count.setter
    def active_thread_count(self, active_thread_count):
        """
        Sets the active_thread_count of this ControllerStatusDTO.
        The number of active threads in the NiFi.

        :param active_thread_count: The active_thread_count of this ControllerStatusDTO.
        :type: int
        """

        self._active_thread_count = active_thread_count

    @property
    def terminated_thread_count(self):
        """
        Gets the terminated_thread_count of this ControllerStatusDTO.
        The number of terminated threads in the NiFi.

        :return: The terminated_thread_count of this ControllerStatusDTO.
        :rtype: int
        """
        return self._terminated_thread_count

    @terminated_thread_count.setter
    def terminated_thread_count(self, terminated_thread_count):
        """
        Sets the terminated_thread_count of this ControllerStatusDTO.
        The number of terminated threads in the NiFi.

        :param terminated_thread_count: The terminated_thread_count of this ControllerStatusDTO.
        :type: int
        """

        self._terminated_thread_count = terminated_thread_count

    @property
    def queued(self):
        """
        Gets the queued of this ControllerStatusDTO.
        The number of flowfiles queued in the NiFi.

        :return: The queued of this ControllerStatusDTO.
        :rtype: str
        """
        return self._queued

    @queued.setter
    def queued(self, queued):
        """
        Sets the queued of this ControllerStatusDTO.
        The number of flowfiles queued in the NiFi.

        :param queued: The queued of this ControllerStatusDTO.
        :type: str
        """

        self._queued = queued

    @property
    def flow_files_queued(self):
        """
        Gets the flow_files_queued of this ControllerStatusDTO.
        The number of FlowFiles queued across the entire flow

        :return: The flow_files_queued of this ControllerStatusDTO.
        :rtype: int
        """
        return self._flow_files_queued

    @flow_files_queued.setter
    def flow_files_queued(self, flow_files_queued):
        """
        Sets the flow_files_queued of this ControllerStatusDTO.
        The number of FlowFiles queued across the entire flow

        :param flow_files_queued: The flow_files_queued of this ControllerStatusDTO.
        :type: int
        """

        self._flow_files_queued = flow_files_queued

    @property
    def bytes_queued(self):
        """
        Gets the bytes_queued of this ControllerStatusDTO.
        The size of the FlowFiles queued across the entire flow

        :return: The bytes_queued of this ControllerStatusDTO.
        :rtype: int
        """
        return self._bytes_queued

    @bytes_queued.setter
    def bytes_queued(self, bytes_queued):
        """
        Sets the bytes_queued of this ControllerStatusDTO.
        The size of the FlowFiles queued across the entire flow

        :param bytes_queued: The bytes_queued of this ControllerStatusDTO.
        :type: int
        """

        self._bytes_queued = bytes_queued

    @property
    def running_count(self):
        """
        Gets the running_count of this ControllerStatusDTO.
        The number of running components in the NiFi.

        :return: The running_count of this ControllerStatusDTO.
        :rtype: int
        """
        return self._running_count

    @running_count.setter
    def running_count(self, running_count):
        """
        Sets the running_count of this ControllerStatusDTO.
        The number of running components in the NiFi.

        :param running_count: The running_count of this ControllerStatusDTO.
        :type: int
        """

        self._running_count = running_count

    @property
    def stopped_count(self):
        """
        Gets the stopped_count of this ControllerStatusDTO.
        The number of stopped components in the NiFi.

        :return: The stopped_count of this ControllerStatusDTO.
        :rtype: int
        """
        return self._stopped_count

    @stopped_count.setter
    def stopped_count(self, stopped_count):
        """
        Sets the stopped_count of this ControllerStatusDTO.
        The number of stopped components in the NiFi.

        :param stopped_count: The stopped_count of this ControllerStatusDTO.
        :type: int
        """

        self._stopped_count = stopped_count

    @property
    def invalid_count(self):
        """
        Gets the invalid_count of this ControllerStatusDTO.
        The number of invalid components in the NiFi.

        :return: The invalid_count of this ControllerStatusDTO.
        :rtype: int
        """
        return self._invalid_count

    @invalid_count.setter
    def invalid_count(self, invalid_count):
        """
        Sets the invalid_count of this ControllerStatusDTO.
        The number of invalid components in the NiFi.

        :param invalid_count: The invalid_count of this ControllerStatusDTO.
        :type: int
        """

        self._invalid_count = invalid_count

    @property
    def disabled_count(self):
        """
        Gets the disabled_count of this ControllerStatusDTO.
        The number of disabled components in the NiFi.

        :return: The disabled_count of this ControllerStatusDTO.
        :rtype: int
        """
        return self._disabled_count

    @disabled_count.setter
    def disabled_count(self, disabled_count):
        """
        Sets the disabled_count of this ControllerStatusDTO.
        The number of disabled components in the NiFi.

        :param disabled_count: The disabled_count of this ControllerStatusDTO.
        :type: int
        """

        self._disabled_count = disabled_count

    @property
    def active_remote_port_count(self):
        """
        Gets the active_remote_port_count of this ControllerStatusDTO.
        The number of active remote ports in the NiFi.

        :return: The active_remote_port_count of this ControllerStatusDTO.
        :rtype: int
        """
        return self._active_remote_port_count

    @active_remote_port_count.setter
    def active_remote_port_count(self, active_remote_port_count):
        """
        Sets the active_remote_port_count of this ControllerStatusDTO.
        The number of active remote ports in the NiFi.

        :param active_remote_port_count: The active_remote_port_count of this ControllerStatusDTO.
        :type: int
        """

        self._active_remote_port_count = active_remote_port_count

    @property
    def inactive_remote_port_count(self):
        """
        Gets the inactive_remote_port_count of this ControllerStatusDTO.
        The number of inactive remote ports in the NiFi.

        :return: The inactive_remote_port_count of this ControllerStatusDTO.
        :rtype: int
        """
        return self._inactive_remote_port_count

    @inactive_remote_port_count.setter
    def inactive_remote_port_count(self, inactive_remote_port_count):
        """
        Sets the inactive_remote_port_count of this ControllerStatusDTO.
        The number of inactive remote ports in the NiFi.

        :param inactive_remote_port_count: The inactive_remote_port_count of this ControllerStatusDTO.
        :type: int
        """

        self._inactive_remote_port_count = inactive_remote_port_count

    @property
    def up_to_date_count(self):
        """
        Gets the up_to_date_count of this ControllerStatusDTO.
        The number of up to date versioned process groups in the NiFi.

        :return: The up_to_date_count of this ControllerStatusDTO.
        :rtype: int
        """
        return self._up_to_date_count

    @up_to_date_count.setter
    def up_to_date_count(self, up_to_date_count):
        """
        Sets the up_to_date_count of this ControllerStatusDTO.
        The number of up to date versioned process groups in the NiFi.

        :param up_to_date_count: The up_to_date_count of this ControllerStatusDTO.
        :type: int
        """

        self._up_to_date_count = up_to_date_count

    @property
    def locally_modified_count(self):
        """
        Gets the locally_modified_count of this ControllerStatusDTO.
        The number of locally modified versioned process groups in the NiFi.

        :return: The locally_modified_count of this ControllerStatusDTO.
        :rtype: int
        """
        return self._locally_modified_count

    @locally_modified_count.setter
    def locally_modified_count(self, locally_modified_count):
        """
        Sets the locally_modified_count of this ControllerStatusDTO.
        The number of locally modified versioned process groups in the NiFi.

        :param locally_modified_count: The locally_modified_count of this ControllerStatusDTO.
        :type: int
        """

        self._locally_modified_count = locally_modified_count

    @property
    def stale_count(self):
        """
        Gets the stale_count of this ControllerStatusDTO.
        The number of stale versioned process groups in the NiFi.

        :return: The stale_count of this ControllerStatusDTO.
        :rtype: int
        """
        return self._stale_count

    @stale_count.setter
    def stale_count(self, stale_count):
        """
        Sets the stale_count of this ControllerStatusDTO.
        The number of stale versioned process groups in the NiFi.

        :param stale_count: The stale_count of this ControllerStatusDTO.
        :type: int
        """

        self._stale_count = stale_count

    @property
    def locally_modified_and_stale_count(self):
        """
        Gets the locally_modified_and_stale_count of this ControllerStatusDTO.
        The number of locally modified and stale versioned process groups in the NiFi.

        :return: The locally_modified_and_stale_count of this ControllerStatusDTO.
        :rtype: int
        """
        return self._locally_modified_and_stale_count

    @locally_modified_and_stale_count.setter
    def locally_modified_and_stale_count(self, locally_modified_and_stale_count):
        """
        Sets the locally_modified_and_stale_count of this ControllerStatusDTO.
        The number of locally modified and stale versioned process groups in the NiFi.

        :param locally_modified_and_stale_count: The locally_modified_and_stale_count of this ControllerStatusDTO.
        :type: int
        """

        self._locally_modified_and_stale_count = locally_modified_and_stale_count

    @property
    def sync_failure_count(self):
        """
        Gets the sync_failure_count of this ControllerStatusDTO.
        The number of versioned process groups in the NiFi that are unable to sync to a registry.

        :return: The sync_failure_count of this ControllerStatusDTO.
        :rtype: int
        """
        return self._sync_failure_count

    @sync_failure_count.setter
    def sync_failure_count(self, sync_failure_count):
        """
        Sets the sync_failure_count of this ControllerStatusDTO.
        The number of versioned process groups in the NiFi that are unable to sync to a registry.

        :param sync_failure_count: The sync_failure_count of this ControllerStatusDTO.
        :type: int
        """

        self._sync_failure_count = sync_failure_count

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
        if not isinstance(other, ControllerStatusDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
