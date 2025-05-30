"""
    Apache NiFi Registry REST API

    The REST API provides an interface to a registry with operations for saving, versioning, reading NiFi flows and components.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class AccessPolicySummary(object):
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
        'resource': 'str',
        'action': 'str',
        'configurable': 'bool',
        'revision': 'RevisionInfo'
    }

    attribute_map = {
        'identifier': 'identifier',
        'resource': 'resource',
        'action': 'action',
        'configurable': 'configurable',
        'revision': 'revision'
    }

    def __init__(self, identifier=None, resource=None, action=None, configurable=None, revision=None):
        """
        AccessPolicySummary - a model defined in Swagger
        """

        self._identifier = None
        self._resource = None
        self._action = None
        self._configurable = None
        self._revision = None

        if identifier is not None:
          self.identifier = identifier
        self.resource = resource
        self.action = action
        if configurable is not None:
          self.configurable = configurable
        if revision is not None:
          self.revision = revision

    @property
    def identifier(self):
        """
        Gets the identifier of this AccessPolicySummary.
        The id of the policy. Set by server at creation time.

        :return: The identifier of this AccessPolicySummary.
        :rtype: str
        """
        return self._identifier

    @identifier.setter
    def identifier(self, identifier):
        """
        Sets the identifier of this AccessPolicySummary.
        The id of the policy. Set by server at creation time.

        :param identifier: The identifier of this AccessPolicySummary.
        :type: str
        """

        self._identifier = identifier

    @property
    def resource(self):
        """
        Gets the resource of this AccessPolicySummary.
        The resource for this access policy.

        :return: The resource of this AccessPolicySummary.
        :rtype: str
        """
        return self._resource

    @resource.setter
    def resource(self, resource):
        """
        Sets the resource of this AccessPolicySummary.
        The resource for this access policy.

        :param resource: The resource of this AccessPolicySummary.
        :type: str
        """
        if resource is None:
            raise ValueError("Invalid value for `resource`, must not be `None`")

        self._resource = resource

    @property
    def action(self):
        """
        Gets the action of this AccessPolicySummary.
        The action associated with this access policy.

        :return: The action of this AccessPolicySummary.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this AccessPolicySummary.
        The action associated with this access policy.

        :param action: The action of this AccessPolicySummary.
        :type: str
        """
        if action is None:
            raise ValueError("Invalid value for `action`, must not be `None`")
        allowed_values = ["read", "write", "delete"]
        if action not in allowed_values:
            raise ValueError(
                "Invalid value for `action` ({0}), must be one of {1}"
                .format(action, allowed_values)
            )

        self._action = action

    @property
    def configurable(self):
        """
        Gets the configurable of this AccessPolicySummary.
        Indicates if this access policy is configurable, based on which Authorizer has been configured to manage it.

        :return: The configurable of this AccessPolicySummary.
        :rtype: bool
        """
        return self._configurable

    @configurable.setter
    def configurable(self, configurable):
        """
        Sets the configurable of this AccessPolicySummary.
        Indicates if this access policy is configurable, based on which Authorizer has been configured to manage it.

        :param configurable: The configurable of this AccessPolicySummary.
        :type: bool
        """

        self._configurable = configurable

    @property
    def revision(self):
        """
        Gets the revision of this AccessPolicySummary.
        The revision of this entity used for optimistic-locking during updates.

        :return: The revision of this AccessPolicySummary.
        :rtype: RevisionInfo
        """
        return self._revision

    @revision.setter
    def revision(self, revision):
        """
        Sets the revision of this AccessPolicySummary.
        The revision of this entity used for optimistic-locking during updates.

        :param revision: The revision of this AccessPolicySummary.
        :type: RevisionInfo
        """

        self._revision = revision

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
        if not isinstance(other, AccessPolicySummary):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
