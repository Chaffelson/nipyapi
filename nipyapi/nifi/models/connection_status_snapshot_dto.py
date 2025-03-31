"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class ConnectionStatusSnapshotDTO(object):
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
        'source_id': 'str',
        'source_name': 'str',
        'destination_id': 'str',
        'destination_name': 'str',
        'predictions': 'ConnectionStatusPredictionsSnapshotDTO',
        'flow_files_in': 'int',
        'bytes_in': 'int',
        'input': 'str',
        'flow_files_out': 'int',
        'bytes_out': 'int',
        'output': 'str',
        'flow_files_queued': 'int',
        'bytes_queued': 'int',
        'queued': 'str',
        'queued_size': 'str',
        'queued_count': 'str',
        'percent_use_count': 'int',
        'percent_use_bytes': 'int',
        'flow_file_availability': 'str'
    }

    attribute_map = {
        'id': 'id',
        'group_id': 'groupId',
        'name': 'name',
        'source_id': 'sourceId',
        'source_name': 'sourceName',
        'destination_id': 'destinationId',
        'destination_name': 'destinationName',
        'predictions': 'predictions',
        'flow_files_in': 'flowFilesIn',
        'bytes_in': 'bytesIn',
        'input': 'input',
        'flow_files_out': 'flowFilesOut',
        'bytes_out': 'bytesOut',
        'output': 'output',
        'flow_files_queued': 'flowFilesQueued',
        'bytes_queued': 'bytesQueued',
        'queued': 'queued',
        'queued_size': 'queuedSize',
        'queued_count': 'queuedCount',
        'percent_use_count': 'percentUseCount',
        'percent_use_bytes': 'percentUseBytes',
        'flow_file_availability': 'flowFileAvailability'
    }

    def __init__(self, id=None, group_id=None, name=None, source_id=None, source_name=None, destination_id=None, destination_name=None, predictions=None, flow_files_in=None, bytes_in=None, input=None, flow_files_out=None, bytes_out=None, output=None, flow_files_queued=None, bytes_queued=None, queued=None, queued_size=None, queued_count=None, percent_use_count=None, percent_use_bytes=None, flow_file_availability=None):
        """
        ConnectionStatusSnapshotDTO - a model defined in Swagger
        """

        self._id = None
        self._group_id = None
        self._name = None
        self._source_id = None
        self._source_name = None
        self._destination_id = None
        self._destination_name = None
        self._predictions = None
        self._flow_files_in = None
        self._bytes_in = None
        self._input = None
        self._flow_files_out = None
        self._bytes_out = None
        self._output = None
        self._flow_files_queued = None
        self._bytes_queued = None
        self._queued = None
        self._queued_size = None
        self._queued_count = None
        self._percent_use_count = None
        self._percent_use_bytes = None
        self._flow_file_availability = None

        if id is not None:
          self.id = id
        if group_id is not None:
          self.group_id = group_id
        if name is not None:
          self.name = name
        if source_id is not None:
          self.source_id = source_id
        if source_name is not None:
          self.source_name = source_name
        if destination_id is not None:
          self.destination_id = destination_id
        if destination_name is not None:
          self.destination_name = destination_name
        if predictions is not None:
          self.predictions = predictions
        if flow_files_in is not None:
          self.flow_files_in = flow_files_in
        if bytes_in is not None:
          self.bytes_in = bytes_in
        if input is not None:
          self.input = input
        if flow_files_out is not None:
          self.flow_files_out = flow_files_out
        if bytes_out is not None:
          self.bytes_out = bytes_out
        if output is not None:
          self.output = output
        if flow_files_queued is not None:
          self.flow_files_queued = flow_files_queued
        if bytes_queued is not None:
          self.bytes_queued = bytes_queued
        if queued is not None:
          self.queued = queued
        if queued_size is not None:
          self.queued_size = queued_size
        if queued_count is not None:
          self.queued_count = queued_count
        if percent_use_count is not None:
          self.percent_use_count = percent_use_count
        if percent_use_bytes is not None:
          self.percent_use_bytes = percent_use_bytes
        if flow_file_availability is not None:
          self.flow_file_availability = flow_file_availability

    @property
    def id(self):
        """
        Gets the id of this ConnectionStatusSnapshotDTO.
        The id of the connection.

        :return: The id of this ConnectionStatusSnapshotDTO.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ConnectionStatusSnapshotDTO.
        The id of the connection.

        :param id: The id of this ConnectionStatusSnapshotDTO.
        :type: str
        """

        self._id = id

    @property
    def group_id(self):
        """
        Gets the group_id of this ConnectionStatusSnapshotDTO.
        The id of the process group the connection belongs to.

        :return: The group_id of this ConnectionStatusSnapshotDTO.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """
        Sets the group_id of this ConnectionStatusSnapshotDTO.
        The id of the process group the connection belongs to.

        :param group_id: The group_id of this ConnectionStatusSnapshotDTO.
        :type: str
        """

        self._group_id = group_id

    @property
    def name(self):
        """
        Gets the name of this ConnectionStatusSnapshotDTO.
        The name of the connection.

        :return: The name of this ConnectionStatusSnapshotDTO.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ConnectionStatusSnapshotDTO.
        The name of the connection.

        :param name: The name of this ConnectionStatusSnapshotDTO.
        :type: str
        """

        self._name = name

    @property
    def source_id(self):
        """
        Gets the source_id of this ConnectionStatusSnapshotDTO.
        The id of the source of the connection.

        :return: The source_id of this ConnectionStatusSnapshotDTO.
        :rtype: str
        """
        return self._source_id

    @source_id.setter
    def source_id(self, source_id):
        """
        Sets the source_id of this ConnectionStatusSnapshotDTO.
        The id of the source of the connection.

        :param source_id: The source_id of this ConnectionStatusSnapshotDTO.
        :type: str
        """

        self._source_id = source_id

    @property
    def source_name(self):
        """
        Gets the source_name of this ConnectionStatusSnapshotDTO.
        The name of the source of the connection.

        :return: The source_name of this ConnectionStatusSnapshotDTO.
        :rtype: str
        """
        return self._source_name

    @source_name.setter
    def source_name(self, source_name):
        """
        Sets the source_name of this ConnectionStatusSnapshotDTO.
        The name of the source of the connection.

        :param source_name: The source_name of this ConnectionStatusSnapshotDTO.
        :type: str
        """

        self._source_name = source_name

    @property
    def destination_id(self):
        """
        Gets the destination_id of this ConnectionStatusSnapshotDTO.
        The id of the destination of the connection.

        :return: The destination_id of this ConnectionStatusSnapshotDTO.
        :rtype: str
        """
        return self._destination_id

    @destination_id.setter
    def destination_id(self, destination_id):
        """
        Sets the destination_id of this ConnectionStatusSnapshotDTO.
        The id of the destination of the connection.

        :param destination_id: The destination_id of this ConnectionStatusSnapshotDTO.
        :type: str
        """

        self._destination_id = destination_id

    @property
    def destination_name(self):
        """
        Gets the destination_name of this ConnectionStatusSnapshotDTO.
        The name of the destination of the connection.

        :return: The destination_name of this ConnectionStatusSnapshotDTO.
        :rtype: str
        """
        return self._destination_name

    @destination_name.setter
    def destination_name(self, destination_name):
        """
        Sets the destination_name of this ConnectionStatusSnapshotDTO.
        The name of the destination of the connection.

        :param destination_name: The destination_name of this ConnectionStatusSnapshotDTO.
        :type: str
        """

        self._destination_name = destination_name

    @property
    def predictions(self):
        """
        Gets the predictions of this ConnectionStatusSnapshotDTO.
        Predictions, if available, for this connection (null if not available)

        :return: The predictions of this ConnectionStatusSnapshotDTO.
        :rtype: ConnectionStatusPredictionsSnapshotDTO
        """
        return self._predictions

    @predictions.setter
    def predictions(self, predictions):
        """
        Sets the predictions of this ConnectionStatusSnapshotDTO.
        Predictions, if available, for this connection (null if not available)

        :param predictions: The predictions of this ConnectionStatusSnapshotDTO.
        :type: ConnectionStatusPredictionsSnapshotDTO
        """

        self._predictions = predictions

    @property
    def flow_files_in(self):
        """
        Gets the flow_files_in of this ConnectionStatusSnapshotDTO.
        The number of FlowFiles that have come into the connection in the last 5 minutes.

        :return: The flow_files_in of this ConnectionStatusSnapshotDTO.
        :rtype: int
        """
        return self._flow_files_in

    @flow_files_in.setter
    def flow_files_in(self, flow_files_in):
        """
        Sets the flow_files_in of this ConnectionStatusSnapshotDTO.
        The number of FlowFiles that have come into the connection in the last 5 minutes.

        :param flow_files_in: The flow_files_in of this ConnectionStatusSnapshotDTO.
        :type: int
        """

        self._flow_files_in = flow_files_in

    @property
    def bytes_in(self):
        """
        Gets the bytes_in of this ConnectionStatusSnapshotDTO.
        The size of the FlowFiles that have come into the connection in the last 5 minutes.

        :return: The bytes_in of this ConnectionStatusSnapshotDTO.
        :rtype: int
        """
        return self._bytes_in

    @bytes_in.setter
    def bytes_in(self, bytes_in):
        """
        Sets the bytes_in of this ConnectionStatusSnapshotDTO.
        The size of the FlowFiles that have come into the connection in the last 5 minutes.

        :param bytes_in: The bytes_in of this ConnectionStatusSnapshotDTO.
        :type: int
        """

        self._bytes_in = bytes_in

    @property
    def input(self):
        """
        Gets the input of this ConnectionStatusSnapshotDTO.
        The input count/size for the connection in the last 5 minutes, pretty printed.

        :return: The input of this ConnectionStatusSnapshotDTO.
        :rtype: str
        """
        return self._input

    @input.setter
    def input(self, input):
        """
        Sets the input of this ConnectionStatusSnapshotDTO.
        The input count/size for the connection in the last 5 minutes, pretty printed.

        :param input: The input of this ConnectionStatusSnapshotDTO.
        :type: str
        """

        self._input = input

    @property
    def flow_files_out(self):
        """
        Gets the flow_files_out of this ConnectionStatusSnapshotDTO.
        The number of FlowFiles that have left the connection in the last 5 minutes.

        :return: The flow_files_out of this ConnectionStatusSnapshotDTO.
        :rtype: int
        """
        return self._flow_files_out

    @flow_files_out.setter
    def flow_files_out(self, flow_files_out):
        """
        Sets the flow_files_out of this ConnectionStatusSnapshotDTO.
        The number of FlowFiles that have left the connection in the last 5 minutes.

        :param flow_files_out: The flow_files_out of this ConnectionStatusSnapshotDTO.
        :type: int
        """

        self._flow_files_out = flow_files_out

    @property
    def bytes_out(self):
        """
        Gets the bytes_out of this ConnectionStatusSnapshotDTO.
        The number of bytes that have left the connection in the last 5 minutes.

        :return: The bytes_out of this ConnectionStatusSnapshotDTO.
        :rtype: int
        """
        return self._bytes_out

    @bytes_out.setter
    def bytes_out(self, bytes_out):
        """
        Sets the bytes_out of this ConnectionStatusSnapshotDTO.
        The number of bytes that have left the connection in the last 5 minutes.

        :param bytes_out: The bytes_out of this ConnectionStatusSnapshotDTO.
        :type: int
        """

        self._bytes_out = bytes_out

    @property
    def output(self):
        """
        Gets the output of this ConnectionStatusSnapshotDTO.
        The output count/sie for the connection in the last 5 minutes, pretty printed.

        :return: The output of this ConnectionStatusSnapshotDTO.
        :rtype: str
        """
        return self._output

    @output.setter
    def output(self, output):
        """
        Sets the output of this ConnectionStatusSnapshotDTO.
        The output count/sie for the connection in the last 5 minutes, pretty printed.

        :param output: The output of this ConnectionStatusSnapshotDTO.
        :type: str
        """

        self._output = output

    @property
    def flow_files_queued(self):
        """
        Gets the flow_files_queued of this ConnectionStatusSnapshotDTO.
        The number of FlowFiles that are currently queued in the connection.

        :return: The flow_files_queued of this ConnectionStatusSnapshotDTO.
        :rtype: int
        """
        return self._flow_files_queued

    @flow_files_queued.setter
    def flow_files_queued(self, flow_files_queued):
        """
        Sets the flow_files_queued of this ConnectionStatusSnapshotDTO.
        The number of FlowFiles that are currently queued in the connection.

        :param flow_files_queued: The flow_files_queued of this ConnectionStatusSnapshotDTO.
        :type: int
        """

        self._flow_files_queued = flow_files_queued

    @property
    def bytes_queued(self):
        """
        Gets the bytes_queued of this ConnectionStatusSnapshotDTO.
        The size of the FlowFiles that are currently queued in the connection.

        :return: The bytes_queued of this ConnectionStatusSnapshotDTO.
        :rtype: int
        """
        return self._bytes_queued

    @bytes_queued.setter
    def bytes_queued(self, bytes_queued):
        """
        Sets the bytes_queued of this ConnectionStatusSnapshotDTO.
        The size of the FlowFiles that are currently queued in the connection.

        :param bytes_queued: The bytes_queued of this ConnectionStatusSnapshotDTO.
        :type: int
        """

        self._bytes_queued = bytes_queued

    @property
    def queued(self):
        """
        Gets the queued of this ConnectionStatusSnapshotDTO.
        The total count and size of queued flowfiles formatted.

        :return: The queued of this ConnectionStatusSnapshotDTO.
        :rtype: str
        """
        return self._queued

    @queued.setter
    def queued(self, queued):
        """
        Sets the queued of this ConnectionStatusSnapshotDTO.
        The total count and size of queued flowfiles formatted.

        :param queued: The queued of this ConnectionStatusSnapshotDTO.
        :type: str
        """

        self._queued = queued

    @property
    def queued_size(self):
        """
        Gets the queued_size of this ConnectionStatusSnapshotDTO.
        The total size of flowfiles that are queued formatted.

        :return: The queued_size of this ConnectionStatusSnapshotDTO.
        :rtype: str
        """
        return self._queued_size

    @queued_size.setter
    def queued_size(self, queued_size):
        """
        Sets the queued_size of this ConnectionStatusSnapshotDTO.
        The total size of flowfiles that are queued formatted.

        :param queued_size: The queued_size of this ConnectionStatusSnapshotDTO.
        :type: str
        """

        self._queued_size = queued_size

    @property
    def queued_count(self):
        """
        Gets the queued_count of this ConnectionStatusSnapshotDTO.
        The number of flowfiles that are queued, pretty printed.

        :return: The queued_count of this ConnectionStatusSnapshotDTO.
        :rtype: str
        """
        return self._queued_count

    @queued_count.setter
    def queued_count(self, queued_count):
        """
        Sets the queued_count of this ConnectionStatusSnapshotDTO.
        The number of flowfiles that are queued, pretty printed.

        :param queued_count: The queued_count of this ConnectionStatusSnapshotDTO.
        :type: str
        """

        self._queued_count = queued_count

    @property
    def percent_use_count(self):
        """
        Gets the percent_use_count of this ConnectionStatusSnapshotDTO.
        Connection percent use regarding queued flow files count and backpressure threshold if configured.

        :return: The percent_use_count of this ConnectionStatusSnapshotDTO.
        :rtype: int
        """
        return self._percent_use_count

    @percent_use_count.setter
    def percent_use_count(self, percent_use_count):
        """
        Sets the percent_use_count of this ConnectionStatusSnapshotDTO.
        Connection percent use regarding queued flow files count and backpressure threshold if configured.

        :param percent_use_count: The percent_use_count of this ConnectionStatusSnapshotDTO.
        :type: int
        """

        self._percent_use_count = percent_use_count

    @property
    def percent_use_bytes(self):
        """
        Gets the percent_use_bytes of this ConnectionStatusSnapshotDTO.
        Connection percent use regarding queued flow files size and backpressure threshold if configured.

        :return: The percent_use_bytes of this ConnectionStatusSnapshotDTO.
        :rtype: int
        """
        return self._percent_use_bytes

    @percent_use_bytes.setter
    def percent_use_bytes(self, percent_use_bytes):
        """
        Sets the percent_use_bytes of this ConnectionStatusSnapshotDTO.
        Connection percent use regarding queued flow files size and backpressure threshold if configured.

        :param percent_use_bytes: The percent_use_bytes of this ConnectionStatusSnapshotDTO.
        :type: int
        """

        self._percent_use_bytes = percent_use_bytes

    @property
    def flow_file_availability(self):
        """
        Gets the flow_file_availability of this ConnectionStatusSnapshotDTO.
        The availability of FlowFiles in this connection

        :return: The flow_file_availability of this ConnectionStatusSnapshotDTO.
        :rtype: str
        """
        return self._flow_file_availability

    @flow_file_availability.setter
    def flow_file_availability(self, flow_file_availability):
        """
        Sets the flow_file_availability of this ConnectionStatusSnapshotDTO.
        The availability of FlowFiles in this connection

        :param flow_file_availability: The flow_file_availability of this ConnectionStatusSnapshotDTO.
        :type: str
        """

        self._flow_file_availability = flow_file_availability

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
        if not isinstance(other, ConnectionStatusSnapshotDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
