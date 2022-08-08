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


class AccessStatusDTO(object):
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
        'identity': 'str',
        'status': 'str',
        'message': 'str'
    }

    attribute_map = {
        'identity': 'identity',
        'status': 'status',
        'message': 'message'
    }

    def __init__(self, identity=None, status=None, message=None):
        """
        AccessStatusDTO - a model defined in Swagger
        """

        self._identity = None
        self._status = None
        self._message = None

        if identity is not None:
          self.identity = identity
        if status is not None:
          self.status = status
        if message is not None:
          self.message = message

    @property
    def identity(self):
        """
        Gets the identity of this AccessStatusDTO.
        The user identity.

        :return: The identity of this AccessStatusDTO.
        :rtype: str
        """
        return self._identity

    @identity.setter
    def identity(self, identity):
        """
        Sets the identity of this AccessStatusDTO.
        The user identity.

        :param identity: The identity of this AccessStatusDTO.
        :type: str
        """

        self._identity = identity

    @property
    def status(self):
        """
        Gets the status of this AccessStatusDTO.
        The user access status.

        :return: The status of this AccessStatusDTO.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this AccessStatusDTO.
        The user access status.

        :param status: The status of this AccessStatusDTO.
        :type: str
        """

        self._status = status

    @property
    def message(self):
        """
        Gets the message of this AccessStatusDTO.
        Additional details about the user access status.

        :return: The message of this AccessStatusDTO.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this AccessStatusDTO.
        Additional details about the user access status.

        :param message: The message of this AccessStatusDTO.
        :type: str
        """

        self._message = message

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
        if not isinstance(other, AccessStatusDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
