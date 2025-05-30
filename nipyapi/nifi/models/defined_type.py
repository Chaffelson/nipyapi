"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class DefinedType(object):
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
        'group': 'str',
        'artifact': 'str',
        'version': 'str',
        'type': 'str',
        'type_description': 'str'
    }

    attribute_map = {
        'group': 'group',
        'artifact': 'artifact',
        'version': 'version',
        'type': 'type',
        'type_description': 'typeDescription'
    }

    def __init__(self, group=None, artifact=None, version=None, type=None, type_description=None):
        """
        DefinedType - a model defined in Swagger
        """

        self._group = None
        self._artifact = None
        self._version = None
        self._type = None
        self._type_description = None

        if group is not None:
          self.group = group
        if artifact is not None:
          self.artifact = artifact
        if version is not None:
          self.version = version
        self.type = type
        if type_description is not None:
          self.type_description = type_description

    @property
    def group(self):
        """
        Gets the group of this DefinedType.
        The group name of the bundle that provides the referenced type.

        :return: The group of this DefinedType.
        :rtype: str
        """
        return self._group

    @group.setter
    def group(self, group):
        """
        Sets the group of this DefinedType.
        The group name of the bundle that provides the referenced type.

        :param group: The group of this DefinedType.
        :type: str
        """

        self._group = group

    @property
    def artifact(self):
        """
        Gets the artifact of this DefinedType.
        The artifact name of the bundle that provides the referenced type.

        :return: The artifact of this DefinedType.
        :rtype: str
        """
        return self._artifact

    @artifact.setter
    def artifact(self, artifact):
        """
        Sets the artifact of this DefinedType.
        The artifact name of the bundle that provides the referenced type.

        :param artifact: The artifact of this DefinedType.
        :type: str
        """

        self._artifact = artifact

    @property
    def version(self):
        """
        Gets the version of this DefinedType.
        The version of the bundle that provides the referenced type.

        :return: The version of this DefinedType.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this DefinedType.
        The version of the bundle that provides the referenced type.

        :param version: The version of this DefinedType.
        :type: str
        """

        self._version = version

    @property
    def type(self):
        """
        Gets the type of this DefinedType.
        The fully-qualified class type

        :return: The type of this DefinedType.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this DefinedType.
        The fully-qualified class type

        :param type: The type of this DefinedType.
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")

        self._type = type

    @property
    def type_description(self):
        """
        Gets the type_description of this DefinedType.
        The description of the type.

        :return: The type_description of this DefinedType.
        :rtype: str
        """
        return self._type_description

    @type_description.setter
    def type_description(self, type_description):
        """
        Sets the type_description of this DefinedType.
        The description of the type.

        :param type_description: The type_description of this DefinedType.
        :type: str
        """

        self._type_description = type_description

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
        if not isinstance(other, DefinedType):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
