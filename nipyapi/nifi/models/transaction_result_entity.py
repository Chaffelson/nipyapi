"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class TransactionResultEntity(object):
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
        'flow_file_sent': 'int',
        'response_code': 'int',
        'message': 'str'
    }

    attribute_map = {
        'flow_file_sent': 'flowFileSent',
        'response_code': 'responseCode',
        'message': 'message'
    }

    def __init__(self, flow_file_sent=None, response_code=None, message=None):
        """
        TransactionResultEntity - a model defined in Swagger
        """

        self._flow_file_sent = None
        self._response_code = None
        self._message = None

        if flow_file_sent is not None:
          self.flow_file_sent = flow_file_sent
        if response_code is not None:
          self.response_code = response_code
        if message is not None:
          self.message = message

    @property
    def flow_file_sent(self):
        """
        Gets the flow_file_sent of this TransactionResultEntity.

        :return: The flow_file_sent of this TransactionResultEntity.
        :rtype: int
        """
        return self._flow_file_sent

    @flow_file_sent.setter
    def flow_file_sent(self, flow_file_sent):
        """
        Sets the flow_file_sent of this TransactionResultEntity.

        :param flow_file_sent: The flow_file_sent of this TransactionResultEntity.
        :type: int
        """

        self._flow_file_sent = flow_file_sent

    @property
    def response_code(self):
        """
        Gets the response_code of this TransactionResultEntity.

        :return: The response_code of this TransactionResultEntity.
        :rtype: int
        """
        return self._response_code

    @response_code.setter
    def response_code(self, response_code):
        """
        Sets the response_code of this TransactionResultEntity.

        :param response_code: The response_code of this TransactionResultEntity.
        :type: int
        """

        self._response_code = response_code

    @property
    def message(self):
        """
        Gets the message of this TransactionResultEntity.

        :return: The message of this TransactionResultEntity.
        :rtype: str
        """
        return self._message

    @message.setter
    def message(self, message):
        """
        Sets the message of this TransactionResultEntity.

        :param message: The message of this TransactionResultEntity.
        :type: str
        """

        self._message = message

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
        if not isinstance(other, TransactionResultEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
