# coding: utf-8

"""
    Cloudera Edge Flow Manager REST API

    This REST API provides remote access to the EFM Server.                                             Endpoints that are marked as [BETA] are subject to change in future releases of the application without backwards compatibility and without a major version change.

    OpenAPI spec version: 1.0.0-SNAPSHOT
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class AgentClass(object):
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
        'name': 'str',
        'description': 'str',
        'agent_manifests': 'list[str]'
    }

    attribute_map = {
        'name': 'name',
        'description': 'description',
        'agent_manifests': 'agentManifests'
    }

    def __init__(self, name=None, description=None, agent_manifests=None):
        """
        AgentClass - a model defined in Swagger
        """

        self._name = None
        self._description = None
        self._agent_manifests = None

        self.name = name
        if description is not None:
          self.description = description
        if agent_manifests is not None:
          self.agent_manifests = agent_manifests

    @property
    def name(self):
        """
        Gets the name of this AgentClass.
        A unique class name for the agent

        :return: The name of this AgentClass.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this AgentClass.
        A unique class name for the agent

        :param name: The name of this AgentClass.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")
        if name is not None and len(name) > 200:
            raise ValueError("Invalid value for `name`, length must be less than or equal to `200`")
        if name is not None and len(name) < 0:
            raise ValueError("Invalid value for `name`, length must be greater than or equal to `0`")

        self._name = name

    @property
    def description(self):
        """
        Gets the description of this AgentClass.
        An optional description of this agent class

        :return: The description of this AgentClass.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this AgentClass.
        An optional description of this agent class

        :param description: The description of this AgentClass.
        :type: str
        """
        if description is not None and len(description) > 8000:
            raise ValueError("Invalid value for `description`, length must be less than or equal to `8000`")
        if description is not None and len(description) < 0:
            raise ValueError("Invalid value for `description`, length must be greater than or equal to `0`")

        self._description = description

    @property
    def agent_manifests(self):
        """
        Gets the agent_manifests of this AgentClass.
        A list of agent manifest ids belonging to this class

        :return: The agent_manifests of this AgentClass.
        :rtype: list[str]
        """
        return self._agent_manifests

    @agent_manifests.setter
    def agent_manifests(self, agent_manifests):
        """
        Sets the agent_manifests of this AgentClass.
        A list of agent manifest ids belonging to this class

        :param agent_manifests: The agent_manifests of this AgentClass.
        :type: list[str]
        """

        self._agent_manifests = agent_manifests

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
        if not isinstance(other, AgentClass):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other