# coding: utf-8

"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.27.0
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class FlowRegistryClientDTO(object):
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
        'name': 'str',
        'description': 'str',
        'uri': 'str',
        'type': 'str',
        'bundle': 'BundleDTO',
        'properties': 'dict(str, str)',
        'descriptors': 'dict(str, PropertyDescriptorDTO)',
        'sensitive_dynamic_property_names': 'list[str]',
        'supports_sensitive_dynamic_properties': 'bool',
        'restricted': 'bool',
        'deprecated': 'bool',
        'validation_errors': 'list[str]',
        'validation_status': 'str',
        'annotation_data': 'str',
        'multiple_versions_available': 'bool',
        'extension_missing': 'bool'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'description': 'description',
        'uri': 'uri',
        'type': 'type',
        'bundle': 'bundle',
        'properties': 'properties',
        'descriptors': 'descriptors',
        'sensitive_dynamic_property_names': 'sensitiveDynamicPropertyNames',
        'supports_sensitive_dynamic_properties': 'supportsSensitiveDynamicProperties',
        'restricted': 'restricted',
        'deprecated': 'deprecated',
        'validation_errors': 'validationErrors',
        'validation_status': 'validationStatus',
        'annotation_data': 'annotationData',
        'multiple_versions_available': 'multipleVersionsAvailable',
        'extension_missing': 'extensionMissing'
    }

    def __init__(self, id=None, name=None, description=None, uri=None, type=None, bundle=None, properties=None, descriptors=None, sensitive_dynamic_property_names=None, supports_sensitive_dynamic_properties=None, restricted=None, deprecated=None, validation_errors=None, validation_status=None, annotation_data=None, multiple_versions_available=None, extension_missing=None):
        """
        FlowRegistryClientDTO - a model defined in Swagger
        """

        self._id = None
        self._name = None
        self._description = None
        self._uri = None
        self._type = None
        self._bundle = None
        self._properties = None
        self._descriptors = None
        self._sensitive_dynamic_property_names = None
        self._supports_sensitive_dynamic_properties = None
        self._restricted = None
        self._deprecated = None
        self._validation_errors = None
        self._validation_status = None
        self._annotation_data = None
        self._multiple_versions_available = None
        self._extension_missing = None

        if id is not None:
          self.id = id
        if name is not None:
          self.name = name
        if description is not None:
          self.description = description
        if uri is not None:
          self.uri = uri
        if type is not None:
          self.type = type
        if bundle is not None:
          self.bundle = bundle
        if properties is not None:
          self.properties = properties
        if descriptors is not None:
          self.descriptors = descriptors
        if sensitive_dynamic_property_names is not None:
          self.sensitive_dynamic_property_names = sensitive_dynamic_property_names
        if supports_sensitive_dynamic_properties is not None:
          self.supports_sensitive_dynamic_properties = supports_sensitive_dynamic_properties
        if restricted is not None:
          self.restricted = restricted
        if deprecated is not None:
          self.deprecated = deprecated
        if validation_errors is not None:
          self.validation_errors = validation_errors
        if validation_status is not None:
          self.validation_status = validation_status
        if annotation_data is not None:
          self.annotation_data = annotation_data
        if multiple_versions_available is not None:
          self.multiple_versions_available = multiple_versions_available
        if extension_missing is not None:
          self.extension_missing = extension_missing

    @property
    def id(self):
        """
        Gets the id of this FlowRegistryClientDTO.
        The registry identifier

        :return: The id of this FlowRegistryClientDTO.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this FlowRegistryClientDTO.
        The registry identifier

        :param id: The id of this FlowRegistryClientDTO.
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this FlowRegistryClientDTO.
        The registry name

        :return: The name of this FlowRegistryClientDTO.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this FlowRegistryClientDTO.
        The registry name

        :param name: The name of this FlowRegistryClientDTO.
        :type: str
        """

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this FlowRegistryClientDTO.
        The registry description

        :return: The description of this FlowRegistryClientDTO.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this FlowRegistryClientDTO.
        The registry description

        :param description: The description of this FlowRegistryClientDTO.
        :type: str
        """

        self._description = description

    @property
    def uri(self):
        """
        Gets the uri of this FlowRegistryClientDTO.

        :return: The uri of this FlowRegistryClientDTO.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """
        Sets the uri of this FlowRegistryClientDTO.

        :param uri: The uri of this FlowRegistryClientDTO.
        :type: str
        """

        self._uri = uri

    @property
    def type(self):
        """
        Gets the type of this FlowRegistryClientDTO.
        The type of the controller service.

        :return: The type of this FlowRegistryClientDTO.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this FlowRegistryClientDTO.
        The type of the controller service.

        :param type: The type of this FlowRegistryClientDTO.
        :type: str
        """

        self._type = type

    @property
    def bundle(self):
        """
        Gets the bundle of this FlowRegistryClientDTO.
        The details of the artifact that bundled this processor type.

        :return: The bundle of this FlowRegistryClientDTO.
        :rtype: BundleDTO
        """
        return self._bundle

    @bundle.setter
    def bundle(self, bundle):
        """
        Sets the bundle of this FlowRegistryClientDTO.
        The details of the artifact that bundled this processor type.

        :param bundle: The bundle of this FlowRegistryClientDTO.
        :type: BundleDTO
        """

        self._bundle = bundle

    @property
    def properties(self):
        """
        Gets the properties of this FlowRegistryClientDTO.
        The properties of the controller service.

        :return: The properties of this FlowRegistryClientDTO.
        :rtype: dict(str, str)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this FlowRegistryClientDTO.
        The properties of the controller service.

        :param properties: The properties of this FlowRegistryClientDTO.
        :type: dict(str, str)
        """

        self._properties = properties

    @property
    def descriptors(self):
        """
        Gets the descriptors of this FlowRegistryClientDTO.
        The descriptors for the controller service properties.

        :return: The descriptors of this FlowRegistryClientDTO.
        :rtype: dict(str, PropertyDescriptorDTO)
        """
        return self._descriptors

    @descriptors.setter
    def descriptors(self, descriptors):
        """
        Sets the descriptors of this FlowRegistryClientDTO.
        The descriptors for the controller service properties.

        :param descriptors: The descriptors of this FlowRegistryClientDTO.
        :type: dict(str, PropertyDescriptorDTO)
        """

        self._descriptors = descriptors

    @property
    def sensitive_dynamic_property_names(self):
        """
        Gets the sensitive_dynamic_property_names of this FlowRegistryClientDTO.
        Set of sensitive dynamic property names

        :return: The sensitive_dynamic_property_names of this FlowRegistryClientDTO.
        :rtype: list[str]
        """
        return self._sensitive_dynamic_property_names

    @sensitive_dynamic_property_names.setter
    def sensitive_dynamic_property_names(self, sensitive_dynamic_property_names):
        """
        Sets the sensitive_dynamic_property_names of this FlowRegistryClientDTO.
        Set of sensitive dynamic property names

        :param sensitive_dynamic_property_names: The sensitive_dynamic_property_names of this FlowRegistryClientDTO.
        :type: list[str]
        """

        self._sensitive_dynamic_property_names = sensitive_dynamic_property_names

    @property
    def supports_sensitive_dynamic_properties(self):
        """
        Gets the supports_sensitive_dynamic_properties of this FlowRegistryClientDTO.
        Whether the reporting task supports sensitive dynamic properties.

        :return: The supports_sensitive_dynamic_properties of this FlowRegistryClientDTO.
        :rtype: bool
        """
        return self._supports_sensitive_dynamic_properties

    @supports_sensitive_dynamic_properties.setter
    def supports_sensitive_dynamic_properties(self, supports_sensitive_dynamic_properties):
        """
        Sets the supports_sensitive_dynamic_properties of this FlowRegistryClientDTO.
        Whether the reporting task supports sensitive dynamic properties.

        :param supports_sensitive_dynamic_properties: The supports_sensitive_dynamic_properties of this FlowRegistryClientDTO.
        :type: bool
        """

        self._supports_sensitive_dynamic_properties = supports_sensitive_dynamic_properties

    @property
    def restricted(self):
        """
        Gets the restricted of this FlowRegistryClientDTO.
        Whether the reporting task requires elevated privileges.

        :return: The restricted of this FlowRegistryClientDTO.
        :rtype: bool
        """
        return self._restricted

    @restricted.setter
    def restricted(self, restricted):
        """
        Sets the restricted of this FlowRegistryClientDTO.
        Whether the reporting task requires elevated privileges.

        :param restricted: The restricted of this FlowRegistryClientDTO.
        :type: bool
        """

        self._restricted = restricted

    @property
    def deprecated(self):
        """
        Gets the deprecated of this FlowRegistryClientDTO.
        Whether the reporting task has been deprecated.

        :return: The deprecated of this FlowRegistryClientDTO.
        :rtype: bool
        """
        return self._deprecated

    @deprecated.setter
    def deprecated(self, deprecated):
        """
        Sets the deprecated of this FlowRegistryClientDTO.
        Whether the reporting task has been deprecated.

        :param deprecated: The deprecated of this FlowRegistryClientDTO.
        :type: bool
        """

        self._deprecated = deprecated

    @property
    def validation_errors(self):
        """
        Gets the validation_errors of this FlowRegistryClientDTO.
        Gets the validation errors from the reporting task. These validation errors represent the problems with the reporting task that must be resolved before it can be scheduled to run.

        :return: The validation_errors of this FlowRegistryClientDTO.
        :rtype: list[str]
        """
        return self._validation_errors

    @validation_errors.setter
    def validation_errors(self, validation_errors):
        """
        Sets the validation_errors of this FlowRegistryClientDTO.
        Gets the validation errors from the reporting task. These validation errors represent the problems with the reporting task that must be resolved before it can be scheduled to run.

        :param validation_errors: The validation_errors of this FlowRegistryClientDTO.
        :type: list[str]
        """

        self._validation_errors = validation_errors

    @property
    def validation_status(self):
        """
        Gets the validation_status of this FlowRegistryClientDTO.
        Indicates whether the Processor is valid, invalid, or still in the process of validating (i.e., it is unknown whether or not the Processor is valid)

        :return: The validation_status of this FlowRegistryClientDTO.
        :rtype: str
        """
        return self._validation_status

    @validation_status.setter
    def validation_status(self, validation_status):
        """
        Sets the validation_status of this FlowRegistryClientDTO.
        Indicates whether the Processor is valid, invalid, or still in the process of validating (i.e., it is unknown whether or not the Processor is valid)

        :param validation_status: The validation_status of this FlowRegistryClientDTO.
        :type: str
        """
        allowed_values = ["VALID", "INVALID", "VALIDATING"]
        if validation_status not in allowed_values:
            raise ValueError(
                "Invalid value for `validation_status` ({0}), must be one of {1}"
                .format(validation_status, allowed_values)
            )

        self._validation_status = validation_status

    @property
    def annotation_data(self):
        """
        Gets the annotation_data of this FlowRegistryClientDTO.
        The annotation data for the repoting task. This is how the custom UI relays configuration to the reporting task.

        :return: The annotation_data of this FlowRegistryClientDTO.
        :rtype: str
        """
        return self._annotation_data

    @annotation_data.setter
    def annotation_data(self, annotation_data):
        """
        Sets the annotation_data of this FlowRegistryClientDTO.
        The annotation data for the repoting task. This is how the custom UI relays configuration to the reporting task.

        :param annotation_data: The annotation_data of this FlowRegistryClientDTO.
        :type: str
        """

        self._annotation_data = annotation_data

    @property
    def multiple_versions_available(self):
        """
        Gets the multiple_versions_available of this FlowRegistryClientDTO.
        Whether the flow registry client has multiple versions available.

        :return: The multiple_versions_available of this FlowRegistryClientDTO.
        :rtype: bool
        """
        return self._multiple_versions_available

    @multiple_versions_available.setter
    def multiple_versions_available(self, multiple_versions_available):
        """
        Sets the multiple_versions_available of this FlowRegistryClientDTO.
        Whether the flow registry client has multiple versions available.

        :param multiple_versions_available: The multiple_versions_available of this FlowRegistryClientDTO.
        :type: bool
        """

        self._multiple_versions_available = multiple_versions_available

    @property
    def extension_missing(self):
        """
        Gets the extension_missing of this FlowRegistryClientDTO.
        Whether the underlying extension is missing.

        :return: The extension_missing of this FlowRegistryClientDTO.
        :rtype: bool
        """
        return self._extension_missing

    @extension_missing.setter
    def extension_missing(self, extension_missing):
        """
        Sets the extension_missing of this FlowRegistryClientDTO.
        Whether the underlying extension is missing.

        :param extension_missing: The extension_missing of this FlowRegistryClientDTO.
        :type: bool
        """

        self._extension_missing = extension_missing

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
        if not isinstance(other, FlowRegistryClientDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
