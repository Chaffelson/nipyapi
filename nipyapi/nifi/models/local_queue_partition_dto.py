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


class LocalQueuePartitionDTO(object):
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
        'active_queue_flow_file_count': 'int',
        'active_queue_byte_count': 'int',
        'swap_flow_file_count': 'int',
        'swap_byte_count': 'int',
        'swap_files': 'int',
        'in_flight_flow_file_count': 'int',
        'in_flight_byte_count': 'int',
        'all_active_queue_flow_files_penalized': 'bool',
        'any_active_queue_flow_files_penalized': 'bool'
    }

    attribute_map = {
        'total_flow_file_count': 'totalFlowFileCount',
        'total_byte_count': 'totalByteCount',
        'active_queue_flow_file_count': 'activeQueueFlowFileCount',
        'active_queue_byte_count': 'activeQueueByteCount',
        'swap_flow_file_count': 'swapFlowFileCount',
        'swap_byte_count': 'swapByteCount',
        'swap_files': 'swapFiles',
        'in_flight_flow_file_count': 'inFlightFlowFileCount',
        'in_flight_byte_count': 'inFlightByteCount',
        'all_active_queue_flow_files_penalized': 'allActiveQueueFlowFilesPenalized',
        'any_active_queue_flow_files_penalized': 'anyActiveQueueFlowFilesPenalized'
    }

    def __init__(self, total_flow_file_count=None, total_byte_count=None, active_queue_flow_file_count=None, active_queue_byte_count=None, swap_flow_file_count=None, swap_byte_count=None, swap_files=None, in_flight_flow_file_count=None, in_flight_byte_count=None, all_active_queue_flow_files_penalized=None, any_active_queue_flow_files_penalized=None):
        """
        LocalQueuePartitionDTO - a model defined in Swagger
        """

        self._total_flow_file_count = None
        self._total_byte_count = None
        self._active_queue_flow_file_count = None
        self._active_queue_byte_count = None
        self._swap_flow_file_count = None
        self._swap_byte_count = None
        self._swap_files = None
        self._in_flight_flow_file_count = None
        self._in_flight_byte_count = None
        self._all_active_queue_flow_files_penalized = None
        self._any_active_queue_flow_files_penalized = None

        if total_flow_file_count is not None:
          self.total_flow_file_count = total_flow_file_count
        if total_byte_count is not None:
          self.total_byte_count = total_byte_count
        if active_queue_flow_file_count is not None:
          self.active_queue_flow_file_count = active_queue_flow_file_count
        if active_queue_byte_count is not None:
          self.active_queue_byte_count = active_queue_byte_count
        if swap_flow_file_count is not None:
          self.swap_flow_file_count = swap_flow_file_count
        if swap_byte_count is not None:
          self.swap_byte_count = swap_byte_count
        if swap_files is not None:
          self.swap_files = swap_files
        if in_flight_flow_file_count is not None:
          self.in_flight_flow_file_count = in_flight_flow_file_count
        if in_flight_byte_count is not None:
          self.in_flight_byte_count = in_flight_byte_count
        if all_active_queue_flow_files_penalized is not None:
          self.all_active_queue_flow_files_penalized = all_active_queue_flow_files_penalized
        if any_active_queue_flow_files_penalized is not None:
          self.any_active_queue_flow_files_penalized = any_active_queue_flow_files_penalized

    @property
    def total_flow_file_count(self):
        """
        Gets the total_flow_file_count of this LocalQueuePartitionDTO.
        Total number of FlowFiles owned by the Connection

        :return: The total_flow_file_count of this LocalQueuePartitionDTO.
        :rtype: int
        """
        return self._total_flow_file_count

    @total_flow_file_count.setter
    def total_flow_file_count(self, total_flow_file_count):
        """
        Sets the total_flow_file_count of this LocalQueuePartitionDTO.
        Total number of FlowFiles owned by the Connection

        :param total_flow_file_count: The total_flow_file_count of this LocalQueuePartitionDTO.
        :type: int
        """

        self._total_flow_file_count = total_flow_file_count

    @property
    def total_byte_count(self):
        """
        Gets the total_byte_count of this LocalQueuePartitionDTO.
        Total number of bytes that make up the content for the FlowFiles owned by this Connection

        :return: The total_byte_count of this LocalQueuePartitionDTO.
        :rtype: int
        """
        return self._total_byte_count

    @total_byte_count.setter
    def total_byte_count(self, total_byte_count):
        """
        Sets the total_byte_count of this LocalQueuePartitionDTO.
        Total number of bytes that make up the content for the FlowFiles owned by this Connection

        :param total_byte_count: The total_byte_count of this LocalQueuePartitionDTO.
        :type: int
        """

        self._total_byte_count = total_byte_count

    @property
    def active_queue_flow_file_count(self):
        """
        Gets the active_queue_flow_file_count of this LocalQueuePartitionDTO.
        Total number of FlowFiles that exist in the Connection's Active Queue, immediately available to be offered up to a component

        :return: The active_queue_flow_file_count of this LocalQueuePartitionDTO.
        :rtype: int
        """
        return self._active_queue_flow_file_count

    @active_queue_flow_file_count.setter
    def active_queue_flow_file_count(self, active_queue_flow_file_count):
        """
        Sets the active_queue_flow_file_count of this LocalQueuePartitionDTO.
        Total number of FlowFiles that exist in the Connection's Active Queue, immediately available to be offered up to a component

        :param active_queue_flow_file_count: The active_queue_flow_file_count of this LocalQueuePartitionDTO.
        :type: int
        """

        self._active_queue_flow_file_count = active_queue_flow_file_count

    @property
    def active_queue_byte_count(self):
        """
        Gets the active_queue_byte_count of this LocalQueuePartitionDTO.
        Total number of bytes that make up the content for the FlowFiles that are present in the Connection's Active Queue

        :return: The active_queue_byte_count of this LocalQueuePartitionDTO.
        :rtype: int
        """
        return self._active_queue_byte_count

    @active_queue_byte_count.setter
    def active_queue_byte_count(self, active_queue_byte_count):
        """
        Sets the active_queue_byte_count of this LocalQueuePartitionDTO.
        Total number of bytes that make up the content for the FlowFiles that are present in the Connection's Active Queue

        :param active_queue_byte_count: The active_queue_byte_count of this LocalQueuePartitionDTO.
        :type: int
        """

        self._active_queue_byte_count = active_queue_byte_count

    @property
    def swap_flow_file_count(self):
        """
        Gets the swap_flow_file_count of this LocalQueuePartitionDTO.
        The total number of FlowFiles that are swapped out for this Connection

        :return: The swap_flow_file_count of this LocalQueuePartitionDTO.
        :rtype: int
        """
        return self._swap_flow_file_count

    @swap_flow_file_count.setter
    def swap_flow_file_count(self, swap_flow_file_count):
        """
        Sets the swap_flow_file_count of this LocalQueuePartitionDTO.
        The total number of FlowFiles that are swapped out for this Connection

        :param swap_flow_file_count: The swap_flow_file_count of this LocalQueuePartitionDTO.
        :type: int
        """

        self._swap_flow_file_count = swap_flow_file_count

    @property
    def swap_byte_count(self):
        """
        Gets the swap_byte_count of this LocalQueuePartitionDTO.
        Total number of bytes that make up the content for the FlowFiles that are swapped out to disk for the Connection

        :return: The swap_byte_count of this LocalQueuePartitionDTO.
        :rtype: int
        """
        return self._swap_byte_count

    @swap_byte_count.setter
    def swap_byte_count(self, swap_byte_count):
        """
        Sets the swap_byte_count of this LocalQueuePartitionDTO.
        Total number of bytes that make up the content for the FlowFiles that are swapped out to disk for the Connection

        :param swap_byte_count: The swap_byte_count of this LocalQueuePartitionDTO.
        :type: int
        """

        self._swap_byte_count = swap_byte_count

    @property
    def swap_files(self):
        """
        Gets the swap_files of this LocalQueuePartitionDTO.
        The number of Swap Files that exist for this Connection

        :return: The swap_files of this LocalQueuePartitionDTO.
        :rtype: int
        """
        return self._swap_files

    @swap_files.setter
    def swap_files(self, swap_files):
        """
        Sets the swap_files of this LocalQueuePartitionDTO.
        The number of Swap Files that exist for this Connection

        :param swap_files: The swap_files of this LocalQueuePartitionDTO.
        :type: int
        """

        self._swap_files = swap_files

    @property
    def in_flight_flow_file_count(self):
        """
        Gets the in_flight_flow_file_count of this LocalQueuePartitionDTO.
        The number of In-Flight FlowFiles for this Connection. These are FlowFiles that belong to the connection but are currently being operated on by a Processor, Port, etc.

        :return: The in_flight_flow_file_count of this LocalQueuePartitionDTO.
        :rtype: int
        """
        return self._in_flight_flow_file_count

    @in_flight_flow_file_count.setter
    def in_flight_flow_file_count(self, in_flight_flow_file_count):
        """
        Sets the in_flight_flow_file_count of this LocalQueuePartitionDTO.
        The number of In-Flight FlowFiles for this Connection. These are FlowFiles that belong to the connection but are currently being operated on by a Processor, Port, etc.

        :param in_flight_flow_file_count: The in_flight_flow_file_count of this LocalQueuePartitionDTO.
        :type: int
        """

        self._in_flight_flow_file_count = in_flight_flow_file_count

    @property
    def in_flight_byte_count(self):
        """
        Gets the in_flight_byte_count of this LocalQueuePartitionDTO.
        The number bytes that make up the content of the FlowFiles that are In-Flight

        :return: The in_flight_byte_count of this LocalQueuePartitionDTO.
        :rtype: int
        """
        return self._in_flight_byte_count

    @in_flight_byte_count.setter
    def in_flight_byte_count(self, in_flight_byte_count):
        """
        Sets the in_flight_byte_count of this LocalQueuePartitionDTO.
        The number bytes that make up the content of the FlowFiles that are In-Flight

        :param in_flight_byte_count: The in_flight_byte_count of this LocalQueuePartitionDTO.
        :type: int
        """

        self._in_flight_byte_count = in_flight_byte_count

    @property
    def all_active_queue_flow_files_penalized(self):
        """
        Gets the all_active_queue_flow_files_penalized of this LocalQueuePartitionDTO.
        Whether or not all of the FlowFiles in the Active Queue are penalized

        :return: The all_active_queue_flow_files_penalized of this LocalQueuePartitionDTO.
        :rtype: bool
        """
        return self._all_active_queue_flow_files_penalized

    @all_active_queue_flow_files_penalized.setter
    def all_active_queue_flow_files_penalized(self, all_active_queue_flow_files_penalized):
        """
        Sets the all_active_queue_flow_files_penalized of this LocalQueuePartitionDTO.
        Whether or not all of the FlowFiles in the Active Queue are penalized

        :param all_active_queue_flow_files_penalized: The all_active_queue_flow_files_penalized of this LocalQueuePartitionDTO.
        :type: bool
        """

        self._all_active_queue_flow_files_penalized = all_active_queue_flow_files_penalized

    @property
    def any_active_queue_flow_files_penalized(self):
        """
        Gets the any_active_queue_flow_files_penalized of this LocalQueuePartitionDTO.
        Whether or not any of the FlowFiles in the Active Queue are penalized

        :return: The any_active_queue_flow_files_penalized of this LocalQueuePartitionDTO.
        :rtype: bool
        """
        return self._any_active_queue_flow_files_penalized

    @any_active_queue_flow_files_penalized.setter
    def any_active_queue_flow_files_penalized(self, any_active_queue_flow_files_penalized):
        """
        Sets the any_active_queue_flow_files_penalized of this LocalQueuePartitionDTO.
        Whether or not any of the FlowFiles in the Active Queue are penalized

        :param any_active_queue_flow_files_penalized: The any_active_queue_flow_files_penalized of this LocalQueuePartitionDTO.
        :type: bool
        """

        self._any_active_queue_flow_files_penalized = any_active_queue_flow_files_penalized

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
        if not isinstance(other, LocalQueuePartitionDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
