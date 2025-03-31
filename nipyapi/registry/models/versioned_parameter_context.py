"""
    Apache NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class VersionedParameterContext(object):
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
        'instance_identifier': 'str',
        'name': 'str',
        'comments': 'str',
        'position': 'Position',
        'parameters': 'list[VersionedParameter]',
        'inherited_parameter_contexts': 'list[str]',
        'description': 'str',
        'parameter_provider': 'str',
        'parameter_group_name': 'str',
        'component_type': 'str',
        'synchronized': 'bool',
        'group_identifier': 'str'
    }

    attribute_map = {
        'identifier': 'identifier',
        'instance_identifier': 'instanceIdentifier',
        'name': 'name',
        'comments': 'comments',
        'position': 'position',
        'parameters': 'parameters',
        'inherited_parameter_contexts': 'inheritedParameterContexts',
        'description': 'description',
        'parameter_provider': 'parameterProvider',
        'parameter_group_name': 'parameterGroupName',
        'component_type': 'componentType',
        'synchronized': 'synchronized',
        'group_identifier': 'groupIdentifier'
    }

    def __init__(self, identifier=None, instance_identifier=None, name=None, comments=None, position=None, parameters=None, inherited_parameter_contexts=None, description=None, parameter_provider=None, parameter_group_name=None, component_type=None, synchronized=None, group_identifier=None):
        """
        VersionedParameterContext - a model defined in Swagger
        """

        self._identifier = None
        self._instance_identifier = None
        self._name = None
        self._comments = None
        self._position = None
        self._parameters = None
        self._inherited_parameter_contexts = None
        self._description = None
        self._parameter_provider = None
        self._parameter_group_name = None
        self._component_type = None
        self._synchronized = None
        self._group_identifier = None

        if identifier is not None:
          self.identifier = identifier
        if instance_identifier is not None:
          self.instance_identifier = instance_identifier
        if name is not None:
          self.name = name
        if comments is not None:
          self.comments = comments
        if position is not None:
          self.position = position
        if parameters is not None:
          self.parameters = parameters
        if inherited_parameter_contexts is not None:
          self.inherited_parameter_contexts = inherited_parameter_contexts
        if description is not None:
          self.description = description
        if parameter_provider is not None:
          self.parameter_provider = parameter_provider
        if parameter_group_name is not None:
          self.parameter_group_name = parameter_group_name
        if component_type is not None:
          self.component_type = component_type
        if synchronized is not None:
          self.synchronized = synchronized
        if group_identifier is not None:
          self.group_identifier = group_identifier

    @property
    def identifier(self):
        """
        Gets the identifier of this VersionedParameterContext.
        The component's unique identifier

        :return: The identifier of this VersionedParameterContext.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this VersionedParameterContext.
        The component's unique identifier

        :param identifier: The identifier of this VersionedParameterContext.
        :type: str
        """

        self._identifier = identifier

    @property
    def instance_identifier(self):
        """
        Gets the instance_identifier of this VersionedParameterContext.
        The instance ID of an existing component that is described by this VersionedComponent, or null if this is not mapped to an instantiated component

        :return: The instance_identifier of this VersionedParameterContext.
        :rtype: str
        """
        return self._instance_identifier

    @instance_identifier.setter
    def instance_identifier(self, instance_identifier):
        """
        Sets the instance_identifier of this VersionedParameterContext.
        The instance ID of an existing component that is described by this VersionedComponent, or null if this is not mapped to an instantiated component

        :param instance_identifier: The instance_identifier of this VersionedParameterContext.
        :type: str
        """

        self._instance_identifier = instance_identifier

    @property
    def name(self):
        """
        Gets the name of this VersionedParameterContext.
        The component's name

        :return: The name of this VersionedParameterContext.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this VersionedParameterContext.
        The component's name

        :param name: The name of this VersionedParameterContext.
        :type: str
        """

        self._name = name

    @property
    def comments(self):
        """
        Gets the comments of this VersionedParameterContext.
        The user-supplied comments for the component

        :return: The comments of this VersionedParameterContext.
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """
        Sets the comments of this VersionedParameterContext.
        The user-supplied comments for the component

        :param comments: The comments of this VersionedParameterContext.
        :type: str
        """

        self._comments = comments

    @property
    def position(self):
        """
        Gets the position of this VersionedParameterContext.
        The component's position on the graph

        :return: The position of this VersionedParameterContext.
        :rtype: Position
        """
        return self._position

    @position.setter
    def position(self, position):
        """
        Sets the position of this VersionedParameterContext.
        The component's position on the graph

        :param position: The position of this VersionedParameterContext.
        :type: Position
        """

        self._position = position

    @property
    def parameters(self):
        """
        Gets the parameters of this VersionedParameterContext.
        The parameters in the context

        :return: The parameters of this VersionedParameterContext.
        :rtype: list[VersionedParameter]
        """
        return self._parameters

    @parameters.setter
    def parameters(self, parameters):
        """
        Sets the parameters of this VersionedParameterContext.
        The parameters in the context

        :param parameters: The parameters of this VersionedParameterContext.
        :type: list[VersionedParameter]
        """

        self._parameters = parameters

    @property
    def inherited_parameter_contexts(self):
        """
        Gets the inherited_parameter_contexts of this VersionedParameterContext.
        The names of additional parameter contexts from which to inherit parameters

        :return: The inherited_parameter_contexts of this VersionedParameterContext.
        :rtype: list[str]
        """
        return self._inherited_parameter_contexts

    @inherited_parameter_contexts.setter
    def inherited_parameter_contexts(self, inherited_parameter_contexts):
        """
        Sets the inherited_parameter_contexts of this VersionedParameterContext.
        The names of additional parameter contexts from which to inherit parameters

        :param inherited_parameter_contexts: The inherited_parameter_contexts of this VersionedParameterContext.
        :type: list[str]
        """

        self._inherited_parameter_contexts = inherited_parameter_contexts

    @property
    def description(self):
        """
        Gets the description of this VersionedParameterContext.
        The description of the parameter context

        :return: The description of this VersionedParameterContext.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this VersionedParameterContext.
        The description of the parameter context

        :param description: The description of this VersionedParameterContext.
        :type: str
        """

        self._description = description

    @property
    def parameter_provider(self):
        """
        Gets the parameter_provider of this VersionedParameterContext.
        The identifier of an optional parameter provider

        :return: The parameter_provider of this VersionedParameterContext.
        :rtype: str
        """
        return self._parameter_provider

    @parameter_provider.setter
    def parameter_provider(self, parameter_provider):
        """
        Sets the parameter_provider of this VersionedParameterContext.
        The identifier of an optional parameter provider

        :param parameter_provider: The parameter_provider of this VersionedParameterContext.
        :type: str
        """

        self._parameter_provider = parameter_provider

    @property
    def parameter_group_name(self):
        """
        Gets the parameter_group_name of this VersionedParameterContext.
        The corresponding parameter group name fetched from the parameter provider, if applicable

        :return: The parameter_group_name of this VersionedParameterContext.
        :rtype: str
        """
        return self._parameter_group_name

    @parameter_group_name.setter
    def parameter_group_name(self, parameter_group_name):
        """
        Sets the parameter_group_name of this VersionedParameterContext.
        The corresponding parameter group name fetched from the parameter provider, if applicable

        :param parameter_group_name: The parameter_group_name of this VersionedParameterContext.
        :type: str
        """

        self._parameter_group_name = parameter_group_name

    @property
    def component_type(self):
        """
        Gets the component_type of this VersionedParameterContext.

        :return: The component_type of this VersionedParameterContext.
        :rtype: str
        """
        return self._component_type

    @component_type.setter
    def component_type(self, component_type):
        """
        Sets the component_type of this VersionedParameterContext.

        :param component_type: The component_type of this VersionedParameterContext.
        :type: str
        """
        allowed_values = ["CONNECTION", "PROCESSOR", "PROCESS_GROUP", "REMOTE_PROCESS_GROUP", "INPUT_PORT", "OUTPUT_PORT", "REMOTE_INPUT_PORT", "REMOTE_OUTPUT_PORT", "FUNNEL", "LABEL", "CONTROLLER_SERVICE", "REPORTING_TASK", "PARAMETER_CONTEXT", "PARAMETER_PROVIDER", "TEMPLATE", "FLOW_REGISTRY_CLIENT"]
        if component_type not in allowed_values:
            raise ValueError(
                "Invalid value for `component_type` ({0}), must be one of {1}"
                .format(component_type, allowed_values)
            )

        self._component_type = component_type

    @property
    def synchronized(self):
        """
        Gets the synchronized of this VersionedParameterContext.
        True if the parameter provider is set and the context should receive updates when its parameters are next fetched

        :return: The synchronized of this VersionedParameterContext.
        :rtype: bool
        """
        return self._synchronized

    @synchronized.setter
    def synchronized(self, synchronized):
        """
        Sets the synchronized of this VersionedParameterContext.
        True if the parameter provider is set and the context should receive updates when its parameters are next fetched

        :param synchronized: The synchronized of this VersionedParameterContext.
        :type: bool
        """

        self._synchronized = synchronized

    @property
    def group_identifier(self):
        """
        Gets the group_identifier of this VersionedParameterContext.
        The ID of the Process Group that this component belongs to

        :return: The group_identifier of this VersionedParameterContext.
        :rtype: str
        """
        return self._group_identifier

    @group_identifier.setter
    def group_identifier(self, group_identifier):
        """
        Sets the group_identifier of this VersionedParameterContext.
        The ID of the Process Group that this component belongs to

        :param group_identifier: The group_identifier of this VersionedParameterContext.
        :type: str
        """

        self._group_identifier = group_identifier

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
        if not isinstance(other, VersionedParameterContext):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
