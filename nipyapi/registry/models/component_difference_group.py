# coding: utf-8

"""
    Apache NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 1.23.2
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ComponentDifferenceGroup(object):
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
        'component_id': 'str',
        'component_name': 'str',
        'component_type': 'str',
        'process_group_id': 'str',
        'differences': 'list[ComponentDifference]'
    }

    attribute_map = {
        'component_id': 'componentId',
        'component_name': 'componentName',
        'component_type': 'componentType',
        'process_group_id': 'processGroupId',
        'differences': 'differences'
    }

    def __init__(self, component_id=None, component_name=None, component_type=None, process_group_id=None, differences=None):
        """
        ComponentDifferenceGroup - a model defined in Swagger
        """

        self._component_id = None
        self._component_name = None
        self._component_type = None
        self._process_group_id = None
        self._differences = None

        if component_id is not None:
          self.component_id = component_id
        if component_name is not None:
          self.component_name = component_name
        if component_type is not None:
          self.component_type = component_type
        if process_group_id is not None:
          self.process_group_id = process_group_id
        if differences is not None:
          self.differences = differences

    @property
    def component_id(self):
        """
        Gets the component_id of this ComponentDifferenceGroup.
        The id of the component whose changes are grouped together.

        :return: The component_id of this ComponentDifferenceGroup.
        :rtype: str
        """
        return self._component_id

    @component_id.setter
    def component_id(self, component_id):
        """
        Sets the component_id of this ComponentDifferenceGroup.
        The id of the component whose changes are grouped together.

        :param component_id: The component_id of this ComponentDifferenceGroup.
        :type: str
        """

        self._component_id = component_id

    @property
    def component_name(self):
        """
        Gets the component_name of this ComponentDifferenceGroup.
        The name of the component whose changes are grouped together.

        :return: The component_name of this ComponentDifferenceGroup.
        :rtype: str
        """
        return self._component_name

    @component_name.setter
    def component_name(self, component_name):
        """
        Sets the component_name of this ComponentDifferenceGroup.
        The name of the component whose changes are grouped together.

        :param component_name: The component_name of this ComponentDifferenceGroup.
        :type: str
        """

        self._component_name = component_name

    @property
    def component_type(self):
        """
        Gets the component_type of this ComponentDifferenceGroup.
        The type of component these changes relate to.

        :return: The component_type of this ComponentDifferenceGroup.
        :rtype: str
        """
        return self._component_type

    @component_type.setter
    def component_type(self, component_type):
        """
        Sets the component_type of this ComponentDifferenceGroup.
        The type of component these changes relate to.

        :param component_type: The component_type of this ComponentDifferenceGroup.
        :type: str
        """

        self._component_type = component_type

    @property
    def process_group_id(self):
        """
        Gets the process_group_id of this ComponentDifferenceGroup.
        The process group id for this component.

        :return: The process_group_id of this ComponentDifferenceGroup.
        :rtype: str
        """
        return self._process_group_id

    @process_group_id.setter
    def process_group_id(self, process_group_id):
        """
        Sets the process_group_id of this ComponentDifferenceGroup.
        The process group id for this component.

        :param process_group_id: The process_group_id of this ComponentDifferenceGroup.
        :type: str
        """

        self._process_group_id = process_group_id

    @property
    def differences(self):
        """
        Gets the differences of this ComponentDifferenceGroup.
        The list of changes related to this component between the 2 versions.

        :return: The differences of this ComponentDifferenceGroup.
        :rtype: list[ComponentDifference]
        """
        return self._differences

    @differences.setter
    def differences(self, differences):
        """
        Sets the differences of this ComponentDifferenceGroup.
        The list of changes related to this component between the 2 versions.

        :param differences: The differences of this ComponentDifferenceGroup.
        :type: list[ComponentDifference]
        """

        self._differences = differences

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
        if not isinstance(other, ComponentDifferenceGroup):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
