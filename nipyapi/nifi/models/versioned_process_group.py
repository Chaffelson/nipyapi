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


class VersionedProcessGroup(object):
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
        'process_groups': 'list[VersionedProcessGroup]',
        'remote_process_groups': 'list[VersionedRemoteProcessGroup]',
        'processors': 'list[VersionedProcessor]',
        'input_ports': 'list[VersionedPort]',
        'output_ports': 'list[VersionedPort]',
        'connections': 'list[VersionedConnection]',
        'labels': 'list[VersionedLabel]',
        'funnels': 'list[VersionedFunnel]',
        'controller_services': 'list[VersionedControllerService]',
        'versioned_flow_coordinates': 'VersionedFlowCoordinates',
        'variables': 'dict(str, str)',
        'parameter_context_name': 'str',
        'default_flow_file_expiration': 'str',
        'default_back_pressure_object_threshold': 'int',
        'default_back_pressure_data_size_threshold': 'str',
        'log_file_suffix': 'str',
        'flow_file_concurrency': 'str',
        'flow_file_outbound_policy': 'str',
        'component_type': 'str',
        'group_identifier': 'str'
    }

    attribute_map = {
        'identifier': 'identifier',
        'instance_identifier': 'instanceIdentifier',
        'name': 'name',
        'comments': 'comments',
        'position': 'position',
        'process_groups': 'processGroups',
        'remote_process_groups': 'remoteProcessGroups',
        'processors': 'processors',
        'input_ports': 'inputPorts',
        'output_ports': 'outputPorts',
        'connections': 'connections',
        'labels': 'labels',
        'funnels': 'funnels',
        'controller_services': 'controllerServices',
        'versioned_flow_coordinates': 'versionedFlowCoordinates',
        'variables': 'variables',
        'parameter_context_name': 'parameterContextName',
        'default_flow_file_expiration': 'defaultFlowFileExpiration',
        'default_back_pressure_object_threshold': 'defaultBackPressureObjectThreshold',
        'default_back_pressure_data_size_threshold': 'defaultBackPressureDataSizeThreshold',
        'log_file_suffix': 'logFileSuffix',
        'flow_file_concurrency': 'flowFileConcurrency',
        'flow_file_outbound_policy': 'flowFileOutboundPolicy',
        'component_type': 'componentType',
        'group_identifier': 'groupIdentifier'
    }

    def __init__(self, identifier=None, instance_identifier=None, name=None, comments=None, position=None, process_groups=None, remote_process_groups=None, processors=None, input_ports=None, output_ports=None, connections=None, labels=None, funnels=None, controller_services=None, versioned_flow_coordinates=None, variables=None, parameter_context_name=None, default_flow_file_expiration=None, default_back_pressure_object_threshold=None, default_back_pressure_data_size_threshold=None, log_file_suffix=None, flow_file_concurrency=None, flow_file_outbound_policy=None, component_type=None, group_identifier=None):
        """
        VersionedProcessGroup - a model defined in Swagger
        """

        self._identifier = None
        self._instance_identifier = None
        self._name = None
        self._comments = None
        self._position = None
        self._process_groups = None
        self._remote_process_groups = None
        self._processors = None
        self._input_ports = None
        self._output_ports = None
        self._connections = None
        self._labels = None
        self._funnels = None
        self._controller_services = None
        self._versioned_flow_coordinates = None
        self._variables = None
        self._parameter_context_name = None
        self._default_flow_file_expiration = None
        self._default_back_pressure_object_threshold = None
        self._default_back_pressure_data_size_threshold = None
        self._log_file_suffix = None
        self._flow_file_concurrency = None
        self._flow_file_outbound_policy = None
        self._component_type = None
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
        if process_groups is not None:
          self.process_groups = process_groups
        if remote_process_groups is not None:
          self.remote_process_groups = remote_process_groups
        if processors is not None:
          self.processors = processors
        if input_ports is not None:
          self.input_ports = input_ports
        if output_ports is not None:
          self.output_ports = output_ports
        if connections is not None:
          self.connections = connections
        if labels is not None:
          self.labels = labels
        if funnels is not None:
          self.funnels = funnels
        if controller_services is not None:
          self.controller_services = controller_services
        if versioned_flow_coordinates is not None:
          self.versioned_flow_coordinates = versioned_flow_coordinates
        if variables is not None:
          self.variables = variables
        if parameter_context_name is not None:
          self.parameter_context_name = parameter_context_name
        if default_flow_file_expiration is not None:
          self.default_flow_file_expiration = default_flow_file_expiration
        if default_back_pressure_object_threshold is not None:
          self.default_back_pressure_object_threshold = default_back_pressure_object_threshold
        if default_back_pressure_data_size_threshold is not None:
          self.default_back_pressure_data_size_threshold = default_back_pressure_data_size_threshold
        if log_file_suffix is not None:
          self.log_file_suffix = log_file_suffix
        if flow_file_concurrency is not None:
          self.flow_file_concurrency = flow_file_concurrency
        if flow_file_outbound_policy is not None:
          self.flow_file_outbound_policy = flow_file_outbound_policy
        if component_type is not None:
          self.component_type = component_type
        if group_identifier is not None:
          self.group_identifier = group_identifier

    @property
    def identifier(self):
        """
        Gets the identifier of this VersionedProcessGroup.
        The component's unique identifier

        :return: The identifier of this VersionedProcessGroup.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this VersionedProcessGroup.
        The component's unique identifier

        :param identifier: The identifier of this VersionedProcessGroup.
        :type: str
        """

        self._identifier = identifier

    @property
    def instance_identifier(self):
        """
        Gets the instance_identifier of this VersionedProcessGroup.
        The instance ID of an existing component that is described by this VersionedComponent, or null if this is not mapped to an instantiated component

        :return: The instance_identifier of this VersionedProcessGroup.
        :rtype: str
        """
        return self._instance_identifier

    @instance_identifier.setter
    def instance_identifier(self, instance_identifier):
        """
        Sets the instance_identifier of this VersionedProcessGroup.
        The instance ID of an existing component that is described by this VersionedComponent, or null if this is not mapped to an instantiated component

        :param instance_identifier: The instance_identifier of this VersionedProcessGroup.
        :type: str
        """

        self._instance_identifier = instance_identifier

    @property
    def name(self):
        """
        Gets the name of this VersionedProcessGroup.
        The component's name

        :return: The name of this VersionedProcessGroup.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this VersionedProcessGroup.
        The component's name

        :param name: The name of this VersionedProcessGroup.
        :type: str
        """

        self._name = name

    @property
    def comments(self):
        """
        Gets the comments of this VersionedProcessGroup.
        The user-supplied comments for the component

        :return: The comments of this VersionedProcessGroup.
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """
        Sets the comments of this VersionedProcessGroup.
        The user-supplied comments for the component

        :param comments: The comments of this VersionedProcessGroup.
        :type: str
        """

        self._comments = comments

    @property
    def position(self):
        """
        Gets the position of this VersionedProcessGroup.
        The component's position on the graph

        :return: The position of this VersionedProcessGroup.
        :rtype: Position
        """
        return self._position

    @position.setter
    def position(self, position):
        """
        Sets the position of this VersionedProcessGroup.
        The component's position on the graph

        :param position: The position of this VersionedProcessGroup.
        :type: Position
        """

        self._position = position

    @property
    def process_groups(self):
        """
        Gets the process_groups of this VersionedProcessGroup.
        The child Process Groups

        :return: The process_groups of this VersionedProcessGroup.
        :rtype: list[VersionedProcessGroup]
        """
        return self._process_groups

    @process_groups.setter
    def process_groups(self, process_groups):
        """
        Sets the process_groups of this VersionedProcessGroup.
        The child Process Groups

        :param process_groups: The process_groups of this VersionedProcessGroup.
        :type: list[VersionedProcessGroup]
        """

        self._process_groups = process_groups

    @property
    def remote_process_groups(self):
        """
        Gets the remote_process_groups of this VersionedProcessGroup.
        The Remote Process Groups

        :return: The remote_process_groups of this VersionedProcessGroup.
        :rtype: list[VersionedRemoteProcessGroup]
        """
        return self._remote_process_groups

    @remote_process_groups.setter
    def remote_process_groups(self, remote_process_groups):
        """
        Sets the remote_process_groups of this VersionedProcessGroup.
        The Remote Process Groups

        :param remote_process_groups: The remote_process_groups of this VersionedProcessGroup.
        :type: list[VersionedRemoteProcessGroup]
        """

        self._remote_process_groups = remote_process_groups

    @property
    def processors(self):
        """
        Gets the processors of this VersionedProcessGroup.
        The Processors

        :return: The processors of this VersionedProcessGroup.
        :rtype: list[VersionedProcessor]
        """
        return self._processors

    @processors.setter
    def processors(self, processors):
        """
        Sets the processors of this VersionedProcessGroup.
        The Processors

        :param processors: The processors of this VersionedProcessGroup.
        :type: list[VersionedProcessor]
        """

        self._processors = processors

    @property
    def input_ports(self):
        """
        Gets the input_ports of this VersionedProcessGroup.
        The Input Ports

        :return: The input_ports of this VersionedProcessGroup.
        :rtype: list[VersionedPort]
        """
        return self._input_ports

    @input_ports.setter
    def input_ports(self, input_ports):
        """
        Sets the input_ports of this VersionedProcessGroup.
        The Input Ports

        :param input_ports: The input_ports of this VersionedProcessGroup.
        :type: list[VersionedPort]
        """

        self._input_ports = input_ports

    @property
    def output_ports(self):
        """
        Gets the output_ports of this VersionedProcessGroup.
        The Output Ports

        :return: The output_ports of this VersionedProcessGroup.
        :rtype: list[VersionedPort]
        """
        return self._output_ports

    @output_ports.setter
    def output_ports(self, output_ports):
        """
        Sets the output_ports of this VersionedProcessGroup.
        The Output Ports

        :param output_ports: The output_ports of this VersionedProcessGroup.
        :type: list[VersionedPort]
        """

        self._output_ports = output_ports

    @property
    def connections(self):
        """
        Gets the connections of this VersionedProcessGroup.
        The Connections

        :return: The connections of this VersionedProcessGroup.
        :rtype: list[VersionedConnection]
        """
        return self._connections

    @connections.setter
    def connections(self, connections):
        """
        Sets the connections of this VersionedProcessGroup.
        The Connections

        :param connections: The connections of this VersionedProcessGroup.
        :type: list[VersionedConnection]
        """

        self._connections = connections

    @property
    def labels(self):
        """
        Gets the labels of this VersionedProcessGroup.
        The Labels

        :return: The labels of this VersionedProcessGroup.
        :rtype: list[VersionedLabel]
        """
        return self._labels

    @labels.setter
    def labels(self, labels):
        """
        Sets the labels of this VersionedProcessGroup.
        The Labels

        :param labels: The labels of this VersionedProcessGroup.
        :type: list[VersionedLabel]
        """

        self._labels = labels

    @property
    def funnels(self):
        """
        Gets the funnels of this VersionedProcessGroup.
        The Funnels

        :return: The funnels of this VersionedProcessGroup.
        :rtype: list[VersionedFunnel]
        """
        return self._funnels

    @funnels.setter
    def funnels(self, funnels):
        """
        Sets the funnels of this VersionedProcessGroup.
        The Funnels

        :param funnels: The funnels of this VersionedProcessGroup.
        :type: list[VersionedFunnel]
        """

        self._funnels = funnels

    @property
    def controller_services(self):
        """
        Gets the controller_services of this VersionedProcessGroup.
        The Controller Services

        :return: The controller_services of this VersionedProcessGroup.
        :rtype: list[VersionedControllerService]
        """
        return self._controller_services

    @controller_services.setter
    def controller_services(self, controller_services):
        """
        Sets the controller_services of this VersionedProcessGroup.
        The Controller Services

        :param controller_services: The controller_services of this VersionedProcessGroup.
        :type: list[VersionedControllerService]
        """

        self._controller_services = controller_services

    @property
    def versioned_flow_coordinates(self):
        """
        Gets the versioned_flow_coordinates of this VersionedProcessGroup.
        The coordinates where the remote flow is stored, or null if the Process Group is not directly under Version Control

        :return: The versioned_flow_coordinates of this VersionedProcessGroup.
        :rtype: VersionedFlowCoordinates
        """
        return self._versioned_flow_coordinates

    @versioned_flow_coordinates.setter
    def versioned_flow_coordinates(self, versioned_flow_coordinates):
        """
        Sets the versioned_flow_coordinates of this VersionedProcessGroup.
        The coordinates where the remote flow is stored, or null if the Process Group is not directly under Version Control

        :param versioned_flow_coordinates: The versioned_flow_coordinates of this VersionedProcessGroup.
        :type: VersionedFlowCoordinates
        """

        self._versioned_flow_coordinates = versioned_flow_coordinates

    @property
    def variables(self):
        """
        Gets the variables of this VersionedProcessGroup.
        The Variables in the Variable Registry for this Process Group (not including any ancestor or descendant Process Groups)

        :return: The variables of this VersionedProcessGroup.
        :rtype: dict(str, str)
        """
        return self._variables

    @variables.setter
    def variables(self, variables):
        """
        Sets the variables of this VersionedProcessGroup.
        The Variables in the Variable Registry for this Process Group (not including any ancestor or descendant Process Groups)

        :param variables: The variables of this VersionedProcessGroup.
        :type: dict(str, str)
        """

        self._variables = variables

    @property
    def parameter_context_name(self):
        """
        Gets the parameter_context_name of this VersionedProcessGroup.
        The name of the parameter context used by this process group

        :return: The parameter_context_name of this VersionedProcessGroup.
        :rtype: str
        """
        return self._parameter_context_name

    @parameter_context_name.setter
    def parameter_context_name(self, parameter_context_name):
        """
        Sets the parameter_context_name of this VersionedProcessGroup.
        The name of the parameter context used by this process group

        :param parameter_context_name: The parameter_context_name of this VersionedProcessGroup.
        :type: str
        """

        self._parameter_context_name = parameter_context_name

    @property
    def default_flow_file_expiration(self):
        """
        Gets the default_flow_file_expiration of this VersionedProcessGroup.
        The default FlowFile Expiration for this Process Group.

        :return: The default_flow_file_expiration of this VersionedProcessGroup.
        :rtype: str
        """
        return self._default_flow_file_expiration

    @default_flow_file_expiration.setter
    def default_flow_file_expiration(self, default_flow_file_expiration):
        """
        Sets the default_flow_file_expiration of this VersionedProcessGroup.
        The default FlowFile Expiration for this Process Group.

        :param default_flow_file_expiration: The default_flow_file_expiration of this VersionedProcessGroup.
        :type: str
        """

        self._default_flow_file_expiration = default_flow_file_expiration

    @property
    def default_back_pressure_object_threshold(self):
        """
        Gets the default_back_pressure_object_threshold of this VersionedProcessGroup.
        Default value used in this Process Group for the maximum number of objects that can be queued before back pressure is applied.

        :return: The default_back_pressure_object_threshold of this VersionedProcessGroup.
        :rtype: int
        """
        return self._default_back_pressure_object_threshold

    @default_back_pressure_object_threshold.setter
    def default_back_pressure_object_threshold(self, default_back_pressure_object_threshold):
        """
        Sets the default_back_pressure_object_threshold of this VersionedProcessGroup.
        Default value used in this Process Group for the maximum number of objects that can be queued before back pressure is applied.

        :param default_back_pressure_object_threshold: The default_back_pressure_object_threshold of this VersionedProcessGroup.
        :type: int
        """

        self._default_back_pressure_object_threshold = default_back_pressure_object_threshold

    @property
    def default_back_pressure_data_size_threshold(self):
        """
        Gets the default_back_pressure_data_size_threshold of this VersionedProcessGroup.
        Default value used in this Process Group for the maximum data size of objects that can be queued before back pressure is applied.

        :return: The default_back_pressure_data_size_threshold of this VersionedProcessGroup.
        :rtype: str
        """
        return self._default_back_pressure_data_size_threshold

    @default_back_pressure_data_size_threshold.setter
    def default_back_pressure_data_size_threshold(self, default_back_pressure_data_size_threshold):
        """
        Sets the default_back_pressure_data_size_threshold of this VersionedProcessGroup.
        Default value used in this Process Group for the maximum data size of objects that can be queued before back pressure is applied.

        :param default_back_pressure_data_size_threshold: The default_back_pressure_data_size_threshold of this VersionedProcessGroup.
        :type: str
        """

        self._default_back_pressure_data_size_threshold = default_back_pressure_data_size_threshold

    @property
    def log_file_suffix(self):
        """
        Gets the log_file_suffix of this VersionedProcessGroup.
        The log file suffix for this Process Group for dedicated logging.

        :return: The log_file_suffix of this VersionedProcessGroup.
        :rtype: str
        """
        return self._log_file_suffix

    @log_file_suffix.setter
    def log_file_suffix(self, log_file_suffix):
        """
        Sets the log_file_suffix of this VersionedProcessGroup.
        The log file suffix for this Process Group for dedicated logging.

        :param log_file_suffix: The log_file_suffix of this VersionedProcessGroup.
        :type: str
        """

        self._log_file_suffix = log_file_suffix

    @property
    def flow_file_concurrency(self):
        """
        Gets the flow_file_concurrency of this VersionedProcessGroup.
        The configured FlowFile Concurrency for the Process Group

        :return: The flow_file_concurrency of this VersionedProcessGroup.
        :rtype: str
        """
        return self._flow_file_concurrency

    @flow_file_concurrency.setter
    def flow_file_concurrency(self, flow_file_concurrency):
        """
        Sets the flow_file_concurrency of this VersionedProcessGroup.
        The configured FlowFile Concurrency for the Process Group

        :param flow_file_concurrency: The flow_file_concurrency of this VersionedProcessGroup.
        :type: str
        """

        self._flow_file_concurrency = flow_file_concurrency

    @property
    def flow_file_outbound_policy(self):
        """
        Gets the flow_file_outbound_policy of this VersionedProcessGroup.
        The FlowFile Outbound Policy for the Process Group

        :return: The flow_file_outbound_policy of this VersionedProcessGroup.
        :rtype: str
        """
        return self._flow_file_outbound_policy

    @flow_file_outbound_policy.setter
    def flow_file_outbound_policy(self, flow_file_outbound_policy):
        """
        Sets the flow_file_outbound_policy of this VersionedProcessGroup.
        The FlowFile Outbound Policy for the Process Group

        :param flow_file_outbound_policy: The flow_file_outbound_policy of this VersionedProcessGroup.
        :type: str
        """

        self._flow_file_outbound_policy = flow_file_outbound_policy

    @property
    def component_type(self):
        """
        Gets the component_type of this VersionedProcessGroup.

        :return: The component_type of this VersionedProcessGroup.
        :rtype: str
        """
        return self._component_type

    @component_type.setter
    def component_type(self, component_type):
        """
        Sets the component_type of this VersionedProcessGroup.

        :param component_type: The component_type of this VersionedProcessGroup.
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
    def group_identifier(self):
        """
        Gets the group_identifier of this VersionedProcessGroup.
        The ID of the Process Group that this component belongs to

        :return: The group_identifier of this VersionedProcessGroup.
        :rtype: str
        """
        return self._group_identifier

    @group_identifier.setter
    def group_identifier(self, group_identifier):
        """
        Sets the group_identifier of this VersionedProcessGroup.
        The ID of the Process Group that this component belongs to

        :param group_identifier: The group_identifier of this VersionedProcessGroup.
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
        if not isinstance(other, VersionedProcessGroup):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
