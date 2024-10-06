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


class VerifyConfigRequestDTO(object):
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
        'uri': 'str',
        'submission_time': 'datetime',
        'last_updated': 'datetime',
        'complete': 'bool',
        'failure_reason': 'str',
        'percent_completed': 'int',
        'state': 'str',
        'update_steps': 'list[VerifyConfigUpdateStepDTO]',
        'component_id': 'str',
        'properties': 'dict(str, str)',
        'attributes': 'dict(str, str)',
        'results': 'list[ConfigVerificationResultDTO]'
    }

    attribute_map = {
        'request_id': 'requestId',
        'uri': 'uri',
        'submission_time': 'submissionTime',
        'last_updated': 'lastUpdated',
        'complete': 'complete',
        'failure_reason': 'failureReason',
        'percent_completed': 'percentCompleted',
        'state': 'state',
        'update_steps': 'updateSteps',
        'component_id': 'componentId',
        'properties': 'properties',
        'attributes': 'attributes',
        'results': 'results'
    }

    def __init__(self, request_id=None, uri=None, submission_time=None, last_updated=None, complete=None, failure_reason=None, percent_completed=None, state=None, update_steps=None, component_id=None, properties=None, attributes=None, results=None):
        """
        VerifyConfigRequestDTO - a model defined in Swagger
        """

        self._request_id = None
        self._uri = None
        self._submission_time = None
        self._last_updated = None
        self._complete = None
        self._failure_reason = None
        self._percent_completed = None
        self._state = None
        self._update_steps = None
        self._component_id = None
        self._properties = None
        self._attributes = None
        self._results = None

        if request_id is not None:
          self.request_id = request_id
        if uri is not None:
          self.uri = uri
        if submission_time is not None:
          self.submission_time = submission_time
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
        if update_steps is not None:
          self.update_steps = update_steps
        if component_id is not None:
          self.component_id = component_id
        if properties is not None:
          self.properties = properties
        if attributes is not None:
          self.attributes = attributes
        if results is not None:
          self.results = results

    @property
    def request_id(self):
        """
        Gets the request_id of this VerifyConfigRequestDTO.
        The ID of the request

        :return: The request_id of this VerifyConfigRequestDTO.
        :rtype: str
        """
        return self._request_id

    @request_id.setter
    def request_id(self, request_id):
        """
        Sets the request_id of this VerifyConfigRequestDTO.
        The ID of the request

        :param request_id: The request_id of this VerifyConfigRequestDTO.
        :type: str
        """

        self._request_id = request_id

    @property
    def uri(self):
        """
        Gets the uri of this VerifyConfigRequestDTO.
        The URI for the request

        :return: The uri of this VerifyConfigRequestDTO.
        :rtype: str
        """
        return self._uri

    @uri.setter
    def uri(self, uri):
        """
        Sets the uri of this VerifyConfigRequestDTO.
        The URI for the request

        :param uri: The uri of this VerifyConfigRequestDTO.
        :type: str
        """

        self._uri = uri

    @property
    def submission_time(self):
        """
        Gets the submission_time of this VerifyConfigRequestDTO.
        The timestamp of when the request was submitted

        :return: The submission_time of this VerifyConfigRequestDTO.
        :rtype: datetime
        """
        return self._submission_time

    @submission_time.setter
    def submission_time(self, submission_time):
        """
        Sets the submission_time of this VerifyConfigRequestDTO.
        The timestamp of when the request was submitted

        :param submission_time: The submission_time of this VerifyConfigRequestDTO.
        :type: datetime
        """

        self._submission_time = submission_time

    @property
    def last_updated(self):
        """
        Gets the last_updated of this VerifyConfigRequestDTO.
        The timestamp of when the request was last updated

        :return: The last_updated of this VerifyConfigRequestDTO.
        :rtype: datetime
        """
        return self._last_updated

    @last_updated.setter
    def last_updated(self, last_updated):
        """
        Sets the last_updated of this VerifyConfigRequestDTO.
        The timestamp of when the request was last updated

        :param last_updated: The last_updated of this VerifyConfigRequestDTO.
        :type: datetime
        """

        self._last_updated = last_updated

    @property
    def complete(self):
        """
        Gets the complete of this VerifyConfigRequestDTO.
        Whether or not the request is completed

        :return: The complete of this VerifyConfigRequestDTO.
        :rtype: bool
        """
        return self._complete

    @complete.setter
    def complete(self, complete):
        """
        Sets the complete of this VerifyConfigRequestDTO.
        Whether or not the request is completed

        :param complete: The complete of this VerifyConfigRequestDTO.
        :type: bool
        """

        self._complete = complete

    @property
    def failure_reason(self):
        """
        Gets the failure_reason of this VerifyConfigRequestDTO.
        The reason for the request failing, or null if the request has not failed

        :return: The failure_reason of this VerifyConfigRequestDTO.
        :rtype: str
        """
        return self._failure_reason

    @failure_reason.setter
    def failure_reason(self, failure_reason):
        """
        Sets the failure_reason of this VerifyConfigRequestDTO.
        The reason for the request failing, or null if the request has not failed

        :param failure_reason: The failure_reason of this VerifyConfigRequestDTO.
        :type: str
        """

        self._failure_reason = failure_reason

    @property
    def percent_completed(self):
        """
        Gets the percent_completed of this VerifyConfigRequestDTO.
        A value between 0 and 100 (inclusive) indicating how close the request is to completion

        :return: The percent_completed of this VerifyConfigRequestDTO.
        :rtype: int
        """
        return self._percent_completed

    @percent_completed.setter
    def percent_completed(self, percent_completed):
        """
        Sets the percent_completed of this VerifyConfigRequestDTO.
        A value between 0 and 100 (inclusive) indicating how close the request is to completion

        :param percent_completed: The percent_completed of this VerifyConfigRequestDTO.
        :type: int
        """

        self._percent_completed = percent_completed

    @property
    def state(self):
        """
        Gets the state of this VerifyConfigRequestDTO.
        A description of the current state of the request

        :return: The state of this VerifyConfigRequestDTO.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this VerifyConfigRequestDTO.
        A description of the current state of the request

        :param state: The state of this VerifyConfigRequestDTO.
        :type: str
        """

        self._state = state

    @property
    def update_steps(self):
        """
        Gets the update_steps of this VerifyConfigRequestDTO.
        The steps that are required in order to complete the request, along with the status of each

        :return: The update_steps of this VerifyConfigRequestDTO.
        :rtype: list[VerifyConfigUpdateStepDTO]
        """
        return self._update_steps

    @update_steps.setter
    def update_steps(self, update_steps):
        """
        Sets the update_steps of this VerifyConfigRequestDTO.
        The steps that are required in order to complete the request, along with the status of each

        :param update_steps: The update_steps of this VerifyConfigRequestDTO.
        :type: list[VerifyConfigUpdateStepDTO]
        """

        self._update_steps = update_steps

    @property
    def component_id(self):
        """
        Gets the component_id of this VerifyConfigRequestDTO.
        The ID of the component whose configuration was verified

        :return: The component_id of this VerifyConfigRequestDTO.
        :rtype: str
        """
        return self._component_id

    @component_id.setter
    def component_id(self, component_id):
        """
        Sets the component_id of this VerifyConfigRequestDTO.
        The ID of the component whose configuration was verified

        :param component_id: The component_id of this VerifyConfigRequestDTO.
        :type: str
        """

        self._component_id = component_id

    @property
    def properties(self):
        """
        Gets the properties of this VerifyConfigRequestDTO.
        The configured component properties

        :return: The properties of this VerifyConfigRequestDTO.
        :rtype: dict(str, str)
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this VerifyConfigRequestDTO.
        The configured component properties

        :param properties: The properties of this VerifyConfigRequestDTO.
        :type: dict(str, str)
        """

        self._properties = properties

    @property
    def attributes(self):
        """
        Gets the attributes of this VerifyConfigRequestDTO.
        FlowFile Attributes that should be used to evaluate Expression Language for resolving property values

        :return: The attributes of this VerifyConfigRequestDTO.
        :rtype: dict(str, str)
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """
        Sets the attributes of this VerifyConfigRequestDTO.
        FlowFile Attributes that should be used to evaluate Expression Language for resolving property values

        :param attributes: The attributes of this VerifyConfigRequestDTO.
        :type: dict(str, str)
        """

        self._attributes = attributes

    @property
    def results(self):
        """
        Gets the results of this VerifyConfigRequestDTO.
        The Results of the verification

        :return: The results of this VerifyConfigRequestDTO.
        :rtype: list[ConfigVerificationResultDTO]
        """
        return self._results

    @results.setter
    def results(self, results):
        """
        Sets the results of this VerifyConfigRequestDTO.
        The Results of the verification

        :param results: The results of this VerifyConfigRequestDTO.
        :type: list[ConfigVerificationResultDTO]
        """

        self._results = results

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
        if not isinstance(other, VerifyConfigRequestDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
