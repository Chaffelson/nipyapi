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


class BulletinEntity(object):
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
        'id': 'int',
        'group_id': 'str',
        'source_id': 'str',
        'timestamp': 'str',
        'node_address': 'str',
        'can_read': 'bool',
        'bulletin': 'BulletinDTO'
    }

    attribute_map = {
        'id': 'id',
        'group_id': 'groupId',
        'source_id': 'sourceId',
        'timestamp': 'timestamp',
        'node_address': 'nodeAddress',
        'can_read': 'canRead',
        'bulletin': 'bulletin'
    }

    def __init__(self, id=None, group_id=None, source_id=None, timestamp=None, node_address=None, can_read=None, bulletin=None):
        """
        BulletinEntity - a model defined in Swagger
        """

        self._id = None
        self._group_id = None
        self._source_id = None
        self._timestamp = None
        self._node_address = None
        self._can_read = None
        self._bulletin = None

        if id is not None:
          self.id = id
        if group_id is not None:
          self.group_id = group_id
        if source_id is not None:
          self.source_id = source_id
        if timestamp is not None:
          self.timestamp = timestamp
        if node_address is not None:
          self.node_address = node_address
        if can_read is not None:
          self.can_read = can_read
        if bulletin is not None:
          self.bulletin = bulletin

    @property
    def id(self):
        """
        Gets the id of this BulletinEntity.

        :return: The id of this BulletinEntity.
        :rtype: int
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this BulletinEntity.

        :param id: The id of this BulletinEntity.
        :type: int
        """

        self._id = id

    @property
    def group_id(self):
        """
        Gets the group_id of this BulletinEntity.

        :return: The group_id of this BulletinEntity.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """
        Sets the group_id of this BulletinEntity.

        :param group_id: The group_id of this BulletinEntity.
        :type: str
        """

        self._group_id = group_id

    @property
    def source_id(self):
        """
        Gets the source_id of this BulletinEntity.

        :return: The source_id of this BulletinEntity.
        :rtype: str
        """
        return self._source_id

    @source_id.setter
    def source_id(self, source_id):
        """
        Sets the source_id of this BulletinEntity.

        :param source_id: The source_id of this BulletinEntity.
        :type: str
        """

        self._source_id = source_id

    @property
    def timestamp(self):
        """
        Gets the timestamp of this BulletinEntity.
        When this bulletin was generated.

        :return: The timestamp of this BulletinEntity.
        :rtype: str
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Sets the timestamp of this BulletinEntity.
        When this bulletin was generated.

        :param timestamp: The timestamp of this BulletinEntity.
        :type: str
        """

        self._timestamp = timestamp

    @property
    def node_address(self):
        """
        Gets the node_address of this BulletinEntity.

        :return: The node_address of this BulletinEntity.
        :rtype: str
        """
        return self._node_address

    @node_address.setter
    def node_address(self, node_address):
        """
        Sets the node_address of this BulletinEntity.

        :param node_address: The node_address of this BulletinEntity.
        :type: str
        """

        self._node_address = node_address

    @property
    def can_read(self):
        """
        Gets the can_read of this BulletinEntity.
        Indicates whether the user can read a given resource.

        :return: The can_read of this BulletinEntity.
        :rtype: bool
        """
        return self._can_read

    @can_read.setter
    def can_read(self, can_read):
        """
        Sets the can_read of this BulletinEntity.
        Indicates whether the user can read a given resource.

        :param can_read: The can_read of this BulletinEntity.
        :type: bool
        """

        self._can_read = can_read

    @property
    def bulletin(self):
        """
        Gets the bulletin of this BulletinEntity.

        :return: The bulletin of this BulletinEntity.
        :rtype: BulletinDTO
        """
        return self._bulletin

    @bulletin.setter
    def bulletin(self, bulletin):
        """
        Sets the bulletin of this BulletinEntity.

        :param bulletin: The bulletin of this BulletinEntity.
        :type: BulletinDTO
        """

        self._bulletin = bulletin

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
        if not isinstance(other, BulletinEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
