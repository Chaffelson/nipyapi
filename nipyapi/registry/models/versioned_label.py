# coding: utf-8

"""
    Apache NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 0.5.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class VersionedLabel(object):
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
        'identifier': 'str',
        'name': 'str',
        'comments': 'str',
        'position': 'Position',
        'label': 'str',
        'width': 'float',
        'height': 'float',
        'style': 'dict(str, str)',
        'component_type': 'str',
        'group_identifier': 'str'
    }

    attribute_map = {
        'identifier': 'identifier',
        'name': 'name',
        'comments': 'comments',
        'position': 'position',
        'label': 'label',
        'width': 'width',
        'height': 'height',
        'style': 'style',
        'component_type': 'componentType',
        'group_identifier': 'groupIdentifier'
    }

    def __init__(self, identifier=None, name=None, comments=None, position=None, label=None, width=None, height=None, style=None, component_type=None, group_identifier=None):
        """
        VersionedLabel - a model defined in Swagger
        """

        self._identifier = None
        self._name = None
        self._comments = None
        self._position = None
        self._label = None
        self._width = None
        self._height = None
        self._style = None
        self._component_type = None
        self._group_identifier = None

        if identifier is not None:
          self.identifier = identifier
        if name is not None:
          self.name = name
        if comments is not None:
          self.comments = comments
        if position is not None:
          self.position = position
        if label is not None:
          self.label = label
        if width is not None:
          self.width = width
        if height is not None:
          self.height = height
        if style is not None:
          self.style = style
        if component_type is not None:
          self.component_type = component_type
        if group_identifier is not None:
          self.group_identifier = group_identifier

    @property
    def identifier(self):
        """
        Gets the identifier of this VersionedLabel.
        The component's unique identifier

        :return: The identifier of this VersionedLabel.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this VersionedLabel.
        The component's unique identifier

        :param identifier: The identifier of this VersionedLabel.
        :type: str
        """

        self._identifier = identifier

    @property
    def name(self):
        """
        Gets the name of this VersionedLabel.
        The component's name

        :return: The name of this VersionedLabel.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this VersionedLabel.
        The component's name

        :param name: The name of this VersionedLabel.
        :type: str
        """

        self._name = name

    @property
    def comments(self):
        """
        Gets the comments of this VersionedLabel.
        The user-supplied comments for the component

        :return: The comments of this VersionedLabel.
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """
        Sets the comments of this VersionedLabel.
        The user-supplied comments for the component

        :param comments: The comments of this VersionedLabel.
        :type: str
        """

        self._comments = comments

    @property
    def position(self):
        """
        Gets the position of this VersionedLabel.
        The component's position on the graph

        :return: The position of this VersionedLabel.
        :rtype: Position
        """
        return self._position

    @position.setter
    def position(self, position):
        """
        Sets the position of this VersionedLabel.
        The component's position on the graph

        :param position: The position of this VersionedLabel.
        :type: Position
        """

        self._position = position

    @property
    def label(self):
        """
        Gets the label of this VersionedLabel.
        The text that appears in the label.

        :return: The label of this VersionedLabel.
        :rtype: str
        """
        return self._label

    @label.setter
    def label(self, label):
        """
        Sets the label of this VersionedLabel.
        The text that appears in the label.

        :param label: The label of this VersionedLabel.
        :type: str
        """

        self._label = label

    @property
    def width(self):
        """
        Gets the width of this VersionedLabel.
        The width of the label in pixels when at a 1:1 scale.

        :return: The width of this VersionedLabel.
        :rtype: float
        """
        return self._width

    @width.setter
    def width(self, width):
        """
        Sets the width of this VersionedLabel.
        The width of the label in pixels when at a 1:1 scale.

        :param width: The width of this VersionedLabel.
        :type: float
        """

        self._width = width

    @property
    def height(self):
        """
        Gets the height of this VersionedLabel.
        The height of the label in pixels when at a 1:1 scale.

        :return: The height of this VersionedLabel.
        :rtype: float
        """
        return self._height

    @height.setter
    def height(self, height):
        """
        Sets the height of this VersionedLabel.
        The height of the label in pixels when at a 1:1 scale.

        :param height: The height of this VersionedLabel.
        :type: float
        """

        self._height = height

    @property
    def style(self):
        """
        Gets the style of this VersionedLabel.
        The styles for this label (font-size : 12px, background-color : #eee, etc).

        :return: The style of this VersionedLabel.
        :rtype: dict(str, str)
        """
        return self._style

    @style.setter
    def style(self, style):
        """
        Sets the style of this VersionedLabel.
        The styles for this label (font-size : 12px, background-color : #eee, etc).

        :param style: The style of this VersionedLabel.
        :type: dict(str, str)
        """

        self._style = style

    @property
    def component_type(self):
        """
        Gets the component_type of this VersionedLabel.

        :return: The component_type of this VersionedLabel.
        :rtype: str
        """
        return self._component_type

    @component_type.setter
    def component_type(self, component_type):
        """
        Sets the component_type of this VersionedLabel.

        :param component_type: The component_type of this VersionedLabel.
        :type: str
        """
        allowed_values = ["CONNECTION", "PROCESSOR", "PROCESS_GROUP", "REMOTE_PROCESS_GROUP", "INPUT_PORT", "OUTPUT_PORT", "REMOTE_INPUT_PORT", "REMOTE_OUTPUT_PORT", "FUNNEL", "LABEL", "CONTROLLER_SERVICE"]
        if component_type not in allowed_values:
            raise ValueError(
                "Invalid value for `component_type` ({0}), must be one of {1}"
                .format(component_type, allowed_values)
            )

        self._component_type = component_type

    @property
    def group_identifier(self):
        """
        Gets the group_identifier of this VersionedLabel.
        The ID of the Process Group that this component belongs to

        :return: The group_identifier of this VersionedLabel.
        :rtype: str
        """
        return self._group_identifier

    @group_identifier.setter
    def group_identifier(self, group_identifier):
        """
        Sets the group_identifier of this VersionedLabel.
        The ID of the Process Group that this component belongs to

        :param group_identifier: The group_identifier of this VersionedLabel.
        :type: str
        """

        self._group_identifier = group_identifier

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
        if not isinstance(other, VersionedLabel):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
