"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class VersionedFlowUpdateRequestDTO(object):
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
        'request_id': 'str',
        'process_group_id': 'str',
        'uri': 'str',
        'last_updated': 'str',
        'complete': 'bool',
        'failure_reason': 'str',
        'percent_completed': 'int',
        'state': 'str',
        'version_control_information': 'VersionControlInformationDTO'
    }

    attribute_map = {
        'request_id': 'requestId',
        'process_group_id': 'processGroupId',
        'uri': 'uri',
        'last_updated': 'lastUpdated',
        'complete': 'complete',
        'failure_reason': 'failureReason',
        'percent_completed': 'percentCompleted',
        'state': 'state',
        'version_control_information': 'versionControlInformation'
    }

    def __init__(self, request_id=None, process_group_id=None, uri=None, last_updated=None, complete=None, failure_reason=None, percent_completed=None, state=None, version_control_information=None):
        """
        VersionedFlowUpdateRequestDTO - a model defined in Swagger
        """

        self._request_id = None
        self._process_group_id = None
        self._uri = None
        self._last_updated = None
        self._complete = None
        self._failure_reason = None
        self._percent_completed = None
        self._state = None
        self._version_control_information = None

        if request_id is not None:
          self.request_id = request_id
        if process_group_id is not None:
          self.process_group_id = process_group_id
        if uri is not None:
          self.uri = uri
        if last_updated is not None:
          self.last_updated = last_updated
        if complete is not None:
          self.complete = complete
        if failure_reason is not None:
          self.failure_reason = failure_reason
        if percent_completed is not None:
          self.percent_completed = percent_completed
        if state is not None:
          self.state = state
        if version_control_information is not None:
          self.version_control_information = version_control_information

    @property
    def request_id(self):
        """
        Gets the request_id of this VersionedFlowUpdateRequestDTO.
        The unique ID of this request.

        :return: The request_id of this VersionedFlowUpdateRequestDTO.
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """
        Sets the request_id of this VersionedFlowUpdateRequestDTO.
        The unique ID of this request.

        :param request_id: The request_id of this VersionedFlowUpdateRequestDTO.
        :type: str
        """

        self._request_id = request_id

    @property
    def process_group_id(self):
        """
        Gets the process_group_id of this VersionedFlowUpdateRequestDTO.
        The unique ID of the Process Group being updated

        :return: The process_group_id of this VersionedFlowUpdateRequestDTO.
        :rtype: str
        """
        return self._process_group_id

    @process_group_id.setter
    def process_group_id(self, process_group_id):
        """
        Sets the process_group_id of this VersionedFlowUpdateRequestDTO.
        The unique ID of the Process Group being updated

        :param process_group_id: The process_group_id of this VersionedFlowUpdateRequestDTO.
        :type: str
        """

        self._process_group_id = process_group_id

    @property
    def uri(self):
        """
        Gets the uri of this VersionedFlowUpdateRequestDTO.
        The URI for future requests to this drop request.

        :return: The uri of this VersionedFlowUpdateRequestDTO.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """
        Sets the uri of this VersionedFlowUpdateRequestDTO.
        The URI for future requests to this drop request.

        :param uri: The uri of this VersionedFlowUpdateRequestDTO.
        :type: str
        """

        self._uri = uri

    @property
    def last_updated(self):
        """
        Gets the last_updated of this VersionedFlowUpdateRequestDTO.
        The last time this request was updated.

        :return: The last_updated of this VersionedFlowUpdateRequestDTO.
        :rtype: str
        """
        return self._last_updated

    @last_updated.setter
    def last_updated(self, last_updated):
        """
        Sets the last_updated of this VersionedFlowUpdateRequestDTO.
        The last time this request was updated.

        :param last_updated: The last_updated of this VersionedFlowUpdateRequestDTO.
        :type: str
        """

        self._last_updated = last_updated

    @property
    def complete(self):
        """
        Gets the complete of this VersionedFlowUpdateRequestDTO.
        Whether or not this request has completed

        :return: The complete of this VersionedFlowUpdateRequestDTO.
        :rtype: bool
        """
        return self._complete

    @complete.setter
    def complete(self, complete):
        """
        Sets the complete of this VersionedFlowUpdateRequestDTO.
        Whether or not this request has completed

        :param complete: The complete of this VersionedFlowUpdateRequestDTO.
        :type: bool
        """

        self._complete = complete

    @property
    def failure_reason(self):
        """
        Gets the failure_reason of this VersionedFlowUpdateRequestDTO.
        An explanation of why this request failed, or null if this request has not failed

        :return: The failure_reason of this VersionedFlowUpdateRequestDTO.
        :rtype: str
        """
        return self._failure_reason

    @failure_reason.setter
    def failure_reason(self, failure_reason):
        """
        Sets the failure_reason of this VersionedFlowUpdateRequestDTO.
        An explanation of why this request failed, or null if this request has not failed

        :param failure_reason: The failure_reason of this VersionedFlowUpdateRequestDTO.
        :type: str
        """

        self._failure_reason = failure_reason

    @property
    def percent_completed(self):
        """
        Gets the percent_completed of this VersionedFlowUpdateRequestDTO.
        The percentage complete for the request, between 0 and 100

        :return: The percent_completed of this VersionedFlowUpdateRequestDTO.
        :rtype: int
        """
        return self._percent_completed

    @percent_completed.setter
    def percent_completed(self, percent_completed):
        """
        Sets the percent_completed of this VersionedFlowUpdateRequestDTO.
        The percentage complete for the request, between 0 and 100

        :param percent_completed: The percent_completed of this VersionedFlowUpdateRequestDTO.
        :type: int
        """

        self._percent_completed = percent_completed

    @property
    def state(self):
        """
        Gets the state of this VersionedFlowUpdateRequestDTO.
        The state of the request

        :return: The state of this VersionedFlowUpdateRequestDTO.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this VersionedFlowUpdateRequestDTO.
        The state of the request

        :param state: The state of this VersionedFlowUpdateRequestDTO.
        :type: str
        """

        self._state = state

    @property
    def version_control_information(self):
        """
        Gets the version_control_information of this VersionedFlowUpdateRequestDTO.
        The VersionControlInformation that describes where the Versioned Flow is located; this may not be populated until the request is completed.

        :return: The version_control_information of this VersionedFlowUpdateRequestDTO.
        :rtype: VersionControlInformationDTO
        """
        return self._version_control_information

    @version_control_information.setter
    def version_control_information(self, version_control_information):
        """
        Sets the version_control_information of this VersionedFlowUpdateRequestDTO.
        The VersionControlInformation that describes where the Versioned Flow is located; this may not be populated until the request is completed.

        :param version_control_information: The version_control_information of this VersionedFlowUpdateRequestDTO.
        :type: VersionControlInformationDTO
        """

        self._version_control_information = version_control_information

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
        if not isinstance(other, VersionedFlowUpdateRequestDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
