# coding: utf-8

"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.17.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class SystemDiagnosticsSnapshotDTO(object):
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
        'total_non_heap': 'str',
        'total_non_heap_bytes': 'int',
        'used_non_heap': 'str',
        'used_non_heap_bytes': 'int',
        'free_non_heap': 'str',
        'free_non_heap_bytes': 'int',
        'max_non_heap': 'str',
        'max_non_heap_bytes': 'int',
        'non_heap_utilization': 'str',
        'total_heap': 'str',
        'total_heap_bytes': 'int',
        'used_heap': 'str',
        'used_heap_bytes': 'int',
        'free_heap': 'str',
        'free_heap_bytes': 'int',
        'max_heap': 'str',
        'max_heap_bytes': 'int',
        'heap_utilization': 'str',
        'available_processors': 'int',
        'processor_load_average': 'float',
        'total_threads': 'int',
        'daemon_threads': 'int',
        'uptime': 'str',
        'flow_file_repository_storage_usage': 'StorageUsageDTO',
        'content_repository_storage_usage': 'list[StorageUsageDTO]',
        'provenance_repository_storage_usage': 'list[StorageUsageDTO]',
        'garbage_collection': 'list[GarbageCollectionDTO]',
        'stats_last_refreshed': 'str',
        'version_info': 'VersionInfoDTO'
    }

    attribute_map = {
        'total_non_heap': 'totalNonHeap',
        'total_non_heap_bytes': 'totalNonHeapBytes',
        'used_non_heap': 'usedNonHeap',
        'used_non_heap_bytes': 'usedNonHeapBytes',
        'free_non_heap': 'freeNonHeap',
        'free_non_heap_bytes': 'freeNonHeapBytes',
        'max_non_heap': 'maxNonHeap',
        'max_non_heap_bytes': 'maxNonHeapBytes',
        'non_heap_utilization': 'nonHeapUtilization',
        'total_heap': 'totalHeap',
        'total_heap_bytes': 'totalHeapBytes',
        'used_heap': 'usedHeap',
        'used_heap_bytes': 'usedHeapBytes',
        'free_heap': 'freeHeap',
        'free_heap_bytes': 'freeHeapBytes',
        'max_heap': 'maxHeap',
        'max_heap_bytes': 'maxHeapBytes',
        'heap_utilization': 'heapUtilization',
        'available_processors': 'availableProcessors',
        'processor_load_average': 'processorLoadAverage',
        'total_threads': 'totalThreads',
        'daemon_threads': 'daemonThreads',
        'uptime': 'uptime',
        'flow_file_repository_storage_usage': 'flowFileRepositoryStorageUsage',
        'content_repository_storage_usage': 'contentRepositoryStorageUsage',
        'provenance_repository_storage_usage': 'provenanceRepositoryStorageUsage',
        'garbage_collection': 'garbageCollection',
        'stats_last_refreshed': 'statsLastRefreshed',
        'version_info': 'versionInfo'
    }

    def __init__(self, total_non_heap=None, total_non_heap_bytes=None, used_non_heap=None, used_non_heap_bytes=None, free_non_heap=None, free_non_heap_bytes=None, max_non_heap=None, max_non_heap_bytes=None, non_heap_utilization=None, total_heap=None, total_heap_bytes=None, used_heap=None, used_heap_bytes=None, free_heap=None, free_heap_bytes=None, max_heap=None, max_heap_bytes=None, heap_utilization=None, available_processors=None, processor_load_average=None, total_threads=None, daemon_threads=None, uptime=None, flow_file_repository_storage_usage=None, content_repository_storage_usage=None, provenance_repository_storage_usage=None, garbage_collection=None, stats_last_refreshed=None, version_info=None):
        """
        SystemDiagnosticsSnapshotDTO - a model defined in Swagger
        """

        self._total_non_heap = None
        self._total_non_heap_bytes = None
        self._used_non_heap = None
        self._used_non_heap_bytes = None
        self._free_non_heap = None
        self._free_non_heap_bytes = None
        self._max_non_heap = None
        self._max_non_heap_bytes = None
        self._non_heap_utilization = None
        self._total_heap = None
        self._total_heap_bytes = None
        self._used_heap = None
        self._used_heap_bytes = None
        self._free_heap = None
        self._free_heap_bytes = None
        self._max_heap = None
        self._max_heap_bytes = None
        self._heap_utilization = None
        self._available_processors = None
        self._processor_load_average = None
        self._total_threads = None
        self._daemon_threads = None
        self._uptime = None
        self._flow_file_repository_storage_usage = None
        self._content_repository_storage_usage = None
        self._provenance_repository_storage_usage = None
        self._garbage_collection = None
        self._stats_last_refreshed = None
        self._version_info = None

        if total_non_heap is not None:
          self.total_non_heap = total_non_heap
        if total_non_heap_bytes is not None:
          self.total_non_heap_bytes = total_non_heap_bytes
        if used_non_heap is not None:
          self.used_non_heap = used_non_heap
        if used_non_heap_bytes is not None:
          self.used_non_heap_bytes = used_non_heap_bytes
        if free_non_heap is not None:
          self.free_non_heap = free_non_heap
        if free_non_heap_bytes is not None:
          self.free_non_heap_bytes = free_non_heap_bytes
        if max_non_heap is not None:
          self.max_non_heap = max_non_heap
        if max_non_heap_bytes is not None:
          self.max_non_heap_bytes = max_non_heap_bytes
        if non_heap_utilization is not None:
          self.non_heap_utilization = non_heap_utilization
        if total_heap is not None:
          self.total_heap = total_heap
        if total_heap_bytes is not None:
          self.total_heap_bytes = total_heap_bytes
        if used_heap is not None:
          self.used_heap = used_heap
        if used_heap_bytes is not None:
          self.used_heap_bytes = used_heap_bytes
        if free_heap is not None:
          self.free_heap = free_heap
        if free_heap_bytes is not None:
          self.free_heap_bytes = free_heap_bytes
        if max_heap is not None:
          self.max_heap = max_heap
        if max_heap_bytes is not None:
          self.max_heap_bytes = max_heap_bytes
        if heap_utilization is not None:
          self.heap_utilization = heap_utilization
        if available_processors is not None:
          self.available_processors = available_processors
        if processor_load_average is not None:
          self.processor_load_average = processor_load_average
        if total_threads is not None:
          self.total_threads = total_threads
        if daemon_threads is not None:
          self.daemon_threads = daemon_threads
        if uptime is not None:
          self.uptime = uptime
        if flow_file_repository_storage_usage is not None:
          self.flow_file_repository_storage_usage = flow_file_repository_storage_usage
        if content_repository_storage_usage is not None:
          self.content_repository_storage_usage = content_repository_storage_usage
        if provenance_repository_storage_usage is not None:
          self.provenance_repository_storage_usage = provenance_repository_storage_usage
        if garbage_collection is not None:
          self.garbage_collection = garbage_collection
        if stats_last_refreshed is not None:
          self.stats_last_refreshed = stats_last_refreshed
        if version_info is not None:
          self.version_info = version_info

    @property
    def total_non_heap(self):
        """
        Gets the total_non_heap of this SystemDiagnosticsSnapshotDTO.
        Total size of non heap.

        :return: The total_non_heap of this SystemDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._total_non_heap

    @total_non_heap.setter
    def total_non_heap(self, total_non_heap):
        """
        Sets the total_non_heap of this SystemDiagnosticsSnapshotDTO.
        Total size of non heap.

        :param total_non_heap: The total_non_heap of this SystemDiagnosticsSnapshotDTO.
        :type: str
        """

        self._total_non_heap = total_non_heap

    @property
    def total_non_heap_bytes(self):
        """
        Gets the total_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        Total number of bytes allocated to the JVM not used for heap

        :return: The total_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._total_non_heap_bytes

    @total_non_heap_bytes.setter
    def total_non_heap_bytes(self, total_non_heap_bytes):
        """
        Sets the total_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        Total number of bytes allocated to the JVM not used for heap

        :param total_non_heap_bytes: The total_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._total_non_heap_bytes = total_non_heap_bytes

    @property
    def used_non_heap(self):
        """
        Gets the used_non_heap of this SystemDiagnosticsSnapshotDTO.
        Amount of use non heap.

        :return: The used_non_heap of this SystemDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._used_non_heap

    @used_non_heap.setter
    def used_non_heap(self, used_non_heap):
        """
        Sets the used_non_heap of this SystemDiagnosticsSnapshotDTO.
        Amount of use non heap.

        :param used_non_heap: The used_non_heap of this SystemDiagnosticsSnapshotDTO.
        :type: str
        """

        self._used_non_heap = used_non_heap

    @property
    def used_non_heap_bytes(self):
        """
        Gets the used_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        Total number of bytes used by the JVM not in the heap space

        :return: The used_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._used_non_heap_bytes

    @used_non_heap_bytes.setter
    def used_non_heap_bytes(self, used_non_heap_bytes):
        """
        Sets the used_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        Total number of bytes used by the JVM not in the heap space

        :param used_non_heap_bytes: The used_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._used_non_heap_bytes = used_non_heap_bytes

    @property
    def free_non_heap(self):
        """
        Gets the free_non_heap of this SystemDiagnosticsSnapshotDTO.
        Amount of free non heap.

        :return: The free_non_heap of this SystemDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._free_non_heap

    @free_non_heap.setter
    def free_non_heap(self, free_non_heap):
        """
        Sets the free_non_heap of this SystemDiagnosticsSnapshotDTO.
        Amount of free non heap.

        :param free_non_heap: The free_non_heap of this SystemDiagnosticsSnapshotDTO.
        :type: str
        """

        self._free_non_heap = free_non_heap

    @property
    def free_non_heap_bytes(self):
        """
        Gets the free_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        Total number of free non-heap bytes available to the JVM

        :return: The free_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._free_non_heap_bytes

    @free_non_heap_bytes.setter
    def free_non_heap_bytes(self, free_non_heap_bytes):
        """
        Sets the free_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        Total number of free non-heap bytes available to the JVM

        :param free_non_heap_bytes: The free_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._free_non_heap_bytes = free_non_heap_bytes

    @property
    def max_non_heap(self):
        """
        Gets the max_non_heap of this SystemDiagnosticsSnapshotDTO.
        Maximum size of non heap.

        :return: The max_non_heap of this SystemDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._max_non_heap

    @max_non_heap.setter
    def max_non_heap(self, max_non_heap):
        """
        Sets the max_non_heap of this SystemDiagnosticsSnapshotDTO.
        Maximum size of non heap.

        :param max_non_heap: The max_non_heap of this SystemDiagnosticsSnapshotDTO.
        :type: str
        """

        self._max_non_heap = max_non_heap

    @property
    def max_non_heap_bytes(self):
        """
        Gets the max_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        The maximum number of bytes that the JVM can use for non-heap purposes

        :return: The max_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._max_non_heap_bytes

    @max_non_heap_bytes.setter
    def max_non_heap_bytes(self, max_non_heap_bytes):
        """
        Sets the max_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        The maximum number of bytes that the JVM can use for non-heap purposes

        :param max_non_heap_bytes: The max_non_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._max_non_heap_bytes = max_non_heap_bytes

    @property
    def non_heap_utilization(self):
        """
        Gets the non_heap_utilization of this SystemDiagnosticsSnapshotDTO.
        Utilization of non heap.

        :return: The non_heap_utilization of this SystemDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._non_heap_utilization

    @non_heap_utilization.setter
    def non_heap_utilization(self, non_heap_utilization):
        """
        Sets the non_heap_utilization of this SystemDiagnosticsSnapshotDTO.
        Utilization of non heap.

        :param non_heap_utilization: The non_heap_utilization of this SystemDiagnosticsSnapshotDTO.
        :type: str
        """

        self._non_heap_utilization = non_heap_utilization

    @property
    def total_heap(self):
        """
        Gets the total_heap of this SystemDiagnosticsSnapshotDTO.
        Total size of heap.

        :return: The total_heap of this SystemDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._total_heap

    @total_heap.setter
    def total_heap(self, total_heap):
        """
        Sets the total_heap of this SystemDiagnosticsSnapshotDTO.
        Total size of heap.

        :param total_heap: The total_heap of this SystemDiagnosticsSnapshotDTO.
        :type: str
        """

        self._total_heap = total_heap

    @property
    def total_heap_bytes(self):
        """
        Gets the total_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        The total number of bytes that are available for the JVM heap to use

        :return: The total_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._total_heap_bytes

    @total_heap_bytes.setter
    def total_heap_bytes(self, total_heap_bytes):
        """
        Sets the total_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        The total number of bytes that are available for the JVM heap to use

        :param total_heap_bytes: The total_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._total_heap_bytes = total_heap_bytes

    @property
    def used_heap(self):
        """
        Gets the used_heap of this SystemDiagnosticsSnapshotDTO.
        Amount of used heap.

        :return: The used_heap of this SystemDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._used_heap

    @used_heap.setter
    def used_heap(self, used_heap):
        """
        Sets the used_heap of this SystemDiagnosticsSnapshotDTO.
        Amount of used heap.

        :param used_heap: The used_heap of this SystemDiagnosticsSnapshotDTO.
        :type: str
        """

        self._used_heap = used_heap

    @property
    def used_heap_bytes(self):
        """
        Gets the used_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        The number of bytes of JVM heap that are currently being used

        :return: The used_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._used_heap_bytes

    @used_heap_bytes.setter
    def used_heap_bytes(self, used_heap_bytes):
        """
        Sets the used_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        The number of bytes of JVM heap that are currently being used

        :param used_heap_bytes: The used_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._used_heap_bytes = used_heap_bytes

    @property
    def free_heap(self):
        """
        Gets the free_heap of this SystemDiagnosticsSnapshotDTO.
        Amount of free heap.

        :return: The free_heap of this SystemDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._free_heap

    @free_heap.setter
    def free_heap(self, free_heap):
        """
        Sets the free_heap of this SystemDiagnosticsSnapshotDTO.
        Amount of free heap.

        :param free_heap: The free_heap of this SystemDiagnosticsSnapshotDTO.
        :type: str
        """

        self._free_heap = free_heap

    @property
    def free_heap_bytes(self):
        """
        Gets the free_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        The number of bytes that are allocated to the JVM heap but not currently being used

        :return: The free_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._free_heap_bytes

    @free_heap_bytes.setter
    def free_heap_bytes(self, free_heap_bytes):
        """
        Sets the free_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        The number of bytes that are allocated to the JVM heap but not currently being used

        :param free_heap_bytes: The free_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._free_heap_bytes = free_heap_bytes

    @property
    def max_heap(self):
        """
        Gets the max_heap of this SystemDiagnosticsSnapshotDTO.
        Maximum size of heap.

        :return: The max_heap of this SystemDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._max_heap

    @max_heap.setter
    def max_heap(self, max_heap):
        """
        Sets the max_heap of this SystemDiagnosticsSnapshotDTO.
        Maximum size of heap.

        :param max_heap: The max_heap of this SystemDiagnosticsSnapshotDTO.
        :type: str
        """

        self._max_heap = max_heap

    @property
    def max_heap_bytes(self):
        """
        Gets the max_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        The maximum number of bytes that can be used by the JVM

        :return: The max_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._max_heap_bytes

    @max_heap_bytes.setter
    def max_heap_bytes(self, max_heap_bytes):
        """
        Sets the max_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        The maximum number of bytes that can be used by the JVM

        :param max_heap_bytes: The max_heap_bytes of this SystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._max_heap_bytes = max_heap_bytes

    @property
    def heap_utilization(self):
        """
        Gets the heap_utilization of this SystemDiagnosticsSnapshotDTO.
        Utilization of heap.

        :return: The heap_utilization of this SystemDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._heap_utilization

    @heap_utilization.setter
    def heap_utilization(self, heap_utilization):
        """
        Sets the heap_utilization of this SystemDiagnosticsSnapshotDTO.
        Utilization of heap.

        :param heap_utilization: The heap_utilization of this SystemDiagnosticsSnapshotDTO.
        :type: str
        """

        self._heap_utilization = heap_utilization

    @property
    def available_processors(self):
        """
        Gets the available_processors of this SystemDiagnosticsSnapshotDTO.
        Number of available processors if supported by the underlying system.

        :return: The available_processors of this SystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._available_processors

    @available_processors.setter
    def available_processors(self, available_processors):
        """
        Sets the available_processors of this SystemDiagnosticsSnapshotDTO.
        Number of available processors if supported by the underlying system.

        :param available_processors: The available_processors of this SystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._available_processors = available_processors

    @property
    def processor_load_average(self):
        """
        Gets the processor_load_average of this SystemDiagnosticsSnapshotDTO.
        The processor load average if supported by the underlying system.

        :return: The processor_load_average of this SystemDiagnosticsSnapshotDTO.
        :rtype: float
        """
        return self._processor_load_average

    @processor_load_average.setter
    def processor_load_average(self, processor_load_average):
        """
        Sets the processor_load_average of this SystemDiagnosticsSnapshotDTO.
        The processor load average if supported by the underlying system.

        :param processor_load_average: The processor_load_average of this SystemDiagnosticsSnapshotDTO.
        :type: float
        """

        self._processor_load_average = processor_load_average

    @property
    def total_threads(self):
        """
        Gets the total_threads of this SystemDiagnosticsSnapshotDTO.
        Total number of threads.

        :return: The total_threads of this SystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._total_threads

    @total_threads.setter
    def total_threads(self, total_threads):
        """
        Sets the total_threads of this SystemDiagnosticsSnapshotDTO.
        Total number of threads.

        :param total_threads: The total_threads of this SystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._total_threads = total_threads

    @property
    def daemon_threads(self):
        """
        Gets the daemon_threads of this SystemDiagnosticsSnapshotDTO.
        Number of daemon threads.

        :return: The daemon_threads of this SystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._daemon_threads

    @daemon_threads.setter
    def daemon_threads(self, daemon_threads):
        """
        Sets the daemon_threads of this SystemDiagnosticsSnapshotDTO.
        Number of daemon threads.

        :param daemon_threads: The daemon_threads of this SystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._daemon_threads = daemon_threads

    @property
    def uptime(self):
        """
        Gets the uptime of this SystemDiagnosticsSnapshotDTO.
        The uptime of the Java virtual machine

        :return: The uptime of this SystemDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._uptime

    @uptime.setter
    def uptime(self, uptime):
        """
        Sets the uptime of this SystemDiagnosticsSnapshotDTO.
        The uptime of the Java virtual machine

        :param uptime: The uptime of this SystemDiagnosticsSnapshotDTO.
        :type: str
        """

        self._uptime = uptime

    @property
    def flow_file_repository_storage_usage(self):
        """
        Gets the flow_file_repository_storage_usage of this SystemDiagnosticsSnapshotDTO.
        The flowfile repository storage usage.

        :return: The flow_file_repository_storage_usage of this SystemDiagnosticsSnapshotDTO.
        :rtype: StorageUsageDTO
        """
        return self._flow_file_repository_storage_usage

    @flow_file_repository_storage_usage.setter
    def flow_file_repository_storage_usage(self, flow_file_repository_storage_usage):
        """
        Sets the flow_file_repository_storage_usage of this SystemDiagnosticsSnapshotDTO.
        The flowfile repository storage usage.

        :param flow_file_repository_storage_usage: The flow_file_repository_storage_usage of this SystemDiagnosticsSnapshotDTO.
        :type: StorageUsageDTO
        """

        self._flow_file_repository_storage_usage = flow_file_repository_storage_usage

    @property
    def content_repository_storage_usage(self):
        """
        Gets the content_repository_storage_usage of this SystemDiagnosticsSnapshotDTO.
        The content repository storage usage.

        :return: The content_repository_storage_usage of this SystemDiagnosticsSnapshotDTO.
        :rtype: list[StorageUsageDTO]
        """
        return self._content_repository_storage_usage

    @content_repository_storage_usage.setter
    def content_repository_storage_usage(self, content_repository_storage_usage):
        """
        Sets the content_repository_storage_usage of this SystemDiagnosticsSnapshotDTO.
        The content repository storage usage.

        :param content_repository_storage_usage: The content_repository_storage_usage of this SystemDiagnosticsSnapshotDTO.
        :type: list[StorageUsageDTO]
        """

        self._content_repository_storage_usage = content_repository_storage_usage

    @property
    def provenance_repository_storage_usage(self):
        """
        Gets the provenance_repository_storage_usage of this SystemDiagnosticsSnapshotDTO.
        The provenance repository storage usage.

        :return: The provenance_repository_storage_usage of this SystemDiagnosticsSnapshotDTO.
        :rtype: list[StorageUsageDTO]
        """
        return self._provenance_repository_storage_usage

    @provenance_repository_storage_usage.setter
    def provenance_repository_storage_usage(self, provenance_repository_storage_usage):
        """
        Sets the provenance_repository_storage_usage of this SystemDiagnosticsSnapshotDTO.
        The provenance repository storage usage.

        :param provenance_repository_storage_usage: The provenance_repository_storage_usage of this SystemDiagnosticsSnapshotDTO.
        :type: list[StorageUsageDTO]
        """

        self._provenance_repository_storage_usage = provenance_repository_storage_usage

    @property
    def garbage_collection(self):
        """
        Gets the garbage_collection of this SystemDiagnosticsSnapshotDTO.
        The garbage collection details.

        :return: The garbage_collection of this SystemDiagnosticsSnapshotDTO.
        :rtype: list[GarbageCollectionDTO]
        """
        return self._garbage_collection

    @garbage_collection.setter
    def garbage_collection(self, garbage_collection):
        """
        Sets the garbage_collection of this SystemDiagnosticsSnapshotDTO.
        The garbage collection details.

        :param garbage_collection: The garbage_collection of this SystemDiagnosticsSnapshotDTO.
        :type: list[GarbageCollectionDTO]
        """

        self._garbage_collection = garbage_collection

    @property
    def stats_last_refreshed(self):
        """
        Gets the stats_last_refreshed of this SystemDiagnosticsSnapshotDTO.
        When the diagnostics were generated.

        :return: The stats_last_refreshed of this SystemDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._stats_last_refreshed

    @stats_last_refreshed.setter
    def stats_last_refreshed(self, stats_last_refreshed):
        """
        Sets the stats_last_refreshed of this SystemDiagnosticsSnapshotDTO.
        When the diagnostics were generated.

        :param stats_last_refreshed: The stats_last_refreshed of this SystemDiagnosticsSnapshotDTO.
        :type: str
        """

        self._stats_last_refreshed = stats_last_refreshed

    @property
    def version_info(self):
        """
        Gets the version_info of this SystemDiagnosticsSnapshotDTO.
        The nifi, os, java, and build version information

        :return: The version_info of this SystemDiagnosticsSnapshotDTO.
        :rtype: VersionInfoDTO
        """
        return self._version_info

    @version_info.setter
    def version_info(self, version_info):
        """
        Sets the version_info of this SystemDiagnosticsSnapshotDTO.
        The nifi, os, java, and build version information

        :param version_info: The version_info of this SystemDiagnosticsSnapshotDTO.
        :type: VersionInfoDTO
        """

        self._version_info = version_info

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
        if not isinstance(other, SystemDiagnosticsSnapshotDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
