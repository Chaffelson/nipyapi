"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class JVMSystemDiagnosticsSnapshotDTO(object):
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
        'flow_file_repository_storage_usage': 'RepositoryUsageDTO',
        'content_repository_storage_usage': 'list[RepositoryUsageDTO]',
        'provenance_repository_storage_usage': 'list[RepositoryUsageDTO]',
        'max_heap_bytes': 'int',
        'max_heap': 'str',
        'garbage_collection_diagnostics': 'list[GarbageCollectionDiagnosticsDTO]',
        'cpu_cores': 'int',
        'cpu_load_average': 'float',
        'physical_memory_bytes': 'int',
        'physical_memory': 'str',
        'open_file_descriptors': 'int',
        'max_open_file_descriptors': 'int'
    }

    attribute_map = {
        'flow_file_repository_storage_usage': 'flowFileRepositoryStorageUsage',
        'content_repository_storage_usage': 'contentRepositoryStorageUsage',
        'provenance_repository_storage_usage': 'provenanceRepositoryStorageUsage',
        'max_heap_bytes': 'maxHeapBytes',
        'max_heap': 'maxHeap',
        'garbage_collection_diagnostics': 'garbageCollectionDiagnostics',
        'cpu_cores': 'cpuCores',
        'cpu_load_average': 'cpuLoadAverage',
        'physical_memory_bytes': 'physicalMemoryBytes',
        'physical_memory': 'physicalMemory',
        'open_file_descriptors': 'openFileDescriptors',
        'max_open_file_descriptors': 'maxOpenFileDescriptors'
    }

    def __init__(self, flow_file_repository_storage_usage=None, content_repository_storage_usage=None, provenance_repository_storage_usage=None, max_heap_bytes=None, max_heap=None, garbage_collection_diagnostics=None, cpu_cores=None, cpu_load_average=None, physical_memory_bytes=None, physical_memory=None, open_file_descriptors=None, max_open_file_descriptors=None):
        """
        JVMSystemDiagnosticsSnapshotDTO - a model defined in Swagger
        """

        self._flow_file_repository_storage_usage = None
        self._content_repository_storage_usage = None
        self._provenance_repository_storage_usage = None
        self._max_heap_bytes = None
        self._max_heap = None
        self._garbage_collection_diagnostics = None
        self._cpu_cores = None
        self._cpu_load_average = None
        self._physical_memory_bytes = None
        self._physical_memory = None
        self._open_file_descriptors = None
        self._max_open_file_descriptors = None

        if flow_file_repository_storage_usage is not None:
          self.flow_file_repository_storage_usage = flow_file_repository_storage_usage
        if content_repository_storage_usage is not None:
          self.content_repository_storage_usage = content_repository_storage_usage
        if provenance_repository_storage_usage is not None:
          self.provenance_repository_storage_usage = provenance_repository_storage_usage
        if max_heap_bytes is not None:
          self.max_heap_bytes = max_heap_bytes
        if max_heap is not None:
          self.max_heap = max_heap
        if garbage_collection_diagnostics is not None:
          self.garbage_collection_diagnostics = garbage_collection_diagnostics
        if cpu_cores is not None:
          self.cpu_cores = cpu_cores
        if cpu_load_average is not None:
          self.cpu_load_average = cpu_load_average
        if physical_memory_bytes is not None:
          self.physical_memory_bytes = physical_memory_bytes
        if physical_memory is not None:
          self.physical_memory = physical_memory
        if open_file_descriptors is not None:
          self.open_file_descriptors = open_file_descriptors
        if max_open_file_descriptors is not None:
          self.max_open_file_descriptors = max_open_file_descriptors

    @property
    def flow_file_repository_storage_usage(self):
        """
        Gets the flow_file_repository_storage_usage of this JVMSystemDiagnosticsSnapshotDTO.
        Information about the FlowFile Repository's usage

        :return: The flow_file_repository_storage_usage of this JVMSystemDiagnosticsSnapshotDTO.
        :rtype: RepositoryUsageDTO
        """
        return self._flow_file_repository_storage_usage

    @flow_file_repository_storage_usage.setter
    def flow_file_repository_storage_usage(self, flow_file_repository_storage_usage):
        """
        Sets the flow_file_repository_storage_usage of this JVMSystemDiagnosticsSnapshotDTO.
        Information about the FlowFile Repository's usage

        :param flow_file_repository_storage_usage: The flow_file_repository_storage_usage of this JVMSystemDiagnosticsSnapshotDTO.
        :type: RepositoryUsageDTO
        """

        self._flow_file_repository_storage_usage = flow_file_repository_storage_usage

    @property
    def content_repository_storage_usage(self):
        """
        Gets the content_repository_storage_usage of this JVMSystemDiagnosticsSnapshotDTO.
        Information about the Content Repository's usage

        :return: The content_repository_storage_usage of this JVMSystemDiagnosticsSnapshotDTO.
        :rtype: list[RepositoryUsageDTO]
        """
        return self._content_repository_storage_usage

    @content_repository_storage_usage.setter
    def content_repository_storage_usage(self, content_repository_storage_usage):
        """
        Sets the content_repository_storage_usage of this JVMSystemDiagnosticsSnapshotDTO.
        Information about the Content Repository's usage

        :param content_repository_storage_usage: The content_repository_storage_usage of this JVMSystemDiagnosticsSnapshotDTO.
        :type: list[RepositoryUsageDTO]
        """

        self._content_repository_storage_usage = content_repository_storage_usage

    @property
    def provenance_repository_storage_usage(self):
        """
        Gets the provenance_repository_storage_usage of this JVMSystemDiagnosticsSnapshotDTO.
        Information about the Provenance Repository's usage

        :return: The provenance_repository_storage_usage of this JVMSystemDiagnosticsSnapshotDTO.
        :rtype: list[RepositoryUsageDTO]
        """
        return self._provenance_repository_storage_usage

    @provenance_repository_storage_usage.setter
    def provenance_repository_storage_usage(self, provenance_repository_storage_usage):
        """
        Sets the provenance_repository_storage_usage of this JVMSystemDiagnosticsSnapshotDTO.
        Information about the Provenance Repository's usage

        :param provenance_repository_storage_usage: The provenance_repository_storage_usage of this JVMSystemDiagnosticsSnapshotDTO.
        :type: list[RepositoryUsageDTO]
        """

        self._provenance_repository_storage_usage = provenance_repository_storage_usage

    @property
    def max_heap_bytes(self):
        """
        Gets the max_heap_bytes of this JVMSystemDiagnosticsSnapshotDTO.
        The maximum number of bytes that the JVM heap is configured to use for heap

        :return: The max_heap_bytes of this JVMSystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._max_heap_bytes

    @max_heap_bytes.setter
    def max_heap_bytes(self, max_heap_bytes):
        """
        Sets the max_heap_bytes of this JVMSystemDiagnosticsSnapshotDTO.
        The maximum number of bytes that the JVM heap is configured to use for heap

        :param max_heap_bytes: The max_heap_bytes of this JVMSystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._max_heap_bytes = max_heap_bytes

    @property
    def max_heap(self):
        """
        Gets the max_heap of this JVMSystemDiagnosticsSnapshotDTO.
        The maximum number of bytes that the JVM heap is configured to use, as a human-readable value

        :return: The max_heap of this JVMSystemDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._max_heap

    @max_heap.setter
    def max_heap(self, max_heap):
        """
        Sets the max_heap of this JVMSystemDiagnosticsSnapshotDTO.
        The maximum number of bytes that the JVM heap is configured to use, as a human-readable value

        :param max_heap: The max_heap of this JVMSystemDiagnosticsSnapshotDTO.
        :type: str
        """

        self._max_heap = max_heap

    @property
    def garbage_collection_diagnostics(self):
        """
        Gets the garbage_collection_diagnostics of this JVMSystemDiagnosticsSnapshotDTO.
        Diagnostic information about the JVM's garbage collections

        :return: The garbage_collection_diagnostics of this JVMSystemDiagnosticsSnapshotDTO.
        :rtype: list[GarbageCollectionDiagnosticsDTO]
        """
        return self._garbage_collection_diagnostics

    @garbage_collection_diagnostics.setter
    def garbage_collection_diagnostics(self, garbage_collection_diagnostics):
        """
        Sets the garbage_collection_diagnostics of this JVMSystemDiagnosticsSnapshotDTO.
        Diagnostic information about the JVM's garbage collections

        :param garbage_collection_diagnostics: The garbage_collection_diagnostics of this JVMSystemDiagnosticsSnapshotDTO.
        :type: list[GarbageCollectionDiagnosticsDTO]
        """

        self._garbage_collection_diagnostics = garbage_collection_diagnostics

    @property
    def cpu_cores(self):
        """
        Gets the cpu_cores of this JVMSystemDiagnosticsSnapshotDTO.
        The number of CPU Cores available on the system

        :return: The cpu_cores of this JVMSystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._cpu_cores

    @cpu_cores.setter
    def cpu_cores(self, cpu_cores):
        """
        Sets the cpu_cores of this JVMSystemDiagnosticsSnapshotDTO.
        The number of CPU Cores available on the system

        :param cpu_cores: The cpu_cores of this JVMSystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._cpu_cores = cpu_cores

    @property
    def cpu_load_average(self):
        """
        Gets the cpu_load_average of this JVMSystemDiagnosticsSnapshotDTO.
        The 1-minute CPU Load Average

        :return: The cpu_load_average of this JVMSystemDiagnosticsSnapshotDTO.
        :rtype: float
        """
        return self._cpu_load_average

    @cpu_load_average.setter
    def cpu_load_average(self, cpu_load_average):
        """
        Sets the cpu_load_average of this JVMSystemDiagnosticsSnapshotDTO.
        The 1-minute CPU Load Average

        :param cpu_load_average: The cpu_load_average of this JVMSystemDiagnosticsSnapshotDTO.
        :type: float
        """

        self._cpu_load_average = cpu_load_average

    @property
    def physical_memory_bytes(self):
        """
        Gets the physical_memory_bytes of this JVMSystemDiagnosticsSnapshotDTO.
        The number of bytes of RAM available on the system

        :return: The physical_memory_bytes of this JVMSystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._physical_memory_bytes

    @physical_memory_bytes.setter
    def physical_memory_bytes(self, physical_memory_bytes):
        """
        Sets the physical_memory_bytes of this JVMSystemDiagnosticsSnapshotDTO.
        The number of bytes of RAM available on the system

        :param physical_memory_bytes: The physical_memory_bytes of this JVMSystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._physical_memory_bytes = physical_memory_bytes

    @property
    def physical_memory(self):
        """
        Gets the physical_memory of this JVMSystemDiagnosticsSnapshotDTO.
        The number of bytes of RAM available on the system as a human-readable value

        :return: The physical_memory of this JVMSystemDiagnosticsSnapshotDTO.
        :rtype: str
        """
        return self._physical_memory

    @physical_memory.setter
    def physical_memory(self, physical_memory):
        """
        Sets the physical_memory of this JVMSystemDiagnosticsSnapshotDTO.
        The number of bytes of RAM available on the system as a human-readable value

        :param physical_memory: The physical_memory of this JVMSystemDiagnosticsSnapshotDTO.
        :type: str
        """

        self._physical_memory = physical_memory

    @property
    def open_file_descriptors(self):
        """
        Gets the open_file_descriptors of this JVMSystemDiagnosticsSnapshotDTO.
        The number of files that are open by the NiFi process

        :return: The open_file_descriptors of this JVMSystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._open_file_descriptors

    @open_file_descriptors.setter
    def open_file_descriptors(self, open_file_descriptors):
        """
        Sets the open_file_descriptors of this JVMSystemDiagnosticsSnapshotDTO.
        The number of files that are open by the NiFi process

        :param open_file_descriptors: The open_file_descriptors of this JVMSystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._open_file_descriptors = open_file_descriptors

    @property
    def max_open_file_descriptors(self):
        """
        Gets the max_open_file_descriptors of this JVMSystemDiagnosticsSnapshotDTO.
        The maximum number of open file descriptors that are available to each process

        :return: The max_open_file_descriptors of this JVMSystemDiagnosticsSnapshotDTO.
        :rtype: int
        """
        return self._max_open_file_descriptors

    @max_open_file_descriptors.setter
    def max_open_file_descriptors(self, max_open_file_descriptors):
        """
        Sets the max_open_file_descriptors of this JVMSystemDiagnosticsSnapshotDTO.
        The maximum number of open file descriptors that are available to each process

        :param max_open_file_descriptors: The max_open_file_descriptors of this JVMSystemDiagnosticsSnapshotDTO.
        :type: int
        """

        self._max_open_file_descriptors = max_open_file_descriptors

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in self.swagger_types.items():
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
        if not isinstance(other, JVMSystemDiagnosticsSnapshotDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
