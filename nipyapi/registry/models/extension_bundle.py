# coding: utf-8

"""
    Apache NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 1.19.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ExtensionBundle(object):
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
        'link': 'JaxbLink',
        'identifier': 'str',
        'name': 'str',
        'description': 'str',
        'bucket_identifier': 'str',
        'bucket_name': 'str',
        'created_timestamp': 'int',
        'modified_timestamp': 'int',
        'type': 'str',
        'permissions': 'Permissions',
        'bundle_type': 'str',
        'group_id': 'str',
        'artifact_id': 'str',
        'version_count': 'int'
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
        'permissions': 'permissions',
        'bundle_type': 'bundleType',
        'group_id': 'groupId',
        'artifact_id': 'artifactId',
        'version_count': 'versionCount'
    }

    def __init__(self, link=None, identifier=None, name=None, description=None, bucket_identifier=None, bucket_name=None, created_timestamp=None, modified_timestamp=None, type=None, permissions=None, bundle_type=None, group_id=None, artifact_id=None, version_count=None):
        """
        ExtensionBundle - a model defined in Swagger
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
        self._bundle_type = None
        self._group_id = None
        self._artifact_id = None
        self._version_count = None

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
        self.bundle_type = bundle_type
        if group_id is not None:
          self.group_id = group_id
        if artifact_id is not None:
          self.artifact_id = artifact_id
        if version_count is not None:
          self.version_count = version_count

    @property
    def link(self):
        """
        Gets the link of this ExtensionBundle.
        An WebLink to this entity.

        :return: The link of this ExtensionBundle.
        :rtype: JaxbLink
        """
        return self._link

    @link.setter
    def link(self, link):
        """
        Sets the link of this ExtensionBundle.
        An WebLink to this entity.

        :param link: The link of this ExtensionBundle.
        :type: JaxbLink
        """

        self._link = link

    @property
    def identifier(self):
        """
        Gets the identifier of this ExtensionBundle.
        An ID to uniquely identify this object.

        :return: The identifier of this ExtensionBundle.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this ExtensionBundle.
        An ID to uniquely identify this object.

        :param identifier: The identifier of this ExtensionBundle.
        :type: str
        """

        self._identifier = identifier

    @property
    def name(self):
        """
        Gets the name of this ExtensionBundle.
        The name of the item.

        :return: The name of this ExtensionBundle.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ExtensionBundle.
        The name of the item.

        :param name: The name of this ExtensionBundle.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this ExtensionBundle.
        A description of the item.

        :return: The description of this ExtensionBundle.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this ExtensionBundle.
        A description of the item.

        :param description: The description of this ExtensionBundle.
        :type: str
        """

        self._description = description

    @property
    def bucket_identifier(self):
        """
        Gets the bucket_identifier of this ExtensionBundle.
        The identifier of the bucket this items belongs to. This cannot be changed after the item is created.

        :return: The bucket_identifier of this ExtensionBundle.
        :rtype: str
        """
        return self._bucket_identifier

    @bucket_identifier.setter
    def bucket_identifier(self, bucket_identifier):
        """
        Sets the bucket_identifier of this ExtensionBundle.
        The identifier of the bucket this items belongs to. This cannot be changed after the item is created.

        :param bucket_identifier: The bucket_identifier of this ExtensionBundle.
        :type: str
        """
        if bucket_identifier is None:
            raise ValueError("Invalid value for `bucket_identifier`, must not be `None`")

        self._bucket_identifier = bucket_identifier

    @property
    def bucket_name(self):
        """
        Gets the bucket_name of this ExtensionBundle.
        The name of the bucket this items belongs to.

        :return: The bucket_name of this ExtensionBundle.
        :rtype: str
        """
        return self._bucket_name

    @bucket_name.setter
    def bucket_name(self, bucket_name):
        """
        Sets the bucket_name of this ExtensionBundle.
        The name of the bucket this items belongs to.

        :param bucket_name: The bucket_name of this ExtensionBundle.
        :type: str
        """

        self._bucket_name = bucket_name

    @property
    def created_timestamp(self):
        """
        Gets the created_timestamp of this ExtensionBundle.
        The timestamp of when the item was created, as milliseconds since epoch.

        :return: The created_timestamp of this ExtensionBundle.
        :rtype: int
        """
        return self._created_timestamp

    @created_timestamp.setter
    def created_timestamp(self, created_timestamp):
        """
        Sets the created_timestamp of this ExtensionBundle.
        The timestamp of when the item was created, as milliseconds since epoch.

        :param created_timestamp: The created_timestamp of this ExtensionBundle.
        :type: int
        """
        if created_timestamp is not None and created_timestamp < 1:
            raise ValueError("Invalid value for `created_timestamp`, must be a value greater than or equal to `1`")

        self._created_timestamp = created_timestamp

    @property
    def modified_timestamp(self):
        """
        Gets the modified_timestamp of this ExtensionBundle.
        The timestamp of when the item was last modified, as milliseconds since epoch.

        :return: The modified_timestamp of this ExtensionBundle.
        :rtype: int
        """
        return self._modified_timestamp

    @modified_timestamp.setter
    def modified_timestamp(self, modified_timestamp):
        """
        Sets the modified_timestamp of this ExtensionBundle.
        The timestamp of when the item was last modified, as milliseconds since epoch.

        :param modified_timestamp: The modified_timestamp of this ExtensionBundle.
        :type: int
        """
        if modified_timestamp is not None and modified_timestamp < 1:
            raise ValueError("Invalid value for `modified_timestamp`, must be a value greater than or equal to `1`")

        self._modified_timestamp = modified_timestamp

    @property
    def type(self):
        """
        Gets the type of this ExtensionBundle.
        The type of item.

        :return: The type of this ExtensionBundle.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ExtensionBundle.
        The type of item.

        :param type: The type of this ExtensionBundle.
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")
        allowed_values = ["Flow", "Bundle"]
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def permissions(self):
        """
        Gets the permissions of this ExtensionBundle.
        The access that the current user has to the bucket containing this item.

        :return: The permissions of this ExtensionBundle.
        :rtype: Permissions
        """
        return self._permissions

    @permissions.setter
    def permissions(self, permissions):
        """
        Sets the permissions of this ExtensionBundle.
        The access that the current user has to the bucket containing this item.

        :param permissions: The permissions of this ExtensionBundle.
        :type: Permissions
        """

        self._permissions = permissions

    @property
    def bundle_type(self):
        """
        Gets the bundle_type of this ExtensionBundle.
        The type of the extension bundle

        :return: The bundle_type of this ExtensionBundle.
        :rtype: str
        """
        return self._bundle_type

    @bundle_type.setter
    def bundle_type(self, bundle_type):
        """
        Sets the bundle_type of this ExtensionBundle.
        The type of the extension bundle

        :param bundle_type: The bundle_type of this ExtensionBundle.
        :type: str
        """
        if bundle_type is None:
            raise ValueError("Invalid value for `bundle_type`, must not be `None`")
        allowed_values = ["NIFI_NAR", "MINIFI_CPP"]
        if bundle_type not in allowed_values:
            raise ValueError(
                "Invalid value for `bundle_type` ({0}), must be one of {1}"
                .format(bundle_type, allowed_values)
            )

        self._bundle_type = bundle_type

    @property
    def group_id(self):
        """
        Gets the group_id of this ExtensionBundle.
        The group id of the extension bundle

        :return: The group_id of this ExtensionBundle.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """
        Sets the group_id of this ExtensionBundle.
        The group id of the extension bundle

        :param group_id: The group_id of this ExtensionBundle.
        :type: str
        """

        self._group_id = group_id

    @property
    def artifact_id(self):
        """
        Gets the artifact_id of this ExtensionBundle.
        The artifact id of the extension bundle

        :return: The artifact_id of this ExtensionBundle.
        :rtype: str
        """
        return self._artifact_id

    @artifact_id.setter
    def artifact_id(self, artifact_id):
        """
        Sets the artifact_id of this ExtensionBundle.
        The artifact id of the extension bundle

        :param artifact_id: The artifact_id of this ExtensionBundle.
        :type: str
        """

        self._artifact_id = artifact_id

    @property
    def version_count(self):
        """
        Gets the version_count of this ExtensionBundle.
        The number of versions of this extension bundle.

        :return: The version_count of this ExtensionBundle.
        :rtype: int
        """
        return self._version_count

    @version_count.setter
    def version_count(self, version_count):
        """
        Sets the version_count of this ExtensionBundle.
        The number of versions of this extension bundle.

        :param version_count: The version_count of this ExtensionBundle.
        :type: int
        """
        if version_count is not None and version_count < 0:
            raise ValueError("Invalid value for `version_count`, must be a value greater than or equal to `0`")

        self._version_count = version_count

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
        if not isinstance(other, ExtensionBundle):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
