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


class DocumentedTypeDTO(object):
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
        'type': 'str',
        'bundle': 'BundleDTO',
        'controller_service_apis': 'list[ControllerServiceApiDTO]',
        'description': 'str',
        'restricted': 'bool',
        'usage_restriction': 'str',
        'explicit_restrictions': 'list[ExplicitRestrictionDTO]',
        'deprecation_reason': 'str',
        'tags': 'list[str]'
    }

    attribute_map = {
        'type': 'type',
        'bundle': 'bundle',
        'controller_service_apis': 'controllerServiceApis',
        'description': 'description',
        'restricted': 'restricted',
        'usage_restriction': 'usageRestriction',
        'explicit_restrictions': 'explicitRestrictions',
        'deprecation_reason': 'deprecationReason',
        'tags': 'tags'
    }

    def __init__(self, type=None, bundle=None, controller_service_apis=None, description=None, restricted=None, usage_restriction=None, explicit_restrictions=None, deprecation_reason=None, tags=None):
        """
        DocumentedTypeDTO - a model defined in Swagger
        """

        self._type = None
        self._bundle = None
        self._controller_service_apis = None
        self._description = None
        self._restricted = None
        self._usage_restriction = None
        self._explicit_restrictions = None
        self._deprecation_reason = None
        self._tags = None

        if type is not None:
          self.type = type
        if bundle is not None:
          self.bundle = bundle
        if controller_service_apis is not None:
          self.controller_service_apis = controller_service_apis
        if description is not None:
          self.description = description
        if restricted is not None:
          self.restricted = restricted
        if usage_restriction is not None:
          self.usage_restriction = usage_restriction
        if explicit_restrictions is not None:
          self.explicit_restrictions = explicit_restrictions
        if deprecation_reason is not None:
          self.deprecation_reason = deprecation_reason
        if tags is not None:
          self.tags = tags

    @property
    def type(self):
        """
        Gets the type of this DocumentedTypeDTO.
        The fully qualified name of the type.

        :return: The type of this DocumentedTypeDTO.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this DocumentedTypeDTO.
        The fully qualified name of the type.

        :param type: The type of this DocumentedTypeDTO.
        :type: str
        """

        self._type = type

    @property
    def bundle(self):
        """
        Gets the bundle of this DocumentedTypeDTO.
        The details of the artifact that bundled this type.

        :return: The bundle of this DocumentedTypeDTO.
        :rtype: BundleDTO
        """
        return self._bundle

    @bundle.setter
    def bundle(self, bundle):
        """
        Sets the bundle of this DocumentedTypeDTO.
        The details of the artifact that bundled this type.

        :param bundle: The bundle of this DocumentedTypeDTO.
        :type: BundleDTO
        """

        self._bundle = bundle

    @property
    def controller_service_apis(self):
        """
        Gets the controller_service_apis of this DocumentedTypeDTO.
        If this type represents a ControllerService, this lists the APIs it implements.

        :return: The controller_service_apis of this DocumentedTypeDTO.
        :rtype: list[ControllerServiceApiDTO]
        """
        return self._controller_service_apis

    @controller_service_apis.setter
    def controller_service_apis(self, controller_service_apis):
        """
        Sets the controller_service_apis of this DocumentedTypeDTO.
        If this type represents a ControllerService, this lists the APIs it implements.

        :param controller_service_apis: The controller_service_apis of this DocumentedTypeDTO.
        :type: list[ControllerServiceApiDTO]
        """

        self._controller_service_apis = controller_service_apis

    @property
    def description(self):
        """
        Gets the description of this DocumentedTypeDTO.
        The description of the type.

        :return: The description of this DocumentedTypeDTO.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this DocumentedTypeDTO.
        The description of the type.

        :param description: The description of this DocumentedTypeDTO.
        :type: str
        """

        self._description = description

    @property
    def restricted(self):
        """
        Gets the restricted of this DocumentedTypeDTO.
        Whether this type is restricted.

        :return: The restricted of this DocumentedTypeDTO.
        :rtype: bool
        """
        return self._restricted

    @restricted.setter
    def restricted(self, restricted):
        """
        Sets the restricted of this DocumentedTypeDTO.
        Whether this type is restricted.

        :param restricted: The restricted of this DocumentedTypeDTO.
        :type: bool
        """

        self._restricted = restricted

    @property
    def usage_restriction(self):
        """
        Gets the usage_restriction of this DocumentedTypeDTO.
        The optional description of why the usage of this component is restricted.

        :return: The usage_restriction of this DocumentedTypeDTO.
        :rtype: str
        """
        return self._usage_restriction

    @usage_restriction.setter
    def usage_restriction(self, usage_restriction):
        """
        Sets the usage_restriction of this DocumentedTypeDTO.
        The optional description of why the usage of this component is restricted.

        :param usage_restriction: The usage_restriction of this DocumentedTypeDTO.
        :type: str
        """

        self._usage_restriction = usage_restriction

    @property
    def explicit_restrictions(self):
        """
        Gets the explicit_restrictions of this DocumentedTypeDTO.
        An optional collection of explicit restrictions. If specified, these explicit restrictions will be enfored.

        :return: The explicit_restrictions of this DocumentedTypeDTO.
        :rtype: list[ExplicitRestrictionDTO]
        """
        return self._explicit_restrictions

    @explicit_restrictions.setter
    def explicit_restrictions(self, explicit_restrictions):
        """
        Sets the explicit_restrictions of this DocumentedTypeDTO.
        An optional collection of explicit restrictions. If specified, these explicit restrictions will be enfored.

        :param explicit_restrictions: The explicit_restrictions of this DocumentedTypeDTO.
        :type: list[ExplicitRestrictionDTO]
        """

        self._explicit_restrictions = explicit_restrictions

    @property
    def deprecation_reason(self):
        """
        Gets the deprecation_reason of this DocumentedTypeDTO.
        The description of why the usage of this component is restricted.

        :return: The deprecation_reason of this DocumentedTypeDTO.
        :rtype: str
        """
        return self._deprecation_reason

    @deprecation_reason.setter
    def deprecation_reason(self, deprecation_reason):
        """
        Sets the deprecation_reason of this DocumentedTypeDTO.
        The description of why the usage of this component is restricted.

        :param deprecation_reason: The deprecation_reason of this DocumentedTypeDTO.
        :type: str
        """

        self._deprecation_reason = deprecation_reason

    @property
    def tags(self):
        """
        Gets the tags of this DocumentedTypeDTO.
        The tags associated with this type.

        :return: The tags of this DocumentedTypeDTO.
        :rtype: list[str]
        """
        return self._tags

    @tags.setter
    def tags(self, tags):
        """
        Sets the tags of this DocumentedTypeDTO.
        The tags associated with this type.

        :param tags: The tags of this DocumentedTypeDTO.
        :type: list[str]
        """

        self._tags = tags

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
        if not isinstance(other, DocumentedTypeDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
