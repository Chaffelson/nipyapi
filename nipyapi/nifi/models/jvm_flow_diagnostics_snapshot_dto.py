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


class JVMFlowDiagnosticsSnapshotDTO(object):
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
        'uptime': 'str',
        'time_zone': 'str',
        'active_timer_driven_threads': 'int',
        'active_event_driven_threads': 'int',
        'bundles_loaded': 'list[BundleDTO]'
    }

    attribute_map = {
        'uptime': 'uptime',
        'time_zone': 'timeZone',
        'active_timer_driven_threads': 'activeTimerDrivenThreads',
        'active_event_driven_threads': 'activeEventDrivenThreads',
        'bundles_loaded': 'bundlesLoaded'
    }

    def __init__(self, uptime=None, time_zone=None, active_timer_driven_threads=None, active_event_driven_threads=None, bundles_loaded=None):
        """
        JVMFlowDiagnosticsSnapshotDTO - a model defined in Swagger
        """

        self._uptime = None
        self._time_zone = None
        self._active_timer_driven_threads = None
        self._active_event_driven_threads = None
        self._bundles_loaded = None

        if uptime is not None:
          self.uptime = uptime
        if time_zone is not None:
          self.time_zone = time_zone
        if active_timer_driven_threads is not None:
          self.active_timer_driven_threads = active_timer_driven_threads
        if active_event_driven_threads is not None:
          self.active_event_driven_threads = active_event_driven_threads
        if bundles_loaded is not None:
          self.bundles_loaded = bundles_loaded

    @property
    def uptime(self):
        """
        Gets the uptime of this JVMFlowDiagnosticsSnapshotDTO.
        How long this node has been running, formatted as hours:minutes:seconds.milliseconds

        :return: The uptime of this JVMFlowDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._uptime

    @uptime.setter
    def uptime(self, uptime):
        """
        Sets the uptime of this JVMFlowDiagnosticsSnapshotDTO.
        How long this node has been running, formatted as hours:minutes:seconds.milliseconds

        :param uptime: The uptime of this JVMFlowDiagnosticsSnapshotDTO.
        :type: str
        """

        self._uptime = uptime

    @property
    def time_zone(self):
        """
        Gets the time_zone of this JVMFlowDiagnosticsSnapshotDTO.
        The name of the Time Zone that is configured, if available

        :return: The time_zone of this JVMFlowDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._time_zone

    @time_zone.setter
    def time_zone(self, time_zone):
        """
        Sets the time_zone of this JVMFlowDiagnosticsSnapshotDTO.
        The name of the Time Zone that is configured, if available

        :param time_zone: The time_zone of this JVMFlowDiagnosticsSnapshotDTO.
        :type: str
        """

        self._time_zone = time_zone

    @property
    def active_timer_driven_threads(self):
        """
        Gets the active_timer_driven_threads of this JVMFlowDiagnosticsSnapshotDTO.
        The number of timer-driven threads that are active

        :return: The active_timer_driven_threads of this JVMFlowDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._active_timer_driven_threads

    @active_timer_driven_threads.setter
    def active_timer_driven_threads(self, active_timer_driven_threads):
        """
        Sets the active_timer_driven_threads of this JVMFlowDiagnosticsSnapshotDTO.
        The number of timer-driven threads that are active

        :param active_timer_driven_threads: The active_timer_driven_threads of this JVMFlowDiagnosticsSnapshotDTO.
        :type: int
        """

        self._active_timer_driven_threads = active_timer_driven_threads

    @property
    def active_event_driven_threads(self):
        """
        Gets the active_event_driven_threads of this JVMFlowDiagnosticsSnapshotDTO.
        The number of event-driven threads that are active

        :return: The active_event_driven_threads of this JVMFlowDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._active_event_driven_threads

    @active_event_driven_threads.setter
    def active_event_driven_threads(self, active_event_driven_threads):
        """
        Sets the active_event_driven_threads of this JVMFlowDiagnosticsSnapshotDTO.
        The number of event-driven threads that are active

        :param active_event_driven_threads: The active_event_driven_threads of this JVMFlowDiagnosticsSnapshotDTO.
        :type: int
        """

        self._active_event_driven_threads = active_event_driven_threads

    @property
    def bundles_loaded(self):
        """
        Gets the bundles_loaded of this JVMFlowDiagnosticsSnapshotDTO.
        The NiFi Bundles (NARs) that are loaded by NiFi

        :return: The bundles_loaded of this JVMFlowDiagnosticsSnapshotDTO.
        :rtype: list[BundleDTO]
        """
        return self._bundles_loaded

    @bundles_loaded.setter
    def bundles_loaded(self, bundles_loaded):
        """
        Sets the bundles_loaded of this JVMFlowDiagnosticsSnapshotDTO.
        The NiFi Bundles (NARs) that are loaded by NiFi

        :param bundles_loaded: The bundles_loaded of this JVMFlowDiagnosticsSnapshotDTO.
        :type: list[BundleDTO]
        """

        self._bundles_loaded = bundles_loaded

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
        if not isinstance(other, JVMFlowDiagnosticsSnapshotDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
