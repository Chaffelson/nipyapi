# coding: utf-8

"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.19.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ThreadDumpDTO(object):
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
        'node_id': 'str',
        'node_address': 'str',
        'api_port': 'int',
        'stack_trace': 'str',
        'thread_name': 'str',
        'thread_active_millis': 'int',
        'task_terminated': 'bool'
    }

    attribute_map = {
        'node_id': 'nodeId',
        'node_address': 'nodeAddress',
        'api_port': 'apiPort',
        'stack_trace': 'stackTrace',
        'thread_name': 'threadName',
        'thread_active_millis': 'threadActiveMillis',
        'task_terminated': 'taskTerminated'
    }

    def __init__(self, node_id=None, node_address=None, api_port=None, stack_trace=None, thread_name=None, thread_active_millis=None, task_terminated=None):
        """
        ThreadDumpDTO - a model defined in Swagger
        """

        self._node_id = None
        self._node_address = None
        self._api_port = None
        self._stack_trace = None
        self._thread_name = None
        self._thread_active_millis = None
        self._task_terminated = None

        if node_id is not None:
          self.node_id = node_id
        if node_address is not None:
          self.node_address = node_address
        if api_port is not None:
          self.api_port = api_port
        if stack_trace is not None:
          self.stack_trace = stack_trace
        if thread_name is not None:
          self.thread_name = thread_name
        if thread_active_millis is not None:
          self.thread_active_millis = thread_active_millis
        if task_terminated is not None:
          self.task_terminated = task_terminated

    @property
    def node_id(self):
        """
        Gets the node_id of this ThreadDumpDTO.
        The ID of the node in the cluster

        :return: The node_id of this ThreadDumpDTO.
        :rtype: str
        """
        return self._node_id

    @node_id.setter
    def node_id(self, node_id):
        """
        Sets the node_id of this ThreadDumpDTO.
        The ID of the node in the cluster

        :param node_id: The node_id of this ThreadDumpDTO.
        :type: str
        """

        self._node_id = node_id

    @property
    def node_address(self):
        """
        Gets the node_address of this ThreadDumpDTO.
        The address of the node in the cluster

        :return: The node_address of this ThreadDumpDTO.
        :rtype: str
        """
        return self._node_address

    @node_address.setter
    def node_address(self, node_address):
        """
        Sets the node_address of this ThreadDumpDTO.
        The address of the node in the cluster

        :param node_address: The node_address of this ThreadDumpDTO.
        :type: str
        """

        self._node_address = node_address

    @property
    def api_port(self):
        """
        Gets the api_port of this ThreadDumpDTO.
        The port the node is listening for API requests.

        :return: The api_port of this ThreadDumpDTO.
        :rtype: int
        """
        return self._api_port

    @api_port.setter
    def api_port(self, api_port):
        """
        Sets the api_port of this ThreadDumpDTO.
        The port the node is listening for API requests.

        :param api_port: The api_port of this ThreadDumpDTO.
        :type: int
        """

        self._api_port = api_port

    @property
    def stack_trace(self):
        """
        Gets the stack_trace of this ThreadDumpDTO.
        The stack trace for the thread

        :return: The stack_trace of this ThreadDumpDTO.
        :rtype: str
        """
        return self._stack_trace

    @stack_trace.setter
    def stack_trace(self, stack_trace):
        """
        Sets the stack_trace of this ThreadDumpDTO.
        The stack trace for the thread

        :param stack_trace: The stack_trace of this ThreadDumpDTO.
        :type: str
        """

        self._stack_trace = stack_trace

    @property
    def thread_name(self):
        """
        Gets the thread_name of this ThreadDumpDTO.
        The name of the thread

        :return: The thread_name of this ThreadDumpDTO.
        :rtype: str
        """
        return self._thread_name

    @thread_name.setter
    def thread_name(self, thread_name):
        """
        Sets the thread_name of this ThreadDumpDTO.
        The name of the thread

        :param thread_name: The thread_name of this ThreadDumpDTO.
        :type: str
        """

        self._thread_name = thread_name

    @property
    def thread_active_millis(self):
        """
        Gets the thread_active_millis of this ThreadDumpDTO.
        The number of milliseconds that the thread has been executing in the Processor

        :return: The thread_active_millis of this ThreadDumpDTO.
        :rtype: int
        """
        return self._thread_active_millis

    @thread_active_millis.setter
    def thread_active_millis(self, thread_active_millis):
        """
        Sets the thread_active_millis of this ThreadDumpDTO.
        The number of milliseconds that the thread has been executing in the Processor

        :param thread_active_millis: The thread_active_millis of this ThreadDumpDTO.
        :type: int
        """

        self._thread_active_millis = thread_active_millis

    @property
    def task_terminated(self):
        """
        Gets the task_terminated of this ThreadDumpDTO.
        Indicates whether or not the user has requested that the task be terminated. If this is true, it may indicate that the thread is in a state where it will continue running indefinitely without returning.

        :return: The task_terminated of this ThreadDumpDTO.
        :rtype: bool
        """
        return self._task_terminated

    @task_terminated.setter
    def task_terminated(self, task_terminated):
        """
        Sets the task_terminated of this ThreadDumpDTO.
        Indicates whether or not the user has requested that the task be terminated. If this is true, it may indicate that the thread is in a state where it will continue running indefinitely without returning.

        :param task_terminated: The task_terminated of this ThreadDumpDTO.
        :type: bool
        """

        self._task_terminated = task_terminated

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
        if not isinstance(other, ThreadDumpDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
