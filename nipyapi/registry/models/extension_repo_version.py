"""
    Apache NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class ExtensionRepoVersion(object):
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
        'extensions_link': 'JaxbLink',
        'download_link': 'JaxbLink',
        'sha256_link': 'JaxbLink',
        'sha256_supplied': 'JaxbLink'
    }

    attribute_map = {
        'extensions_link': 'extensionsLink',
        'download_link': 'downloadLink',
        'sha256_link': 'sha256Link',
        'sha256_supplied': 'sha256Supplied'
    }

    def __init__(self, extensions_link=None, download_link=None, sha256_link=None, sha256_supplied=None):
        """
        ExtensionRepoVersion - a model defined in Swagger
        """

        self._extensions_link = None
        self._download_link = None
        self._sha256_link = None
        self._sha256_supplied = None

        if extensions_link is not None:
          self.extensions_link = extensions_link
        if download_link is not None:
          self.download_link = download_link
        if sha256_link is not None:
          self.sha256_link = sha256_link
        if sha256_supplied is not None:
          self.sha256_supplied = sha256_supplied

    @property
    def extensions_link(self):
        """
        Gets the extensions_link of this ExtensionRepoVersion.
        The WebLink to view the metadata about the extensions contained in the extension bundle.

        :return: The extensions_link of this ExtensionRepoVersion.
        :rtype: JaxbLink
        """
        return self._extensions_link

    @extensions_link.setter
    def extensions_link(self, extensions_link):
        """
        Sets the extensions_link of this ExtensionRepoVersion.
        The WebLink to view the metadata about the extensions contained in the extension bundle.

        :param extensions_link: The extensions_link of this ExtensionRepoVersion.
        :type: JaxbLink
        """

        self._extensions_link = extensions_link

    @property
    def download_link(self):
        """
        Gets the download_link of this ExtensionRepoVersion.
        The WebLink to download this version of the extension bundle.

        :return: The download_link of this ExtensionRepoVersion.
        :rtype: JaxbLink
        """
        return self._download_link

    @download_link.setter
    def download_link(self, download_link):
        """
        Sets the download_link of this ExtensionRepoVersion.
        The WebLink to download this version of the extension bundle.

        :param download_link: The download_link of this ExtensionRepoVersion.
        :type: JaxbLink
        """

        self._download_link = download_link

    @property
    def sha256_link(self):
        """
        Gets the sha256_link of this ExtensionRepoVersion.
        The WebLink to retrieve the SHA-256 digest for this version of the extension bundle.

        :return: The sha256_link of this ExtensionRepoVersion.
        :rtype: JaxbLink
        """
        return self._sha256_link

    @sha256_link.setter
    def sha256_link(self, sha256_link):
        """
        Sets the sha256_link of this ExtensionRepoVersion.
        The WebLink to retrieve the SHA-256 digest for this version of the extension bundle.

        :param sha256_link: The sha256_link of this ExtensionRepoVersion.
        :type: JaxbLink
        """

        self._sha256_link = sha256_link

    @property
    def sha256_supplied(self):
        """
        Gets the sha256_supplied of this ExtensionRepoVersion.
        Indicates if the client supplied a SHA-256 when uploading this version of the extension bundle.

        :return: The sha256_supplied of this ExtensionRepoVersion.
        :rtype: JaxbLink
        """
        return self._sha256_supplied

    @sha256_supplied.setter
    def sha256_supplied(self, sha256_supplied):
        """
        Sets the sha256_supplied of this ExtensionRepoVersion.
        Indicates if the client supplied a SHA-256 when uploading this version of the extension bundle.

        :param sha256_supplied: The sha256_supplied of this ExtensionRepoVersion.
        :type: JaxbLink
        """

        self._sha256_supplied = sha256_supplied

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
        if not isinstance(other, ExtensionRepoVersion):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
