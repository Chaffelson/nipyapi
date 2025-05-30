"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class ProcessorRunStatusDetailsDTO(object):
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
        'run_status': 'str',
        'validation_errors': 'list[str]',
        'active_thread_count': 'int'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'run_status': 'runStatus',
        'validation_errors': 'validationErrors',
        'active_thread_count': 'activeThreadCount'
    }

    def __init__(self, id=None, name=None, run_status=None, validation_errors=None, active_thread_count=None):
        """
        ProcessorRunStatusDetailsDTO - a model defined in Swagger
        """

        self._id = None
        self._name = None
        self._run_status = None
        self._validation_errors = None
        self._active_thread_count = None

        if id is not None:
          self.id = id
        if name is not None:
          self.name = name
        if run_status is not None:
          self.run_status = run_status
        if validation_errors is not None:
          self.validation_errors = validation_errors
        if active_thread_count is not None:
          self.active_thread_count = active_thread_count

    @property
    def id(self):
        """
        Gets the id of this ProcessorRunStatusDetailsDTO.
        The ID of the processor

        :return: The id of this ProcessorRunStatusDetailsDTO.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ProcessorRunStatusDetailsDTO.
        The ID of the processor

        :param id: The id of this ProcessorRunStatusDetailsDTO.
        :type: str
        """

        self._id = id

    @property
    def name(self):
        """
        Gets the name of this ProcessorRunStatusDetailsDTO.
        The name of the processor

        :return: The name of this ProcessorRunStatusDetailsDTO.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this ProcessorRunStatusDetailsDTO.
        The name of the processor

        :param name: The name of this ProcessorRunStatusDetailsDTO.
        :type: str
        """

        self._name = name

    @property
    def run_status(self):
        """
        Gets the run_status of this ProcessorRunStatusDetailsDTO.
        The run status of the processor

        :return: The run_status of this ProcessorRunStatusDetailsDTO.
        :rtype: str
        """
        return self._run_status

    @run_status.setter
    def run_status(self, run_status):
        """
        Sets the run_status of this ProcessorRunStatusDetailsDTO.
        The run status of the processor

        :param run_status: The run_status of this ProcessorRunStatusDetailsDTO.
        :type: str
        """
        allowed_values = ["Running", "Stopped", "Invalid", "Validating", "Disabled"]
        if run_status not in allowed_values:
            raise ValueError(
                "Invalid value for `run_status` ({0}), must be one of {1}"
                .format(run_status, allowed_values)
            )

        self._run_status = run_status

    @property
    def validation_errors(self):
        """
        Gets the validation_errors of this ProcessorRunStatusDetailsDTO.
        The processor's validation errors

        :return: The validation_errors of this ProcessorRunStatusDetailsDTO.
        :rtype: list[str]
        """
        return self._validation_errors

    @validation_errors.setter
    def validation_errors(self, validation_errors):
        """
        Sets the validation_errors of this ProcessorRunStatusDetailsDTO.
        The processor's validation errors

        :param validation_errors: The validation_errors of this ProcessorRunStatusDetailsDTO.
        :type: list[str]
        """

        self._validation_errors = validation_errors

    @property
    def active_thread_count(self):
        """
        Gets the active_thread_count of this ProcessorRunStatusDetailsDTO.
        The current number of threads that the processor is currently using

        :return: The active_thread_count of this ProcessorRunStatusDetailsDTO.
        :rtype: int
        """
        return self._active_thread_count

    @active_thread_count.setter
    def active_thread_count(self, active_thread_count):
        """
        Sets the active_thread_count of this ProcessorRunStatusDetailsDTO.
        The current number of threads that the processor is currently using

        :param active_thread_count: The active_thread_count of this ProcessorRunStatusDetailsDTO.
        :type: int
        """

        self._active_thread_count = active_thread_count

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
        if not isinstance(other, ProcessorRunStatusDetailsDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
