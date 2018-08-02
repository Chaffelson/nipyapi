# coding: utf-8

"""
    NiFi Rest Api

    The Rest Api provides programmatic access to command and control a NiFi instance in real time. Start and                                              stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.7.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class UserGroupDTO(object):
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
        'versioned_component_id': 'str',
        'parent_group_id': 'str',
        'position': 'PositionDTO',
        'identity': 'str',
        'configurable': 'bool',
        'users': 'list[TenantEntity]',
        'access_policies': 'list[AccessPolicyEntity]'
    }

    attribute_map = {
        'id': 'id',
        'versioned_component_id': 'versionedComponentId',
        'parent_group_id': 'parentGroupId',
        'position': 'position',
        'identity': 'identity',
        'configurable': 'configurable',
        'users': 'users',
        'access_policies': 'accessPolicies'
    }

    def __init__(self, id=None, versioned_component_id=None, parent_group_id=None, position=None, identity=None, configurable=None, users=None, access_policies=None):
        """
        UserGroupDTO - a model defined in Swagger
        """

        self._id = None
        self._versioned_component_id = None
        self._parent_group_id = None
        self._position = None
        self._identity = None
        self._configurable = None
        self._users = None
        self._access_policies = None

        if id is not None:
          self.id = id
        if versioned_component_id is not None:
          self.versioned_component_id = versioned_component_id
        if parent_group_id is not None:
          self.parent_group_id = parent_group_id
        if position is not None:
          self.position = position
        if identity is not None:
          self.identity = identity
        if configurable is not None:
          self.configurable = configurable
        if users is not None:
          self.users = users
        if access_policies is not None:
          self.access_policies = access_policies

    @property
    def id(self):
        """
        Gets the id of this UserGroupDTO.
        The id of the component.

        :return: The id of this UserGroupDTO.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this UserGroupDTO.
        The id of the component.

        :param id: The id of this UserGroupDTO.
        :type: str
        """

        self._id = id

    @property
    def versioned_component_id(self):
        """
        Gets the versioned_component_id of this UserGroupDTO.
        The ID of the corresponding component that is under version control

        :return: The versioned_component_id of this UserGroupDTO.
        :rtype: str
        """
        return self._versioned_component_id

    @versioned_component_id.setter
    def versioned_component_id(self, versioned_component_id):
        """
        Sets the versioned_component_id of this UserGroupDTO.
        The ID of the corresponding component that is under version control

        :param versioned_component_id: The versioned_component_id of this UserGroupDTO.
        :type: str
        """

        self._versioned_component_id = versioned_component_id

    @property
    def parent_group_id(self):
        """
        Gets the parent_group_id of this UserGroupDTO.
        The id of parent process group of this component if applicable.

        :return: The parent_group_id of this UserGroupDTO.
        :rtype: str
        """
        return self._parent_group_id

    @parent_group_id.setter
    def parent_group_id(self, parent_group_id):
        """
        Sets the parent_group_id of this UserGroupDTO.
        The id of parent process group of this component if applicable.

        :param parent_group_id: The parent_group_id of this UserGroupDTO.
        :type: str
        """

        self._parent_group_id = parent_group_id

    @property
    def position(self):
        """
        Gets the position of this UserGroupDTO.
        The position of this component in the UI if applicable.

        :return: The position of this UserGroupDTO.
        :rtype: PositionDTO
        """
        return self._position

    @position.setter
    def position(self, position):
        """
        Sets the position of this UserGroupDTO.
        The position of this component in the UI if applicable.

        :param position: The position of this UserGroupDTO.
        :type: PositionDTO
        """

        self._position = position

    @property
    def identity(self):
        """
        Gets the identity of this UserGroupDTO.
        The identity of the tenant.

        :return: The identity of this UserGroupDTO.
        :rtype: str
        """
        return self._identity

    @identity.setter
    def identity(self, identity):
        """
        Sets the identity of this UserGroupDTO.
        The identity of the tenant.

        :param identity: The identity of this UserGroupDTO.
        :type: str
        """

        self._identity = identity

    @property
    def configurable(self):
        """
        Gets the configurable of this UserGroupDTO.
        Whether this tenant is configurable.

        :return: The configurable of this UserGroupDTO.
        :rtype: bool
        """
        return self._configurable

    @configurable.setter
    def configurable(self, configurable):
        """
        Sets the configurable of this UserGroupDTO.
        Whether this tenant is configurable.

        :param configurable: The configurable of this UserGroupDTO.
        :type: bool
        """

        self._configurable = configurable

    @property
    def users(self):
        """
        Gets the users of this UserGroupDTO.
        The users that belong to the user group.

        :return: The users of this UserGroupDTO.
        :rtype: list[TenantEntity]
        """
        return self._users

    @users.setter
    def users(self, users):
        """
        Sets the users of this UserGroupDTO.
        The users that belong to the user group.

        :param users: The users of this UserGroupDTO.
        :type: list[TenantEntity]
        """

        self._users = users

    @property
    def access_policies(self):
        """
        Gets the access_policies of this UserGroupDTO.
        The access policies this user group belongs to. This field was incorrectly defined as an AccessPolicyEntity. For compatibility reasons the field will remain of this type, however only the fields that are present in the AccessPolicySummaryEntity will be populated here.

        :return: The access_policies of this UserGroupDTO.
        :rtype: list[AccessPolicyEntity]
        """
        return self._access_policies

    @access_policies.setter
    def access_policies(self, access_policies):
        """
        Sets the access_policies of this UserGroupDTO.
        The access policies this user group belongs to. This field was incorrectly defined as an AccessPolicyEntity. For compatibility reasons the field will remain of this type, however only the fields that are present in the AccessPolicySummaryEntity will be populated here.

        :param access_policies: The access_policies of this UserGroupDTO.
        :type: list[AccessPolicyEntity]
        """

        self._access_policies = access_policies

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
        if not isinstance(other, UserGroupDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
