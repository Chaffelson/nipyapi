"""
    NiFi Rest API

    The Rest API provides programmatic access to command and control a NiFi instance in real time. Start and                                             stop processors, monitor queues, query provenance data, and more. Each endpoint below includes a description,                                             definitions of the expected input and output, potential response codes, and the authorizations required                                             to invoke each service.

    OpenAPI spec version: 1.28.1
    Contact: dev@nifi.apache.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
import re


class ControllerConfigurationDTO(object):
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
        'max_timer_driven_thread_count': 'int',
        'max_event_driven_thread_count': 'int'
    }

    attribute_map = {
        'max_timer_driven_thread_count': 'maxTimerDrivenThreadCount',
        'max_event_driven_thread_count': 'maxEventDrivenThreadCount'
    }

    def __init__(self, max_timer_driven_thread_count=None, max_event_driven_thread_count=None):
        """
        ControllerConfigurationDTO - a model defined in Swagger
        """

        self._max_timer_driven_thread_count = None
        self._max_event_driven_thread_count = None

        if max_timer_driven_thread_count is not None:
          self.max_timer_driven_thread_count = max_timer_driven_thread_count
        if max_event_driven_thread_count is not None:
          self.max_event_driven_thread_count = max_event_driven_thread_count

    @property
    def max_timer_driven_thread_count(self):
        """
        Gets the max_timer_driven_thread_count of this ControllerConfigurationDTO.
        The maximum number of timer driven threads the NiFi has available.

        :return: The max_timer_driven_thread_count of this ControllerConfigurationDTO.
        :rtype: int
        """
        return self._max_timer_driven_thread_count

    @max_timer_driven_thread_count.setter
    def max_timer_driven_thread_count(self, max_timer_driven_thread_count):
        """
        Sets the max_timer_driven_thread_count of this ControllerConfigurationDTO.
        The maximum number of timer driven threads the NiFi has available.

        :param max_timer_driven_thread_count: The max_timer_driven_thread_count of this ControllerConfigurationDTO.
        :type: int
        """

        self._max_timer_driven_thread_count = max_timer_driven_thread_count

    @property
    def max_event_driven_thread_count(self):
        """
        Gets the max_event_driven_thread_count of this ControllerConfigurationDTO.
        The maximum number of event driven threads the NiFi has available.

        :return: The max_event_driven_thread_count of this ControllerConfigurationDTO.
        :rtype: int
        """
        return self._max_event_driven_thread_count

    @max_event_driven_thread_count.setter
    def max_event_driven_thread_count(self, max_event_driven_thread_count):
        """
        Sets the max_event_driven_thread_count of this ControllerConfigurationDTO.
        The maximum number of event driven threads the NiFi has available.

        :param max_event_driven_thread_count: The max_event_driven_thread_count of this ControllerConfigurationDTO.
        :type: int
        """

        self._max_event_driven_thread_count = max_event_driven_thread_count

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
        if not isinstance(other, ControllerConfigurationDTO):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
