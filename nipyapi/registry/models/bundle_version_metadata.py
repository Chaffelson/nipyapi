# coding: utf-8

"""
    Apache NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 1.27.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class BundleVersionMetadata(object):
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
        'id': 'str',
        'bundle_id': 'str',
        'bucket_id': 'str',
        'group_id': 'str',
        'artifact_id': 'str',
        'version': 'str',
        'timestamp': 'int',
        'author': 'str',
        'description': 'str',
        'sha256': 'str',
        'sha256_supplied': 'bool',
        'content_size': 'int',
        'system_api_version': 'str',
        'build_info': 'BuildInfo'
    }

    attribute_map = {
        'link': 'link',
        'id': 'id',
        'bundle_id': 'bundleId',
        'bucket_id': 'bucketId',
        'group_id': 'groupId',
        'artifact_id': 'artifactId',
        'version': 'version',
        'timestamp': 'timestamp',
        'author': 'author',
        'description': 'description',
        'sha256': 'sha256',
        'sha256_supplied': 'sha256Supplied',
        'content_size': 'contentSize',
        'system_api_version': 'systemApiVersion',
        'build_info': 'buildInfo'
    }

    def __init__(self, link=None, id=None, bundle_id=None, bucket_id=None, group_id=None, artifact_id=None, version=None, timestamp=None, author=None, description=None, sha256=None, sha256_supplied=None, content_size=None, system_api_version=None, build_info=None):
        """
        BundleVersionMetadata - a model defined in Swagger
        """

        self._link = None
        self._id = None
        self._bundle_id = None
        self._bucket_id = None
        self._group_id = None
        self._artifact_id = None
        self._version = None
        self._timestamp = None
        self._author = None
        self._description = None
        self._sha256 = None
        self._sha256_supplied = None
        self._content_size = None
        self._system_api_version = None
        self._build_info = None

        if link is not None:
          self.link = link
        if id is not None:
          self.id = id
        if bundle_id is not None:
          self.bundle_id = bundle_id
        self.bucket_id = bucket_id
        if group_id is not None:
          self.group_id = group_id
        if artifact_id is not None:
          self.artifact_id = artifact_id
        if version is not None:
          self.version = version
        if timestamp is not None:
          self.timestamp = timestamp
        if author is not None:
          self.author = author
        if description is not None:
          self.description = description
        if sha256 is not None:
          self.sha256 = sha256
        self.sha256_supplied = sha256_supplied
        self.content_size = content_size
        if system_api_version is not None:
          self.system_api_version = system_api_version
        self.build_info = build_info

    @property
    def link(self):
        """
        Gets the link of this BundleVersionMetadata.
        An WebLink to this entity.

        :return: The link of this BundleVersionMetadata.
        :rtype: JaxbLink
        """
        return self._link

    @link.setter
    def link(self, link):
        """
        Sets the link of this BundleVersionMetadata.
        An WebLink to this entity.

        :param link: The link of this BundleVersionMetadata.
        :type: JaxbLink
        """

        self._link = link

    @property
    def id(self):
        """
        Gets the id of this BundleVersionMetadata.
        The id of this version of the extension bundle

        :return: The id of this BundleVersionMetadata.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this BundleVersionMetadata.
        The id of this version of the extension bundle

        :param id: The id of this BundleVersionMetadata.
        :type: str
        """

        self._id = id

    @property
    def bundle_id(self):
        """
        Gets the bundle_id of this BundleVersionMetadata.
        The id of the extension bundle this version is for

        :return: The bundle_id of this BundleVersionMetadata.
        :rtype: str
        """
        return self._bundle_id

    @bundle_id.setter
    def bundle_id(self, bundle_id):
        """
        Sets the bundle_id of this BundleVersionMetadata.
        The id of the extension bundle this version is for

        :param bundle_id: The bundle_id of this BundleVersionMetadata.
        :type: str
        """

        self._bundle_id = bundle_id

    @property
    def bucket_id(self):
        """
        Gets the bucket_id of this BundleVersionMetadata.
        The id of the bucket the extension bundle belongs to

        :return: The bucket_id of this BundleVersionMetadata.
        :rtype: str
        """
        return self._bucket_id

    @bucket_id.setter
    def bucket_id(self, bucket_id):
        """
        Sets the bucket_id of this BundleVersionMetadata.
        The id of the bucket the extension bundle belongs to

        :param bucket_id: The bucket_id of this BundleVersionMetadata.
        :type: str
        """
        if bucket_id is None:
            raise ValueError("Invalid value for `bucket_id`, must not be `None`")

        self._bucket_id = bucket_id

    @property
    def group_id(self):
        """
        Gets the group_id of this BundleVersionMetadata.

        :return: The group_id of this BundleVersionMetadata.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """
        Sets the group_id of this BundleVersionMetadata.

        :param group_id: The group_id of this BundleVersionMetadata.
        :type: str
        """

        self._group_id = group_id

    @property
    def artifact_id(self):
        """
        Gets the artifact_id of this BundleVersionMetadata.

        :return: The artifact_id of this BundleVersionMetadata.
        :rtype: str
        """
        return self._artifact_id

    @artifact_id.setter
    def artifact_id(self, artifact_id):
        """
        Sets the artifact_id of this BundleVersionMetadata.

        :param artifact_id: The artifact_id of this BundleVersionMetadata.
        :type: str
        """

        self._artifact_id = artifact_id

    @property
    def version(self):
        """
        Gets the version of this BundleVersionMetadata.
        The version of the extension bundle

        :return: The version of this BundleVersionMetadata.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this BundleVersionMetadata.
        The version of the extension bundle

        :param version: The version of this BundleVersionMetadata.
        :type: str
        """

        self._version = version

    @property
    def timestamp(self):
        """
        Gets the timestamp of this BundleVersionMetadata.
        The timestamp of the create date of this version

        :return: The timestamp of this BundleVersionMetadata.
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Sets the timestamp of this BundleVersionMetadata.
        The timestamp of the create date of this version

        :param timestamp: The timestamp of this BundleVersionMetadata.
        :type: int
        """
        if timestamp is not None and timestamp < 1:
            raise ValueError("Invalid value for `timestamp`, must be a value greater than or equal to `1`")

        self._timestamp = timestamp

    @property
    def author(self):
        """
        Gets the author of this BundleVersionMetadata.
        The identity that created this version

        :return: The author of this BundleVersionMetadata.
        :rtype: str
        """
        return self._author

    @author.setter
    def author(self, author):
        """
        Sets the author of this BundleVersionMetadata.
        The identity that created this version

        :param author: The author of this BundleVersionMetadata.
        :type: str
        """

        self._author = author

    @property
    def description(self):
        """
        Gets the description of this BundleVersionMetadata.
        The description for this version

        :return: The description of this BundleVersionMetadata.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this BundleVersionMetadata.
        The description for this version

        :param description: The description of this BundleVersionMetadata.
        :type: str
        """

        self._description = description

    @property
    def sha256(self):
        """
        Gets the sha256 of this BundleVersionMetadata.
        The hex representation of the SHA-256 digest of the binary content for this version

        :return: The sha256 of this BundleVersionMetadata.
        :rtype: str
        """
        return self._sha256

    @sha256.setter
    def sha256(self, sha256):
        """
        Sets the sha256 of this BundleVersionMetadata.
        The hex representation of the SHA-256 digest of the binary content for this version

        :param sha256: The sha256 of this BundleVersionMetadata.
        :type: str
        """

        self._sha256 = sha256

    @property
    def sha256_supplied(self):
        """
        Gets the sha256_supplied of this BundleVersionMetadata.
        Whether or not the client supplied a SHA-256 when uploading the bundle

        :return: The sha256_supplied of this BundleVersionMetadata.
        :rtype: bool
        """
        return self._sha256_supplied

    @sha256_supplied.setter
    def sha256_supplied(self, sha256_supplied):
        """
        Sets the sha256_supplied of this BundleVersionMetadata.
        Whether or not the client supplied a SHA-256 when uploading the bundle

        :param sha256_supplied: The sha256_supplied of this BundleVersionMetadata.
        :type: bool
        """
        if sha256_supplied is None:
            raise ValueError("Invalid value for `sha256_supplied`, must not be `None`")

        self._sha256_supplied = sha256_supplied

    @property
    def content_size(self):
        """
        Gets the content_size of this BundleVersionMetadata.
        The size of the binary content for this version in bytes

        :return: The content_size of this BundleVersionMetadata.
        :rtype: int
        """
        return self._content_size

    @content_size.setter
    def content_size(self, content_size):
        """
        Sets the content_size of this BundleVersionMetadata.
        The size of the binary content for this version in bytes

        :param content_size: The content_size of this BundleVersionMetadata.
        :type: int
        """
        if content_size is None:
            raise ValueError("Invalid value for `content_size`, must not be `None`")
        if content_size is not None and content_size < 0:
            raise ValueError("Invalid value for `content_size`, must be a value greater than or equal to `0`")

        self._content_size = content_size

    @property
    def system_api_version(self):
        """
        Gets the system_api_version of this BundleVersionMetadata.
        The version of the system API that this bundle version was built against

        :return: The system_api_version of this BundleVersionMetadata.
        :rtype: str
        """
        return self._system_api_version

    @system_api_version.setter
    def system_api_version(self, system_api_version):
        """
        Sets the system_api_version of this BundleVersionMetadata.
        The version of the system API that this bundle version was built against

        :param system_api_version: The system_api_version of this BundleVersionMetadata.
        :type: str
        """

        self._system_api_version = system_api_version

    @property
    def build_info(self):
        """
        Gets the build_info of this BundleVersionMetadata.
        The build information about this version

        :return: The build_info of this BundleVersionMetadata.
        :rtype: BuildInfo
        """
        return self._build_info

    @build_info.setter
    def build_info(self, build_info):
        """
        Sets the build_info of this BundleVersionMetadata.
        The build information about this version

        :param build_info: The build_info of this BundleVersionMetadata.
        :type: BuildInfo
        """
        if build_info is None:
            raise ValueError("Invalid value for `build_info`, must not be `None`")

        self._build_info = build_info

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
        if not isinstance(other, BundleVersionMetadata):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
