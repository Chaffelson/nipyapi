"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class BannerDTO(object):
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
        'header_text': 'str',
        'footer_text': 'str'
    }

    attribute_map = {
        'header_text': 'headerText',
        'footer_text': 'footerText'
    }

    def __init__(self, header_text=None, footer_text=None):
        """
        BannerDTO - a model defined in Swagger
        """

        self._header_text = None
        self._footer_text = None

        if header_text is not None:
          self.header_text = header_text
        if footer_text is not None:
          self.footer_text = footer_text

    @property
    def header_text(self):
        """
        Gets the header_text of this BannerDTO.
        The header text.

        :return: The header_text of this BannerDTO.
        :rtype: str
        """
        return self._header_text

    @header_text.setter
    def header_text(self, header_text):
        """
        Sets the header_text of this BannerDTO.
        The header text.

        :param header_text: The header_text of this BannerDTO.
        :type: str
        """

        self._header_text = header_text

    @property
    def footer_text(self):
        """
        Gets the footer_text of this BannerDTO.
        The footer text.

        :return: The footer_text of this BannerDTO.
        :rtype: str
        """
        return self._footer_text

    @footer_text.setter
    def footer_text(self, footer_text):
        """
        Sets the footer_text of this BannerDTO.
        The footer text.

        :param footer_text: The footer_text of this BannerDTO.
        :type: str
        """

        self._footer_text = footer_text

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
        if not isinstance(other, BannerDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
