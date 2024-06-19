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


class ControllerServiceReferencingComponentDTO(object):
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
        'group_id': 'str',
        'id': 'str',
        'name': 'str',
        'type': 'str',
        'state': 'str',
        'properties': 'dict(str, str)',
        'descriptors': 'dict(str, PropertyDescriptorDTO)',
        'validation_errors': 'list[str]',
        'reference_type': 'str',
        'active_thread_count': 'int',
        'reference_cycle': 'bool',
        'referencing_components': 'list[ControllerServiceReferencingComponentEntity]'
    }

    attribute_map = {
        'group_id': 'groupId',
        'id': 'id',
        'name': 'name',
        'type': 'type',
        'state': 'state',
        'properties': 'properties',
        'descriptors': 'descriptors',
        'validation_errors': 'validationErrors',
        'reference_type': 'referenceType',
        'active_thread_count': 'activeThreadCount',
        'reference_cycle': 'referenceCycle',
        'referencing_components': 'referencingComponents'
    }

    def __init__(self, group_id=None, id=None, name=None, type=None, state=None, properties=None, descriptors=None, validation_errors=None, reference_type=None, active_thread_count=None, reference_cycle=None, referencing_components=None):
        """
        ControllerServiceReferencingComponentDTO - a model defined in Swagger
        """

        self._group_id = None
        self._id = None
        self._name = None
        self._type = None
        self._state = None
        self._properties = None
        self._descriptors = None
        self._validation_errors = None
        self._reference_type = None
        self._active_thread_count = None
        self._reference_cycle = None
        self._referencing_components = None

        if group_id is not None:
          self.group_id = group_id
        if id is not None:
          self.id = id
        if name is not None:
          self.name = name
        if type is not None:
          self.type = type
        if state is not None:
          self.state = state
        if properties is not None:
          self.properties = properties
        if descriptors is not None:
          self.descriptors = descriptors
        if validation_errors is not None:
          self.validation_errors = validation_errors
        if reference_type is not None:
          self.reference_type = reference_type
        if active_thread_count is not None:
          self.active_thread_count = active_thread_count
        if reference_cycle is not None:
          self.reference_cycle = reference_cycle
        if referencing_components is not None:
          self.referencing_components = referencing_components

    @property
    def group_id(self):
        """
        Gets the group_id of this ControllerServiceReferencingComponentDTO.
        The group id for the component referencing a controller service. If this component is another controller service or a reporting task, this field is blank.

        :return: The group_id of this ControllerServiceReferencingComponentDTO.
        :rtype: str
        """
        return self._group_id

    @group_id.setter
    def group_id(self, group_id):
        """
        Sets the group_id of this ControllerServiceReferencingComponentDTO.
        The group id for the component referencing a controller service. If this component is another controller service or a reporting task, this field is blank.

        :param group_id: The group_id of this ControllerServiceReferencingComponentDTO.
        :type: str
        """

        self._group_id = group_id

    @property
    def id(self):
        """
        Gets the id of this ControllerServiceReferencingComponentDTO.
        The id of the component referencing a controller service.

        :return: The id of this ControllerServiceReferencingComponentDTO.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ControllerServiceReferencingComponentDTO.
        The id of the component referencing a controller service.

        :param id: The id of this ControllerServiceReferencingComponentDTO.
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ControllerServiceReferencingComponentDTO.
        The name of the component referencing a controller service.

        :return: The name of this ControllerServiceReferencingComponentDTO.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ControllerServiceReferencingComponentDTO.
        The name of the component referencing a controller service.

        :param name: The name of this ControllerServiceReferencingComponentDTO.
        :type: str
        """

        self._name = name

    @property
    def type(self):
        """
        Gets the type of this ControllerServiceReferencingComponentDTO.
        The type of the component referencing a controller service in simple Java class name format without package name.

        :return: The type of this ControllerServiceReferencingComponentDTO.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this ControllerServiceReferencingComponentDTO.
        The type of the component referencing a controller service in simple Java class name format without package name.

        :param type: The type of this ControllerServiceReferencingComponentDTO.
        :type: str
        """

        self._type = type

    @property
    def state(self):
        """
        Gets the state of this ControllerServiceReferencingComponentDTO.
        The scheduled state of a processor or reporting task referencing a controller service. If this component is another controller service, this field represents the controller service state.

        :return: The state of this ControllerServiceReferencingComponentDTO.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this ControllerServiceReferencingComponentDTO.
        The scheduled state of a processor or reporting task referencing a controller service. If this component is another controller service, this field represents the controller service state.

        :param state: The state of this ControllerServiceReferencingComponentDTO.
        :type: str
        """

        self._state = state

    @property
    def properties(self):
        """
        Gets the properties of this ControllerServiceReferencingComponentDTO.
        The properties for the component.

        :return: The properties of this ControllerServiceReferencingComponentDTO.
        :rtype: dict(str, str)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this ControllerServiceReferencingComponentDTO.
        The properties for the component.

        :param properties: The properties of this ControllerServiceReferencingComponentDTO.
        :type: dict(str, str)
        """

        self._properties = properties

    @property
    def descriptors(self):
        """
        Gets the descriptors of this ControllerServiceReferencingComponentDTO.
        The descriptors for the component properties.

        :return: The descriptors of this ControllerServiceReferencingComponentDTO.
        :rtype: dict(str, PropertyDescriptorDTO)
        """
        return self._descriptors

    @descriptors.setter
    def descriptors(self, descriptors):
        """
        Sets the descriptors of this ControllerServiceReferencingComponentDTO.
        The descriptors for the component properties.

        :param descriptors: The descriptors of this ControllerServiceReferencingComponentDTO.
        :type: dict(str, PropertyDescriptorDTO)
        """

        self._descriptors = descriptors

    @property
    def validation_errors(self):
        """
        Gets the validation_errors of this ControllerServiceReferencingComponentDTO.
        The validation errors for the component.

        :return: The validation_errors of this ControllerServiceReferencingComponentDTO.
        :rtype: list[str]
        """
        return self._validation_errors

    @validation_errors.setter
    def validation_errors(self, validation_errors):
        """
        Sets the validation_errors of this ControllerServiceReferencingComponentDTO.
        The validation errors for the component.

        :param validation_errors: The validation_errors of this ControllerServiceReferencingComponentDTO.
        :type: list[str]
        """

        self._validation_errors = validation_errors

    @property
    def reference_type(self):
        """
        Gets the reference_type of this ControllerServiceReferencingComponentDTO.
        The type of reference this is.

        :return: The reference_type of this ControllerServiceReferencingComponentDTO.
        :rtype: str
        """
        return self._reference_type

    @reference_type.setter
    def reference_type(self, reference_type):
        """
        Sets the reference_type of this ControllerServiceReferencingComponentDTO.
        The type of reference this is.

        :param reference_type: The reference_type of this ControllerServiceReferencingComponentDTO.
        :type: str
        """
        allowed_values = ["Processor", "ControllerService", "ReportingTask", "FlowRegistryClient"]
        if reference_type not in allowed_values:
            raise ValueError(
                "Invalid value for `reference_type` ({0}), must be one of {1}"
                .format(reference_type, allowed_values)
            )

        self._reference_type = reference_type

    @property
    def active_thread_count(self):
        """
        Gets the active_thread_count of this ControllerServiceReferencingComponentDTO.
        The number of active threads for the referencing component.

        :return: The active_thread_count of this ControllerServiceReferencingComponentDTO.
        :rtype: int
        """
        return self._active_thread_count

    @active_thread_count.setter
    def active_thread_count(self, active_thread_count):
        """
        Sets the active_thread_count of this ControllerServiceReferencingComponentDTO.
        The number of active threads for the referencing component.

        :param active_thread_count: The active_thread_count of this ControllerServiceReferencingComponentDTO.
        :type: int
        """

        self._active_thread_count = active_thread_count

    @property
    def reference_cycle(self):
        """
        Gets the reference_cycle of this ControllerServiceReferencingComponentDTO.
        If the referencing component represents a controller service, this indicates whether it has already been represented in this hierarchy.

        :return: The reference_cycle of this ControllerServiceReferencingComponentDTO.
        :rtype: bool
        """
        return self._reference_cycle

    @reference_cycle.setter
    def reference_cycle(self, reference_cycle):
        """
        Sets the reference_cycle of this ControllerServiceReferencingComponentDTO.
        If the referencing component represents a controller service, this indicates whether it has already been represented in this hierarchy.

        :param reference_cycle: The reference_cycle of this ControllerServiceReferencingComponentDTO.
        :type: bool
        """

        self._reference_cycle = reference_cycle

    @property
    def referencing_components(self):
        """
        Gets the referencing_components of this ControllerServiceReferencingComponentDTO.
        If the referencing component represents a controller service, these are the components that reference it.

        :return: The referencing_components of this ControllerServiceReferencingComponentDTO.
        :rtype: list[ControllerServiceReferencingComponentEntity]
        """
        return self._referencing_components

    @referencing_components.setter
    def referencing_components(self, referencing_components):
        """
        Sets the referencing_components of this ControllerServiceReferencingComponentDTO.
        If the referencing component represents a controller service, these are the components that reference it.

        :param referencing_components: The referencing_components of this ControllerServiceReferencingComponentDTO.
        :type: list[ControllerServiceReferencingComponentEntity]
        """

        self._referencing_components = referencing_components

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
        if not isinstance(other, ControllerServiceReferencingComponentDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
