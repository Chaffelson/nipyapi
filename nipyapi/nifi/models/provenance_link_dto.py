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


class ProvenanceLinkDTO(object):
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
        'source_id': 'str',
        'target_id': 'str',
        'flow_file_uuid': 'str',
        'timestamp': 'str',
        'millis': 'int'
    }

    attribute_map = {
        'source_id': 'sourceId',
        'target_id': 'targetId',
        'flow_file_uuid': 'flowFileUuid',
        'timestamp': 'timestamp',
        'millis': 'millis'
    }

    def __init__(self, source_id=None, target_id=None, flow_file_uuid=None, timestamp=None, millis=None):
        """
        ProvenanceLinkDTO - a model defined in Swagger
        """

        self._source_id = None
        self._target_id = None
        self._flow_file_uuid = None
        self._timestamp = None
        self._millis = None

        if source_id is not None:
          self.source_id = source_id
        if target_id is not None:
          self.target_id = target_id
        if flow_file_uuid is not None:
          self.flow_file_uuid = flow_file_uuid
        if timestamp is not None:
          self.timestamp = timestamp
        if millis is not None:
          self.millis = millis

    @property
    def source_id(self):
        """
        Gets the source_id of this ProvenanceLinkDTO.
        The source node id of the link.

        :return: The source_id of this ProvenanceLinkDTO.
        :rtype: str
        """
        return self._source_id

    @source_id.setter
    def source_id(self, source_id):
        """
        Sets the source_id of this ProvenanceLinkDTO.
        The source node id of the link.

        :param source_id: The source_id of this ProvenanceLinkDTO.
        :type: str
        """

        self._source_id = source_id

    @property
    def target_id(self):
        """
        Gets the target_id of this ProvenanceLinkDTO.
        The target node id of the link.

        :return: The target_id of this ProvenanceLinkDTO.
        :rtype: str
        """
        return self._target_id

    @target_id.setter
    def target_id(self, target_id):
        """
        Sets the target_id of this ProvenanceLinkDTO.
        The target node id of the link.

        :param target_id: The target_id of this ProvenanceLinkDTO.
        :type: str
        """

        self._target_id = target_id

    @property
    def flow_file_uuid(self):
        """
        Gets the flow_file_uuid of this ProvenanceLinkDTO.
        The flowfile uuid that traversed the link.

        :return: The flow_file_uuid of this ProvenanceLinkDTO.
        :rtype: str
        """
        return self._flow_file_uuid

    @flow_file_uuid.setter
    def flow_file_uuid(self, flow_file_uuid):
        """
        Sets the flow_file_uuid of this ProvenanceLinkDTO.
        The flowfile uuid that traversed the link.

        :param flow_file_uuid: The flow_file_uuid of this ProvenanceLinkDTO.
        :type: str
        """

        self._flow_file_uuid = flow_file_uuid

    @property
    def timestamp(self):
        """
        Gets the timestamp of this ProvenanceLinkDTO.
        The timestamp of the link (based on the destination).

        :return: The timestamp of this ProvenanceLinkDTO.
        :rtype: str
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Sets the timestamp of this ProvenanceLinkDTO.
        The timestamp of the link (based on the destination).

        :param timestamp: The timestamp of this ProvenanceLinkDTO.
        :type: str
        """

        self._timestamp = timestamp

    @property
    def millis(self):
        """
        Gets the millis of this ProvenanceLinkDTO.
        The timestamp of this link in milliseconds.

        :return: The millis of this ProvenanceLinkDTO.
        :rtype: int
        """
        return self._millis

    @millis.setter
    def millis(self, millis):
        """
        Sets the millis of this ProvenanceLinkDTO.
        The timestamp of this link in milliseconds.

        :param millis: The millis of this ProvenanceLinkDTO.
        :type: int
        """

        self._millis = millis

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
        if not isinstance(other, ProvenanceLinkDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
