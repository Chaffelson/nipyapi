"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class QueueSizeDTO(object):
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
        'byte_count': 'int',
        'object_count': 'int'
    }

    attribute_map = {
        'byte_count': 'byteCount',
        'object_count': 'objectCount'
    }

    def __init__(self, byte_count=None, object_count=None):
        """
        QueueSizeDTO - a model defined in Swagger
        """

        self._byte_count = None
        self._object_count = None

        if byte_count is not None:
          self.byte_count = byte_count
        if object_count is not None:
          self.object_count = object_count

    @property
    def byte_count(self):
        """
        Gets the byte_count of this QueueSizeDTO.
        The size of objects in a queue.

        :return: The byte_count of this QueueSizeDTO.
        :rtype: int
        """
        return self._byte_count

    @byte_count.setter
    def byte_count(self, byte_count):
        """
        Sets the byte_count of this QueueSizeDTO.
        The size of objects in a queue.

        :param byte_count: The byte_count of this QueueSizeDTO.
        :type: int
        """

        self._byte_count = byte_count

    @property
    def object_count(self):
        """
        Gets the object_count of this QueueSizeDTO.
        The count of objects in a queue.

        :return: The object_count of this QueueSizeDTO.
        :rtype: int
        """
        return self._object_count

    @object_count.setter
    def object_count(self, object_count):
        """
        Sets the object_count of this QueueSizeDTO.
        The count of objects in a queue.

        :param object_count: The object_count of this QueueSizeDTO.
        :type: int
        """

        self._object_count = object_count

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
        if not isinstance(other, QueueSizeDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
