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


class LineageResultsDTO(object):
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
        'errors': 'list[str]',
        'nodes': 'list[ProvenanceNodeDTO]',
        'links': 'list[ProvenanceLinkDTO]'
    }

    attribute_map = {
        'errors': 'errors',
        'nodes': 'nodes',
        'links': 'links'
    }

    def __init__(self, errors=None, nodes=None, links=None):
        """
        LineageResultsDTO - a model defined in Swagger
        """

        self._errors = None
        self._nodes = None
        self._links = None

        if errors is not None:
          self.errors = errors
        if nodes is not None:
          self.nodes = nodes
        if links is not None:
          self.links = links

    @property
    def errors(self):
        """
        Gets the errors of this LineageResultsDTO.
        Any errors that occurred while generating the lineage.

        :return: The errors of this LineageResultsDTO.
        :rtype: list[str]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """
        Sets the errors of this LineageResultsDTO.
        Any errors that occurred while generating the lineage.

        :param errors: The errors of this LineageResultsDTO.
        :type: list[str]
        """

        self._errors = errors

    @property
    def nodes(self):
        """
        Gets the nodes of this LineageResultsDTO.
        The nodes in the lineage.

        :return: The nodes of this LineageResultsDTO.
        :rtype: list[ProvenanceNodeDTO]
        """
        return self._nodes

    @nodes.setter
    def nodes(self, nodes):
        """
        Sets the nodes of this LineageResultsDTO.
        The nodes in the lineage.

        :param nodes: The nodes of this LineageResultsDTO.
        :type: list[ProvenanceNodeDTO]
        """

        self._nodes = nodes

    @property
    def links(self):
        """
        Gets the links of this LineageResultsDTO.
        The links between the nodes in the lineage.

        :return: The links of this LineageResultsDTO.
        :rtype: list[ProvenanceLinkDTO]
        """
        return self._links

    @links.setter
    def links(self, links):
        """
        Sets the links of this LineageResultsDTO.
        The links between the nodes in the lineage.

        :param links: The links of this LineageResultsDTO.
        :type: list[ProvenanceLinkDTO]
        """

        self._links = links

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
        if not isinstance(other, LineageResultsDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
