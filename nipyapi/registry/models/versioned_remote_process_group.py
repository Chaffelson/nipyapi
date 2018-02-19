# coding: utf-8

"""
    NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 0.2.0-SNAPSHOT
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class VersionedRemoteProcessGroup(object):
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
        'position': 'ThePositionOfAComponentOnTheGraph',
        'target_uri': 'str',
        'target_uris': 'str',
        'communications_timeout': 'str',
        'yield_duration': 'str',
        'transport_protocol': 'str',
        'local_network_interface': 'str',
        'proxy_host': 'str',
        'proxy_port': 'int',
        'proxy_user': 'str',
        'input_ports': 'list[VersionedRemoteGroupPort]',
        'output_ports': 'list[VersionedRemoteGroupPort]',
        'component_type': 'str',
        'group_identifier': 'str'
    }

    attribute_map = {
        'identifier': 'identifier',
        'name': 'name',
        'comments': 'comments',
        'position': 'position',
        'target_uri': 'targetUri',
        'target_uris': 'targetUris',
        'communications_timeout': 'communicationsTimeout',
        'yield_duration': 'yieldDuration',
        'transport_protocol': 'transportProtocol',
        'local_network_interface': 'localNetworkInterface',
        'proxy_host': 'proxyHost',
        'proxy_port': 'proxyPort',
        'proxy_user': 'proxyUser',
        'input_ports': 'inputPorts',
        'output_ports': 'outputPorts',
        'component_type': 'componentType',
        'group_identifier': 'groupIdentifier'
    }

    def __init__(self, identifier=None, name=None, comments=None, position=None, target_uri=None, target_uris=None, communications_timeout=None, yield_duration=None, transport_protocol=None, local_network_interface=None, proxy_host=None, proxy_port=None, proxy_user=None, input_ports=None, output_ports=None, component_type=None, group_identifier=None):
        """
        VersionedRemoteProcessGroup - a model defined in Swagger
        """

        self._identifier = None
        self._name = None
        self._comments = None
        self._position = None
        self._target_uri = None
        self._target_uris = None
        self._communications_timeout = None
        self._yield_duration = None
        self._transport_protocol = None
        self._local_network_interface = None
        self._proxy_host = None
        self._proxy_port = None
        self._proxy_user = None
        self._input_ports = None
        self._output_ports = None
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
        if target_uri is not None:
          self.target_uri = target_uri
        if target_uris is not None:
          self.target_uris = target_uris
        if communications_timeout is not None:
          self.communications_timeout = communications_timeout
        if yield_duration is not None:
          self.yield_duration = yield_duration
        if transport_protocol is not None:
          self.transport_protocol = transport_protocol
        if local_network_interface is not None:
          self.local_network_interface = local_network_interface
        if proxy_host is not None:
          self.proxy_host = proxy_host
        if proxy_port is not None:
          self.proxy_port = proxy_port
        if proxy_user is not None:
          self.proxy_user = proxy_user
        if input_ports is not None:
          self.input_ports = input_ports
        if output_ports is not None:
          self.output_ports = output_ports
        if component_type is not None:
          self.component_type = component_type
        if group_identifier is not None:
          self.group_identifier = group_identifier

    @property
    def identifier(self):
        """
        Gets the identifier of this VersionedRemoteProcessGroup.
        The component's unique identifier

        :return: The identifier of this VersionedRemoteProcessGroup.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this VersionedRemoteProcessGroup.
        The component's unique identifier

        :param identifier: The identifier of this VersionedRemoteProcessGroup.
        :type: str
        """

        self._identifier = identifier

    @property
    def name(self):
        """
        Gets the name of this VersionedRemoteProcessGroup.
        The component's name

        :return: The name of this VersionedRemoteProcessGroup.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this VersionedRemoteProcessGroup.
        The component's name

        :param name: The name of this VersionedRemoteProcessGroup.
        :type: str
        """

        self._name = name

    @property
    def comments(self):
        """
        Gets the comments of this VersionedRemoteProcessGroup.
        The user-supplied comments for the component

        :return: The comments of this VersionedRemoteProcessGroup.
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """
        Sets the comments of this VersionedRemoteProcessGroup.
        The user-supplied comments for the component

        :param comments: The comments of this VersionedRemoteProcessGroup.
        :type: str
        """

        self._comments = comments

    @property
    def position(self):
        """
        Gets the position of this VersionedRemoteProcessGroup.
        The component's position on the graph

        :return: The position of this VersionedRemoteProcessGroup.
        :rtype: ThePositionOfAComponentOnTheGraph
        """
        return self._position

    @position.setter
    def position(self, position):
        """
        Sets the position of this VersionedRemoteProcessGroup.
        The component's position on the graph

        :param position: The position of this VersionedRemoteProcessGroup.
        :type: ThePositionOfAComponentOnTheGraph
        """

        self._position = position

    @property
    def target_uri(self):
        """
        Gets the target_uri of this VersionedRemoteProcessGroup.
        The target URI of the remote process group. If target uri is not set, but uris are set, then returns the first url in the urls. If neither target uri nor uris are set, then returns null.

        :return: The target_uri of this VersionedRemoteProcessGroup.
        :rtype: str
        """
        return self._target_uri

    @target_uri.setter
    def target_uri(self, target_uri):
        """
        Sets the target_uri of this VersionedRemoteProcessGroup.
        The target URI of the remote process group. If target uri is not set, but uris are set, then returns the first url in the urls. If neither target uri nor uris are set, then returns null.

        :param target_uri: The target_uri of this VersionedRemoteProcessGroup.
        :type: str
        """

        self._target_uri = target_uri

    @property
    def target_uris(self):
        """
        Gets the target_uris of this VersionedRemoteProcessGroup.
        The target URI of the remote process group. If target uris is not set but target uri is set, then returns the single target uri. If neither target uris nor target uri is set, then returns null.

        :return: The target_uris of this VersionedRemoteProcessGroup.
        :rtype: str
        """
        return self._target_uris

    @target_uris.setter
    def target_uris(self, target_uris):
        """
        Sets the target_uris of this VersionedRemoteProcessGroup.
        The target URI of the remote process group. If target uris is not set but target uri is set, then returns the single target uri. If neither target uris nor target uri is set, then returns null.

        :param target_uris: The target_uris of this VersionedRemoteProcessGroup.
        :type: str
        """

        self._target_uris = target_uris

    @property
    def communications_timeout(self):
        """
        Gets the communications_timeout of this VersionedRemoteProcessGroup.
        The time period used for the timeout when communicating with the target.

        :return: The communications_timeout of this VersionedRemoteProcessGroup.
        :rtype: str
        """
        return self._communications_timeout

    @communications_timeout.setter
    def communications_timeout(self, communications_timeout):
        """
        Sets the communications_timeout of this VersionedRemoteProcessGroup.
        The time period used for the timeout when communicating with the target.

        :param communications_timeout: The communications_timeout of this VersionedRemoteProcessGroup.
        :type: str
        """

        self._communications_timeout = communications_timeout

    @property
    def yield_duration(self):
        """
        Gets the yield_duration of this VersionedRemoteProcessGroup.
        When yielding, this amount of time must elapse before the remote process group is scheduled again.

        :return: The yield_duration of this VersionedRemoteProcessGroup.
        :rtype: str
        """
        return self._yield_duration

    @yield_duration.setter
    def yield_duration(self, yield_duration):
        """
        Sets the yield_duration of this VersionedRemoteProcessGroup.
        When yielding, this amount of time must elapse before the remote process group is scheduled again.

        :param yield_duration: The yield_duration of this VersionedRemoteProcessGroup.
        :type: str
        """

        self._yield_duration = yield_duration

    @property
    def transport_protocol(self):
        """
        Gets the transport_protocol of this VersionedRemoteProcessGroup.
        The Transport Protocol that is used for Site-to-Site communications

        :return: The transport_protocol of this VersionedRemoteProcessGroup.
        :rtype: str
        """
        return self._transport_protocol

    @transport_protocol.setter
    def transport_protocol(self, transport_protocol):
        """
        Sets the transport_protocol of this VersionedRemoteProcessGroup.
        The Transport Protocol that is used for Site-to-Site communications

        :param transport_protocol: The transport_protocol of this VersionedRemoteProcessGroup.
        :type: str
        """
        allowed_values = ["RAW", "HTTP"]
        if transport_protocol not in allowed_values:
            raise ValueError(
                "Invalid value for `transport_protocol` ({0}), must be one of {1}"
                .format(transport_protocol, allowed_values)
            )

        self._transport_protocol = transport_protocol

    @property
    def local_network_interface(self):
        """
        Gets the local_network_interface of this VersionedRemoteProcessGroup.
        The local network interface to send/receive data. If not specified, any local address is used. If clustered, all nodes must have an interface with this identifier.

        :return: The local_network_interface of this VersionedRemoteProcessGroup.
        :rtype: str
        """
        return self._local_network_interface

    @local_network_interface.setter
    def local_network_interface(self, local_network_interface):
        """
        Sets the local_network_interface of this VersionedRemoteProcessGroup.
        The local network interface to send/receive data. If not specified, any local address is used. If clustered, all nodes must have an interface with this identifier.

        :param local_network_interface: The local_network_interface of this VersionedRemoteProcessGroup.
        :type: str
        """

        self._local_network_interface = local_network_interface

    @property
    def proxy_host(self):
        """
        Gets the proxy_host of this VersionedRemoteProcessGroup.

        :return: The proxy_host of this VersionedRemoteProcessGroup.
        :rtype: str
        """
        return self._proxy_host

    @proxy_host.setter
    def proxy_host(self, proxy_host):
        """
        Sets the proxy_host of this VersionedRemoteProcessGroup.

        :param proxy_host: The proxy_host of this VersionedRemoteProcessGroup.
        :type: str
        """

        self._proxy_host = proxy_host

    @property
    def proxy_port(self):
        """
        Gets the proxy_port of this VersionedRemoteProcessGroup.

        :return: The proxy_port of this VersionedRemoteProcessGroup.
        :rtype: int
        """
        return self._proxy_port

    @proxy_port.setter
    def proxy_port(self, proxy_port):
        """
        Sets the proxy_port of this VersionedRemoteProcessGroup.

        :param proxy_port: The proxy_port of this VersionedRemoteProcessGroup.
        :type: int
        """

        self._proxy_port = proxy_port

    @property
    def proxy_user(self):
        """
        Gets the proxy_user of this VersionedRemoteProcessGroup.

        :return: The proxy_user of this VersionedRemoteProcessGroup.
        :rtype: str
        """
        return self._proxy_user

    @proxy_user.setter
    def proxy_user(self, proxy_user):
        """
        Sets the proxy_user of this VersionedRemoteProcessGroup.

        :param proxy_user: The proxy_user of this VersionedRemoteProcessGroup.
        :type: str
        """

        self._proxy_user = proxy_user

    @property
    def input_ports(self):
        """
        Gets the input_ports of this VersionedRemoteProcessGroup.
        A Set of Input Ports that can be connected to, in order to send data to the remote NiFi instance

        :return: The input_ports of this VersionedRemoteProcessGroup.
        :rtype: list[VersionedRemoteGroupPort]
        """
        return self._input_ports

    @input_ports.setter
    def input_ports(self, input_ports):
        """
        Sets the input_ports of this VersionedRemoteProcessGroup.
        A Set of Input Ports that can be connected to, in order to send data to the remote NiFi instance

        :param input_ports: The input_ports of this VersionedRemoteProcessGroup.
        :type: list[VersionedRemoteGroupPort]
        """

        self._input_ports = input_ports

    @property
    def output_ports(self):
        """
        Gets the output_ports of this VersionedRemoteProcessGroup.
        A Set of Output Ports that can be connected to, in order to pull data from the remote NiFi instance

        :return: The output_ports of this VersionedRemoteProcessGroup.
        :rtype: list[VersionedRemoteGroupPort]
        """
        return self._output_ports

    @output_ports.setter
    def output_ports(self, output_ports):
        """
        Sets the output_ports of this VersionedRemoteProcessGroup.
        A Set of Output Ports that can be connected to, in order to pull data from the remote NiFi instance

        :param output_ports: The output_ports of this VersionedRemoteProcessGroup.
        :type: list[VersionedRemoteGroupPort]
        """

        self._output_ports = output_ports

    @property
    def component_type(self):
        """
        Gets the component_type of this VersionedRemoteProcessGroup.

        :return: The component_type of this VersionedRemoteProcessGroup.
        :rtype: str
        """
        return self._component_type

    @component_type.setter
    def component_type(self, component_type):
        """
        Sets the component_type of this VersionedRemoteProcessGroup.

        :param component_type: The component_type of this VersionedRemoteProcessGroup.
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
        Gets the group_identifier of this VersionedRemoteProcessGroup.
        The ID of the Process Group that this component belongs to

        :return: The group_identifier of this VersionedRemoteProcessGroup.
        :rtype: str
        """
        return self._group_identifier

    @group_identifier.setter
    def group_identifier(self, group_identifier):
        """
        Sets the group_identifier of this VersionedRemoteProcessGroup.
        The ID of the Process Group that this component belongs to

        :param group_identifier: The group_identifier of this VersionedRemoteProcessGroup.
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
        if not isinstance(other, VersionedRemoteProcessGroup):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
