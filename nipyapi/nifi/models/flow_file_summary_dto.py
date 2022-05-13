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


class FlowFileSummaryDTO(object):
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
        'uri': 'str',
        'uuid': 'str',
        'filename': 'str',
        'position': 'int',
        'size': 'int',
        'queued_duration': 'int',
        'lineage_duration': 'int',
        'penalty_expires_in': 'int',
        'cluster_node_id': 'str',
        'cluster_node_address': 'str',
        'penalized': 'bool'
    }

    attribute_map = {
        'uri': 'uri',
        'uuid': 'uuid',
        'filename': 'filename',
        'position': 'position',
        'size': 'size',
        'queued_duration': 'queuedDuration',
        'lineage_duration': 'lineageDuration',
        'penalty_expires_in': 'penaltyExpiresIn',
        'cluster_node_id': 'clusterNodeId',
        'cluster_node_address': 'clusterNodeAddress',
        'penalized': 'penalized'
    }

    def __init__(self, uri=None, uuid=None, filename=None, position=None, size=None, queued_duration=None, lineage_duration=None, penalty_expires_in=None, cluster_node_id=None, cluster_node_address=None, penalized=None):
        """
        FlowFileSummaryDTO - a model defined in Swagger
        """

        self._uri = None
        self._uuid = None
        self._filename = None
        self._position = None
        self._size = None
        self._queued_duration = None
        self._lineage_duration = None
        self._penalty_expires_in = None
        self._cluster_node_id = None
        self._cluster_node_address = None
        self._penalized = None

        if uri is not None:
          self.uri = uri
        if uuid is not None:
          self.uuid = uuid
        if filename is not None:
          self.filename = filename
        if position is not None:
          self.position = position
        if size is not None:
          self.size = size
        if queued_duration is not None:
          self.queued_duration = queued_duration
        if lineage_duration is not None:
          self.lineage_duration = lineage_duration
        if penalty_expires_in is not None:
          self.penalty_expires_in = penalty_expires_in
        if cluster_node_id is not None:
          self.cluster_node_id = cluster_node_id
        if cluster_node_address is not None:
          self.cluster_node_address = cluster_node_address
        if penalized is not None:
          self.penalized = penalized

    @property
    def uri(self):
        """
        Gets the uri of this FlowFileSummaryDTO.
        The URI that can be used to access this FlowFile.

        :return: The uri of this FlowFileSummaryDTO.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """
        Sets the uri of this FlowFileSummaryDTO.
        The URI that can be used to access this FlowFile.

        :param uri: The uri of this FlowFileSummaryDTO.
        :type: str
        """

        self._uri = uri

    @property
    def uuid(self):
        """
        Gets the uuid of this FlowFileSummaryDTO.
        The FlowFile UUID.

        :return: The uuid of this FlowFileSummaryDTO.
        :rtype: str
        """
        return self._uuid

    @uuid.setter
    def uuid(self, uuid):
        """
        Sets the uuid of this FlowFileSummaryDTO.
        The FlowFile UUID.

        :param uuid: The uuid of this FlowFileSummaryDTO.
        :type: str
        """

        self._uuid = uuid

    @property
    def filename(self):
        """
        Gets the filename of this FlowFileSummaryDTO.
        The FlowFile filename.

        :return: The filename of this FlowFileSummaryDTO.
        :rtype: str
        """
        return self._filename

    @filename.setter
    def filename(self, filename):
        """
        Sets the filename of this FlowFileSummaryDTO.
        The FlowFile filename.

        :param filename: The filename of this FlowFileSummaryDTO.
        :type: str
        """

        self._filename = filename

    @property
    def position(self):
        """
        Gets the position of this FlowFileSummaryDTO.
        The FlowFile's position in the queue.

        :return: The position of this FlowFileSummaryDTO.
        :rtype: int
        """
        return self._position

    @position.setter
    def position(self, position):
        """
        Sets the position of this FlowFileSummaryDTO.
        The FlowFile's position in the queue.

        :param position: The position of this FlowFileSummaryDTO.
        :type: int
        """

        self._position = position

    @property
    def size(self):
        """
        Gets the size of this FlowFileSummaryDTO.
        The FlowFile file size.

        :return: The size of this FlowFileSummaryDTO.
        :rtype: int
        """
        return self._size

    @size.setter
    def size(self, size):
        """
        Sets the size of this FlowFileSummaryDTO.
        The FlowFile file size.

        :param size: The size of this FlowFileSummaryDTO.
        :type: int
        """

        self._size = size

    @property
    def queued_duration(self):
        """
        Gets the queued_duration of this FlowFileSummaryDTO.
        How long this FlowFile has been enqueued.

        :return: The queued_duration of this FlowFileSummaryDTO.
        :rtype: int
        """
        return self._queued_duration

    @queued_duration.setter
    def queued_duration(self, queued_duration):
        """
        Sets the queued_duration of this FlowFileSummaryDTO.
        How long this FlowFile has been enqueued.

        :param queued_duration: The queued_duration of this FlowFileSummaryDTO.
        :type: int
        """

        self._queued_duration = queued_duration

    @property
    def lineage_duration(self):
        """
        Gets the lineage_duration of this FlowFileSummaryDTO.
        Duration since the FlowFile's greatest ancestor entered the flow.

        :return: The lineage_duration of this FlowFileSummaryDTO.
        :rtype: int
        """
        return self._lineage_duration

    @lineage_duration.setter
    def lineage_duration(self, lineage_duration):
        """
        Sets the lineage_duration of this FlowFileSummaryDTO.
        Duration since the FlowFile's greatest ancestor entered the flow.

        :param lineage_duration: The lineage_duration of this FlowFileSummaryDTO.
        :type: int
        """

        self._lineage_duration = lineage_duration

    @property
    def penalty_expires_in(self):
        """
        Gets the penalty_expires_in of this FlowFileSummaryDTO.
        How long in milliseconds until the FlowFile penalty expires.

        :return: The penalty_expires_in of this FlowFileSummaryDTO.
        :rtype: int
        """
        return self._penalty_expires_in

    @penalty_expires_in.setter
    def penalty_expires_in(self, penalty_expires_in):
        """
        Sets the penalty_expires_in of this FlowFileSummaryDTO.
        How long in milliseconds until the FlowFile penalty expires.

        :param penalty_expires_in: The penalty_expires_in of this FlowFileSummaryDTO.
        :type: int
        """

        self._penalty_expires_in = penalty_expires_in

    @property
    def cluster_node_id(self):
        """
        Gets the cluster_node_id of this FlowFileSummaryDTO.
        The id of the node where this FlowFile resides.

        :return: The cluster_node_id of this FlowFileSummaryDTO.
        :rtype: str
        """
        return self._cluster_node_id

    @cluster_node_id.setter
    def cluster_node_id(self, cluster_node_id):
        """
        Sets the cluster_node_id of this FlowFileSummaryDTO.
        The id of the node where this FlowFile resides.

        :param cluster_node_id: The cluster_node_id of this FlowFileSummaryDTO.
        :type: str
        """

        self._cluster_node_id = cluster_node_id

    @property
    def cluster_node_address(self):
        """
        Gets the cluster_node_address of this FlowFileSummaryDTO.
        The label for the node where this FlowFile resides.

        :return: The cluster_node_address of this FlowFileSummaryDTO.
        :rtype: str
        """
        return self._cluster_node_address

    @cluster_node_address.setter
    def cluster_node_address(self, cluster_node_address):
        """
        Sets the cluster_node_address of this FlowFileSummaryDTO.
        The label for the node where this FlowFile resides.

        :param cluster_node_address: The cluster_node_address of this FlowFileSummaryDTO.
        :type: str
        """

        self._cluster_node_address = cluster_node_address

    @property
    def penalized(self):
        """
        Gets the penalized of this FlowFileSummaryDTO.
        If the FlowFile is penalized.

        :return: The penalized of this FlowFileSummaryDTO.
        :rtype: bool
        """
        return self._penalized

    @penalized.setter
    def penalized(self, penalized):
        """
        Sets the penalized of this FlowFileSummaryDTO.
        If the FlowFile is penalized.

        :param penalized: The penalized of this FlowFileSummaryDTO.
        :type: bool
        """

        self._penalized = penalized

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
        if not isinstance(other, FlowFileSummaryDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
