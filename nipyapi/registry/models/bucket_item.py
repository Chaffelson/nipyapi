# coding: utf-8

"""
    NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 0.2.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class BucketItem(object):
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
        'link': 'Link',
        'identifier': 'str',
        'name': 'str',
        'description': 'str',
        'bucket_identifier': 'str',
        'bucket_name': 'str',
        'created_timestamp': 'int',
        'modified_timestamp': 'int',
        'type': 'str',
        'permissions': 'Permissions'
    }

    attribute_map = {
        'link': 'link',
        'identifier': 'identifier',
        'name': 'name',
        'description': 'description',
        'bucket_identifier': 'bucketIdentifier',
        'bucket_name': 'bucketName',
        'created_timestamp': 'createdTimestamp',
        'modified_timestamp': 'modifiedTimestamp',
        'type': 'type',
        'permissions': 'permissions'
    }

    def __init__(self, link=None, identifier=None, name=None, description=None, bucket_identifier=None, bucket_name=None, created_timestamp=None, modified_timestamp=None, type=None, permissions=None):
        """
        BucketItem - a model defined in Swagger
        """

        self._link = None
        self._identifier = None
        self._name = None
        self._description = None
        self._bucket_identifier = None
        self._bucket_name = None
        self._created_timestamp = None
        self._modified_timestamp = None
        self._type = None
        self._permissions = None

        if link is not None:
          self.link = link
        if identifier is not None:
          self.identifier = identifier
        self.name = name
        if description is not None:
          self.description = description
        self.bucket_identifier = bucket_identifier
        if bucket_name is not None:
          self.bucket_name = bucket_name
        if created_timestamp is not None:
          self.created_timestamp = created_timestamp
        if modified_timestamp is not None:
          self.modified_timestamp = modified_timestamp
        self.type = type
        if permissions is not None:
          self.permissions = permissions

    @property
    def link(self):
        """
        Gets the link of this BucketItem.
        An WebLink to this entity.

        :return: The link of this BucketItem.
        :rtype: Link
        """
        return self._link

    @link.setter
    def link(self, link):
        """
        Sets the link of this BucketItem.
        An WebLink to this entity.

        :param link: The link of this BucketItem.
        :type: Link
        """

        self._link = link

    @property
    def identifier(self):
        """
        Gets the identifier of this BucketItem.
        An ID to uniquely identify this object.

        :return: The identifier of this BucketItem.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this BucketItem.
        An ID to uniquely identify this object.

        :param identifier: The identifier of this BucketItem.
        :type: str
        """

        self._identifier = identifier

    @property
    def name(self):
        """
        Gets the name of this BucketItem.
        The name of the item.

        :return: The name of this BucketItem.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this BucketItem.
        The name of the item.

        :param name: The name of this BucketItem.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this BucketItem.
        A description of the item.

        :return: The description of this BucketItem.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this BucketItem.
        A description of the item.

        :param description: The description of this BucketItem.
        :type: str
        """

        self._description = description

    @property
    def bucket_identifier(self):
        """
        Gets the bucket_identifier of this BucketItem.
        The identifier of the bucket this items belongs to. This cannot be changed after the item is created.

        :return: The bucket_identifier of this BucketItem.
        :rtype: str
        """
        return self._bucket_identifier

    @bucket_identifier.setter
    def bucket_identifier(self, bucket_identifier):
        """
        Sets the bucket_identifier of this BucketItem.
        The identifier of the bucket this items belongs to. This cannot be changed after the item is created.

        :param bucket_identifier: The bucket_identifier of this BucketItem.
        :type: str
        """
        if bucket_identifier is None:
            raise ValueError("Invalid value for `bucket_identifier`, must not be `None`")

        self._bucket_identifier = bucket_identifier

    @property
    def bucket_name(self):
        """
        Gets the bucket_name of this BucketItem.
        The name of the bucket this items belongs to.

        :return: The bucket_name of this BucketItem.
        :rtype: str
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        """
        Sets the bucket_name of this BucketItem.
        The name of the bucket this items belongs to.

        :param bucket_name: The bucket_name of this BucketItem.
        :type: str
        """

        self._bucket_name = bucket_name

    @property
    def created_timestamp(self):
        """
        Gets the created_timestamp of this BucketItem.
        The timestamp of when the item was created, as milliseconds since epoch.

        :return: The created_timestamp of this BucketItem.
        :rtype: int
        """
        return self._created_timestamp

    @created_timestamp.setter
    def created_timestamp(self, created_timestamp):
        """
        Sets the created_timestamp of this BucketItem.
        The timestamp of when the item was created, as milliseconds since epoch.

        :param created_timestamp: The created_timestamp of this BucketItem.
        :type: int
        """
        if created_timestamp is not None and created_timestamp < 1:
            raise ValueError("Invalid value for `created_timestamp`, must be a value greater than or equal to `1`")

        self._created_timestamp = created_timestamp

    @property
    def modified_timestamp(self):
        """
        Gets the modified_timestamp of this BucketItem.
        The timestamp of when the item was last modified, as milliseconds since epoch.

        :return: The modified_timestamp of this BucketItem.
        :rtype: int
        """
        return self._modified_timestamp

    @modified_timestamp.setter
    def modified_timestamp(self, modified_timestamp):
        """
        Sets the modified_timestamp of this BucketItem.
        The timestamp of when the item was last modified, as milliseconds since epoch.

        :param modified_timestamp: The modified_timestamp of this BucketItem.
        :type: int
        """
        if modified_timestamp is not None and modified_timestamp < 1:
            raise ValueError("Invalid value for `modified_timestamp`, must be a value greater than or equal to `1`")

        self._modified_timestamp = modified_timestamp

    @property
    def type(self):
        """
        Gets the type of this BucketItem.
        The type of item.

        :return: The type of this BucketItem.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this BucketItem.
        The type of item.

        :param type: The type of this BucketItem.
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")
        allowed_values = ["Flow"]
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def permissions(self):
        """
        Gets the permissions of this BucketItem.
        The access that the current user has to the bucket containing this item.

        :return: The permissions of this BucketItem.
        :rtype: Permissions
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """
        Sets the permissions of this BucketItem.
        The access that the current user has to the bucket containing this item.

        :param permissions: The permissions of this BucketItem.
        :type: Permissions
        """

        self._permissions = permissions

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
        if not isinstance(other, BucketItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
