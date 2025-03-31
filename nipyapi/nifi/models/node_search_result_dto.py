"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class NodeSearchResultDTO(object):
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
        'id': 'str',
        'address': 'str'
    }

    attribute_map = {
        'id': 'id',
        'address': 'address'
    }

    def __init__(self, id=None, address=None):
        """
        NodeSearchResultDTO - a model defined in Swagger
        """

        self._id = None
        self._address = None

        if id is not None:
          self.id = id
        if address is not None:
          self.address = address

    @property
    def id(self):
        """
        Gets the id of this NodeSearchResultDTO.
        The id of the node that matched the search.

        :return: The id of this NodeSearchResultDTO.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this NodeSearchResultDTO.
        The id of the node that matched the search.

        :param id: The id of this NodeSearchResultDTO.
        :type: str
        """

        self._id = id

    @property
    def address(self):
        """
        Gets the address of this NodeSearchResultDTO.
        The address of the node that matched the search.

        :return: The address of this NodeSearchResultDTO.
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """
        Sets the address of this NodeSearchResultDTO.
        The address of the node that matched the search.

        :param address: The address of this NodeSearchResultDTO.
        :type: str
        """

        self._address = address

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
        if not isinstance(other, NodeSearchResultDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
