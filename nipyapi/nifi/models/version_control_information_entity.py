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


class VersionControlInformationEntity(object):
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
        'process_group_revision': 'RevisionDTO',
        'disconnected_node_acknowledged': 'bool',
        'version_control_information': 'VersionControlInformationDTO'
    }

    attribute_map = {
        'process_group_revision': 'processGroupRevision',
        'disconnected_node_acknowledged': 'disconnectedNodeAcknowledged',
        'version_control_information': 'versionControlInformation'
    }

    def __init__(self, process_group_revision=None, disconnected_node_acknowledged=None, version_control_information=None):
        """
        VersionControlInformationEntity - a model defined in Swagger
        """

        self._process_group_revision = None
        self._disconnected_node_acknowledged = None
        self._version_control_information = None

        if process_group_revision is not None:
          self.process_group_revision = process_group_revision
        if disconnected_node_acknowledged is not None:
          self.disconnected_node_acknowledged = disconnected_node_acknowledged
        if version_control_information is not None:
          self.version_control_information = version_control_information

    @property
    def process_group_revision(self):
        """
        Gets the process_group_revision of this VersionControlInformationEntity.
        The Revision for the Process Group

        :return: The process_group_revision of this VersionControlInformationEntity.
        :rtype: RevisionDTO
        """
        return self._process_group_revision

    @process_group_revision.setter
    def process_group_revision(self, process_group_revision):
        """
        Sets the process_group_revision of this VersionControlInformationEntity.
        The Revision for the Process Group

        :param process_group_revision: The process_group_revision of this VersionControlInformationEntity.
        :type: RevisionDTO
        """

        self._process_group_revision = process_group_revision

    @property
    def disconnected_node_acknowledged(self):
        """
        Gets the disconnected_node_acknowledged of this VersionControlInformationEntity.
        Acknowledges that this node is disconnected to allow for mutable requests to proceed.

        :return: The disconnected_node_acknowledged of this VersionControlInformationEntity.
        :rtype: bool
        """
        return self._disconnected_node_acknowledged

    @disconnected_node_acknowledged.setter
    def disconnected_node_acknowledged(self, disconnected_node_acknowledged):
        """
        Sets the disconnected_node_acknowledged of this VersionControlInformationEntity.
        Acknowledges that this node is disconnected to allow for mutable requests to proceed.

        :param disconnected_node_acknowledged: The disconnected_node_acknowledged of this VersionControlInformationEntity.
        :type: bool
        """

        self._disconnected_node_acknowledged = disconnected_node_acknowledged

    @property
    def version_control_information(self):
        """
        Gets the version_control_information of this VersionControlInformationEntity.
        The Version Control information

        :return: The version_control_information of this VersionControlInformationEntity.
        :rtype: VersionControlInformationDTO
        """
        return self._version_control_information

    @version_control_information.setter
    def version_control_information(self, version_control_information):
        """
        Sets the version_control_information of this VersionControlInformationEntity.
        The Version Control information

        :param version_control_information: The version_control_information of this VersionControlInformationEntity.
        :type: VersionControlInformationDTO
        """

        self._version_control_information = version_control_information

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
        if not isinstance(other, VersionControlInformationEntity):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
