# coding: utf-8

"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.17.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class BuildInfo(object):
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
        'version': 'str',
        'revision': 'str',
        'timestamp': 'int',
        'target_arch': 'str',
        'compiler': 'str',
        'compiler_flags': 'str'
    }

    attribute_map = {
        'version': 'version',
        'revision': 'revision',
        'timestamp': 'timestamp',
        'target_arch': 'targetArch',
        'compiler': 'compiler',
        'compiler_flags': 'compilerFlags'
    }

    def __init__(self, version=None, revision=None, timestamp=None, target_arch=None, compiler=None, compiler_flags=None):
        """
        BuildInfo - a model defined in Swagger
        """

        self._version = None
        self._revision = None
        self._timestamp = None
        self._target_arch = None
        self._compiler = None
        self._compiler_flags = None

        if version is not None:
          self.version = version
        if revision is not None:
          self.revision = revision
        if timestamp is not None:
          self.timestamp = timestamp
        if target_arch is not None:
          self.target_arch = target_arch
        if compiler is not None:
          self.compiler = compiler
        if compiler_flags is not None:
          self.compiler_flags = compiler_flags

    @property
    def version(self):
        """
        Gets the version of this BuildInfo.
        The version number of the built component.

        :return: The version of this BuildInfo.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this BuildInfo.
        The version number of the built component.

        :param version: The version of this BuildInfo.
        :type: str
        """

        self._version = version

    @property
    def revision(self):
        """
        Gets the revision of this BuildInfo.
        The SCM revision id of the source code used for this build.

        :return: The revision of this BuildInfo.
        :rtype: str
        """
        return self._revision

    @revision.setter
    def revision(self, revision):
        """
        Sets the revision of this BuildInfo.
        The SCM revision id of the source code used for this build.

        :param revision: The revision of this BuildInfo.
        :type: str
        """

        self._revision = revision

    @property
    def timestamp(self):
        """
        Gets the timestamp of this BuildInfo.
        The timestamp (milliseconds since Epoch) of the build.

        :return: The timestamp of this BuildInfo.
        :rtype: int
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Sets the timestamp of this BuildInfo.
        The timestamp (milliseconds since Epoch) of the build.

        :param timestamp: The timestamp of this BuildInfo.
        :type: int
        """

        self._timestamp = timestamp

    @property
    def target_arch(self):
        """
        Gets the target_arch of this BuildInfo.
        The target architecture of the built component.

        :return: The target_arch of this BuildInfo.
        :rtype: str
        """
        return self._target_arch

    @target_arch.setter
    def target_arch(self, target_arch):
        """
        Sets the target_arch of this BuildInfo.
        The target architecture of the built component.

        :param target_arch: The target_arch of this BuildInfo.
        :type: str
        """

        self._target_arch = target_arch

    @property
    def compiler(self):
        """
        Gets the compiler of this BuildInfo.
        The compiler used for the build

        :return: The compiler of this BuildInfo.
        :rtype: str
        """
        return self._compiler

    @compiler.setter
    def compiler(self, compiler):
        """
        Sets the compiler of this BuildInfo.
        The compiler used for the build

        :param compiler: The compiler of this BuildInfo.
        :type: str
        """

        self._compiler = compiler

    @property
    def compiler_flags(self):
        """
        Gets the compiler_flags of this BuildInfo.
        The compiler flags used for the build.

        :return: The compiler_flags of this BuildInfo.
        :rtype: str
        """
        return self._compiler_flags

    @compiler_flags.setter
    def compiler_flags(self, compiler_flags):
        """
        Sets the compiler_flags of this BuildInfo.
        The compiler flags used for the build.

        :param compiler_flags: The compiler_flags of this BuildInfo.
        :type: str
        """

        self._compiler_flags = compiler_flags

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
        if not isinstance(other, BuildInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
