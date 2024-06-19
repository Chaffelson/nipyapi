# coding: utf-8

"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.26.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class JmxMetricsResultDTO(object):
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
        'bean_name': 'str',
        'attribute_name': 'str',
        'attribute_value': 'object'
    }

    attribute_map = {
        'bean_name': 'beanName',
        'attribute_name': 'attributeName',
        'attribute_value': 'attributeValue'
    }

    def __init__(self, bean_name=None, attribute_name=None, attribute_value=None):
        """
        JmxMetricsResultDTO - a model defined in Swagger
        """

        self._bean_name = None
        self._attribute_name = None
        self._attribute_value = None

        if bean_name is not None:
          self.bean_name = bean_name
        if attribute_name is not None:
          self.attribute_name = attribute_name
        if attribute_value is not None:
          self.attribute_value = attribute_value

    @property
    def bean_name(self):
        """
        Gets the bean_name of this JmxMetricsResultDTO.
        The bean name of the metrics bean.

        :return: The bean_name of this JmxMetricsResultDTO.
        :rtype: str
        """
        return self._bean_name

    @bean_name.setter
    def bean_name(self, bean_name):
        """
        Sets the bean_name of this JmxMetricsResultDTO.
        The bean name of the metrics bean.

        :param bean_name: The bean_name of this JmxMetricsResultDTO.
        :type: str
        """

        self._bean_name = bean_name

    @property
    def attribute_name(self):
        """
        Gets the attribute_name of this JmxMetricsResultDTO.
        The attribute name of the metrics bean's attribute.

        :return: The attribute_name of this JmxMetricsResultDTO.
        :rtype: str
        """
        return self._attribute_name

    @attribute_name.setter
    def attribute_name(self, attribute_name):
        """
        Sets the attribute_name of this JmxMetricsResultDTO.
        The attribute name of the metrics bean's attribute.

        :param attribute_name: The attribute_name of this JmxMetricsResultDTO.
        :type: str
        """

        self._attribute_name = attribute_name

    @property
    def attribute_value(self):
        """
        Gets the attribute_value of this JmxMetricsResultDTO.
        The attribute value of the the metrics bean's attribute

        :return: The attribute_value of this JmxMetricsResultDTO.
        :rtype: object
        """
        return self._attribute_value

    @attribute_value.setter
    def attribute_value(self, attribute_value):
        """
        Sets the attribute_value of this JmxMetricsResultDTO.
        The attribute value of the the metrics bean's attribute

        :param attribute_value: The attribute_value of this JmxMetricsResultDTO.
        :type: object
        """

        self._attribute_value = attribute_value

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
        if not isinstance(other, JmxMetricsResultDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
