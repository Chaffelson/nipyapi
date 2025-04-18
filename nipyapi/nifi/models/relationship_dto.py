"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class RelationshipDTO(object):
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
        'name': 'str',
        'description': 'str',
        'auto_terminate': 'bool',
        'retry': 'bool'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'auto_terminate': 'autoTerminate',
        'retry': 'retry'
    }

    def __init__(self, name=None, description=None, auto_terminate=None, retry=None):
        """
        RelationshipDTO - a model defined in Swagger
        """

        self._name = None
        self._description = None
        self._auto_terminate = None
        self._retry = None

        if name is not None:
          self.name = name
        if description is not None:
          self.description = description
        if auto_terminate is not None:
          self.auto_terminate = auto_terminate
        if retry is not None:
          self.retry = retry

    @property
    def name(self):
        """
        Gets the name of this RelationshipDTO.
        The relationship name.

        :return: The name of this RelationshipDTO.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this RelationshipDTO.
        The relationship name.

        :param name: The name of this RelationshipDTO.
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this RelationshipDTO.
        The relationship description.

        :return: The description of this RelationshipDTO.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this RelationshipDTO.
        The relationship description.

        :param description: The description of this RelationshipDTO.
        :type: str
        """

        self._description = description

    @property
    def auto_terminate(self):
        """
        Gets the auto_terminate of this RelationshipDTO.
        Whether or not flowfiles sent to this relationship should auto terminate.

        :return: The auto_terminate of this RelationshipDTO.
        :rtype: bool
        """
        return self._auto_terminate

    @auto_terminate.setter
    def auto_terminate(self, auto_terminate):
        """
        Sets the auto_terminate of this RelationshipDTO.
        Whether or not flowfiles sent to this relationship should auto terminate.

        :param auto_terminate: The auto_terminate of this RelationshipDTO.
        :type: bool
        """

        self._auto_terminate = auto_terminate

    @property
    def retry(self):
        """
        Gets the retry of this RelationshipDTO.
        Whether or not flowfiles sent to this relationship should retry.

        :return: The retry of this RelationshipDTO.
        :rtype: bool
        """
        return self._retry

    @retry.setter
    def retry(self, retry):
        """
        Sets the retry of this RelationshipDTO.
        Whether or not flowfiles sent to this relationship should retry.

        :param retry: The retry of this RelationshipDTO.
        :type: bool
        """

        self._retry = retry

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
        if not isinstance(other, RelationshipDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
