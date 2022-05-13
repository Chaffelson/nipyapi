# coding: utf-8

"""
    Apache NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 1.16.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class VersionedControllerService(object):
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
        'type': 'str',
        'bundle': 'Bundle',
        'properties': 'dict(str, str)',
        'property_descriptors': 'dict(str, VersionedPropertyDescriptor)',
        'controller_service_apis': 'list[ControllerServiceAPI]',
        'annotation_data': 'str',
        'scheduled_state': 'str',
        'component_type': 'str',
        'group_identifier': 'str'
    }

    attribute_map = {
        'identifier': 'identifier',
        'instance_identifier': 'instanceIdentifier',
        'name': 'name',
        'comments': 'comments',
        'position': 'position',
        'type': 'type',
        'bundle': 'bundle',
        'properties': 'properties',
        'property_descriptors': 'propertyDescriptors',
        'controller_service_apis': 'controllerServiceApis',
        'annotation_data': 'annotationData',
        'scheduled_state': 'scheduledState',
        'component_type': 'componentType',
        'group_identifier': 'groupIdentifier'
    }

    def __init__(self, identifier=None, instance_identifier=None, name=None, comments=None, position=None, type=None, bundle=None, properties=None, property_descriptors=None, controller_service_apis=None, annotation_data=None, scheduled_state=None, component_type=None, group_identifier=None):
        """
        VersionedControllerService - a model defined in Swagger
        """

        self._identifier = None
        self._instance_identifier = None
        self._name = None
        self._comments = None
        self._position = None
        self._type = None
        self._bundle = None
        self._properties = None
        self._property_descriptors = None
        self._controller_service_apis = None
        self._annotation_data = None
        self._scheduled_state = None
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
        if type is not None:
          self.type = type
        if bundle is not None:
          self.bundle = bundle
        if properties is not None:
          self.properties = properties
        if property_descriptors is not None:
          self.property_descriptors = property_descriptors
        if controller_service_apis is not None:
          self.controller_service_apis = controller_service_apis
        if annotation_data is not None:
          self.annotation_data = annotation_data
        if scheduled_state is not None:
          self.scheduled_state = scheduled_state
        if component_type is not None:
          self.component_type = component_type
        if group_identifier is not None:
          self.group_identifier = group_identifier

    @property
    def identifier(self):
        """
        Gets the identifier of this VersionedControllerService.
        The component's unique identifier

        :return: The identifier of this VersionedControllerService.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this VersionedControllerService.
        The component's unique identifier

        :param identifier: The identifier of this VersionedControllerService.
        :type: str
        """

        self._identifier = identifier

    @property
    def instance_identifier(self):
        """
        Gets the instance_identifier of this VersionedControllerService.
        The instance ID of an existing component that is described by this VersionedComponent, or null if this is not mapped to an instantiated component

        :return: The instance_identifier of this VersionedControllerService.
        :rtype: str
        """
        return self._instance_identifier

    @instance_identifier.setter
    def instance_identifier(self, instance_identifier):
        """
        Sets the instance_identifier of this VersionedControllerService.
        The instance ID of an existing component that is described by this VersionedComponent, or null if this is not mapped to an instantiated component

        :param instance_identifier: The instance_identifier of this VersionedControllerService.
        :type: str
        """

        self._instance_identifier = instance_identifier

    @property
    def name(self):
        """
        Gets the name of this VersionedControllerService.
        The component's name

        :return: The name of this VersionedControllerService.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this VersionedControllerService.
        The component's name

        :param name: The name of this VersionedControllerService.
        :type: str
        """

        self._name = name

    @property
    def comments(self):
        """
        Gets the comments of this VersionedControllerService.
        The user-supplied comments for the component

        :return: The comments of this VersionedControllerService.
        :rtype: str
        """
        return self._comments

    @comments.setter
    def comments(self, comments):
        """
        Sets the comments of this VersionedControllerService.
        The user-supplied comments for the component

        :param comments: The comments of this VersionedControllerService.
        :type: str
        """

        self._comments = comments

    @property
    def position(self):
        """
        Gets the position of this VersionedControllerService.
        The component's position on the graph

        :return: The position of this VersionedControllerService.
        :rtype: Position
        """
        return self._position

    @position.setter
    def position(self, position):
        """
        Sets the position of this VersionedControllerService.
        The component's position on the graph

        :param position: The position of this VersionedControllerService.
        :type: Position
        """

        self._position = position

    @property
    def type(self):
        """
        Gets the type of this VersionedControllerService.
        The type of the extension component

        :return: The type of this VersionedControllerService.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this VersionedControllerService.
        The type of the extension component

        :param type: The type of this VersionedControllerService.
        :type: str
        """

        self._type = type

    @property
    def bundle(self):
        """
        Gets the bundle of this VersionedControllerService.
        Information about the bundle from which the component came

        :return: The bundle of this VersionedControllerService.
        :rtype: Bundle
        """
        return self._bundle

    @bundle.setter
    def bundle(self, bundle):
        """
        Sets the bundle of this VersionedControllerService.
        Information about the bundle from which the component came

        :param bundle: The bundle of this VersionedControllerService.
        :type: Bundle
        """

        self._bundle = bundle

    @property
    def properties(self):
        """
        Gets the properties of this VersionedControllerService.
        The properties for the component. Properties whose value is not set will only contain the property name.

        :return: The properties of this VersionedControllerService.
        :rtype: dict(str, str)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this VersionedControllerService.
        The properties for the component. Properties whose value is not set will only contain the property name.

        :param properties: The properties of this VersionedControllerService.
        :type: dict(str, str)
        """

        self._properties = properties

    @property
    def property_descriptors(self):
        """
        Gets the property_descriptors of this VersionedControllerService.
        The property descriptors for the component.

        :return: The property_descriptors of this VersionedControllerService.
        :rtype: dict(str, VersionedPropertyDescriptor)
        """
        return self._property_descriptors

    @property_descriptors.setter
    def property_descriptors(self, property_descriptors):
        """
        Sets the property_descriptors of this VersionedControllerService.
        The property descriptors for the component.

        :param property_descriptors: The property_descriptors of this VersionedControllerService.
        :type: dict(str, VersionedPropertyDescriptor)
        """

        self._property_descriptors = property_descriptors

    @property
    def controller_service_apis(self):
        """
        Gets the controller_service_apis of this VersionedControllerService.
        Lists the APIs this Controller Service implements.

        :return: The controller_service_apis of this VersionedControllerService.
        :rtype: list[ControllerServiceAPI]
        """
        return self._controller_service_apis

    @controller_service_apis.setter
    def controller_service_apis(self, controller_service_apis):
        """
        Sets the controller_service_apis of this VersionedControllerService.
        Lists the APIs this Controller Service implements.

        :param controller_service_apis: The controller_service_apis of this VersionedControllerService.
        :type: list[ControllerServiceAPI]
        """

        self._controller_service_apis = controller_service_apis

    @property
    def annotation_data(self):
        """
        Gets the annotation_data of this VersionedControllerService.
        The annotation for the controller service. This is how the custom UI relays configuration to the controller service.

        :return: The annotation_data of this VersionedControllerService.
        :rtype: str
        """
        return self._annotation_data

    @annotation_data.setter
    def annotation_data(self, annotation_data):
        """
        Sets the annotation_data of this VersionedControllerService.
        The annotation for the controller service. This is how the custom UI relays configuration to the controller service.

        :param annotation_data: The annotation_data of this VersionedControllerService.
        :type: str
        """

        self._annotation_data = annotation_data

    @property
    def scheduled_state(self):
        """
        Gets the scheduled_state of this VersionedControllerService.
        The ScheduledState denoting whether the Controller Service is ENABLED or DISABLED

        :return: The scheduled_state of this VersionedControllerService.
        :rtype: str
        """
        return self._scheduled_state

    @scheduled_state.setter
    def scheduled_state(self, scheduled_state):
        """
        Sets the scheduled_state of this VersionedControllerService.
        The ScheduledState denoting whether the Controller Service is ENABLED or DISABLED

        :param scheduled_state: The scheduled_state of this VersionedControllerService.
        :type: str
        """
        allowed_values = ["ENABLED", "DISABLED", "RUNNING"]
        if scheduled_state not in allowed_values:
            raise ValueError(
                "Invalid value for `scheduled_state` ({0}), must be one of {1}"
                .format(scheduled_state, allowed_values)
            )

        self._scheduled_state = scheduled_state

    @property
    def component_type(self):
        """
        Gets the component_type of this VersionedControllerService.

        :return: The component_type of this VersionedControllerService.
        :rtype: str
        """
        return self._component_type

    @component_type.setter
    def component_type(self, component_type):
        """
        Sets the component_type of this VersionedControllerService.

        :param component_type: The component_type of this VersionedControllerService.
        :type: str
        """
        allowed_values = ["CONNECTION", "PROCESSOR", "PROCESS_GROUP", "REMOTE_PROCESS_GROUP", "INPUT_PORT", "OUTPUT_PORT", "REMOTE_INPUT_PORT", "REMOTE_OUTPUT_PORT", "FUNNEL", "LABEL", "CONTROLLER_SERVICE", "REPORTING_TASK", "PARAMETER_CONTEXT", "TEMPLATE"]
        if component_type not in allowed_values:
            raise ValueError(
                "Invalid value for `component_type` ({0}), must be one of {1}"
                .format(component_type, allowed_values)
            )

        self._component_type = component_type

    @property
    def group_identifier(self):
        """
        Gets the group_identifier of this VersionedControllerService.
        The ID of the Process Group that this component belongs to

        :return: The group_identifier of this VersionedControllerService.
        :rtype: str
        """
        return self._group_identifier

    @group_identifier.setter
    def group_identifier(self, group_identifier):
        """
        Sets the group_identifier of this VersionedControllerService.
        The ID of the Process Group that this component belongs to

        :param group_identifier: The group_identifier of this VersionedControllerService.
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
        if not isinstance(other, VersionedControllerService):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
